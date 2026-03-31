import compiler_gym
import random
import copy
import time
import sys

BENCHMARK = "cbench-v1/qsort"
POPULATION_SIZE = 50
GENOME_LENGTH = 50
GENERATIONS = 20
MUTATION_RATE = 0.1
ELITISM_COUNT = 5

def evaluate_genome(env, genome):
    try:
        env.reset()
        for action in genome:
            env.step(action)
        return env.observation["IrInstructionCount"]
    except Exception:
        return float('inf')

def create_population(pop_size, genome_length, action_space_size):
    return [
        [random.randint(0, action_space_size - 1) for _ in range(genome_length)]
        for _ in range(pop_size)
    ]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(genome, action_space_size, mutation_rate):
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            genome[i] = random.randint(0, action_space_size - 1)
    return genome

def main():
    print(f"--- POKRETANJE EVOLUCIJE NA {BENCHMARK} ---")
    start_time = time.time()

    env = compiler_gym.make("llvm-v0")
    env.reset(benchmark=BENCHMARK)
    env.observation_space = "IrInstructionCount"
    action_space_size = env.action_space.n

    population = create_population(POPULATION_SIZE, GENOME_LENGTH, action_space_size)

    global_best_score = float('inf')
    GREEDY_RESULT = 271

    print(f"Populacija: {POPULATION_SIZE} | Generacija: {GENERATIONS}")
    print("-" * 50)

    for gen in range(1, GENERATIONS + 1):
        scores = []
        # Evaluacija
        for genome in population:
            with env.fork() as temp_env:
                score = evaluate_genome(temp_env, genome)
                scores.append(score)

        gen_best = min(scores)
        gen_avg = sum(scores) / len(scores)

        if gen_best < global_best_score:
            global_best_score = gen_best
            print(f"Gen {gen}: NOVI REKORD! {gen_best} (Avg: {gen_avg:.1f})")
        else:
            print(f"Gen {gen}: Best {gen_best} | Avg {gen_avg:.1f}")

        # --- FIX JE OVDE ---
        # Sada cuvamo parove (score, genome) da bi logika dole radila
        sorted_pop_tuples = sorted(zip(scores, population))
        
        # Elitizam: Uzimamo genome iz prvih 5 parova
        new_population = [genome for _, genome in sorted_pop_tuples[:ELITISM_COUNT]]

        while len(new_population) < POPULATION_SIZE:
            # Turnirska selekcija
            # Biramo nasumicno dvoje, ali pristupamo [1] jer je sorted_pop_tuples lista parova
            p1_idx = random.randint(0, POPULATION_SIZE // 2)
            p2_idx = random.randint(0, POPULATION_SIZE // 2)
            
            parent1 = sorted_pop_tuples[p1_idx][1]
            parent2 = sorted_pop_tuples[p2_idx][1]

            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, action_space_size, MUTATION_RATE)
            child2 = mutate(child2, action_space_size, MUTATION_RATE)

            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    print("-" * 50)
    duration = time.time() - start_time
    print(f"ZAVRSENO ZA {duration:.1f} sekundi.")
    print(f"Greedy rezultat: {GREEDY_RESULT}")
    print(f"EVOLUCIJA REZULTAT: {global_best_score}")

    if global_best_score < GREEDY_RESULT:
        print("\nUSPEH! Evolucija je pobedila Greedy!")
    elif global_best_score == GREEDY_RESULT:
        print("\nNERESENO. Lokalni minimum je jak.")
    else:
        print("\nGREEDY JE I DALJE KRALJ. Evoluciji treba vise vremena.")

    env.close()

if __name__ == "__main__":
    main()
