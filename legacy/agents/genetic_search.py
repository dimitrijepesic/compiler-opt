# Legacy standalone genetic-search script, superseded by the PPO agents
# in src/agents/ppo_*.py. Kept for provenance only.
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
        return float("inf")


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
    print(f"--- STARTING EVOLUTION ON {BENCHMARK} ---")
    start_time = time.time()

    env = compiler_gym.make("llvm-v0")
    env.reset(benchmark=BENCHMARK)
    env.observation_space = "IrInstructionCount"
    action_space_size = env.action_space.n

    population = create_population(POPULATION_SIZE, GENOME_LENGTH, action_space_size)

    global_best_score = float("inf")
    GREEDY_RESULT = 271

    print(f"Population: {POPULATION_SIZE} | Generations: {GENERATIONS}")
    print("-" * 50)

    for gen in range(1, GENERATIONS + 1):
        scores = []
        for genome in population:
            with env.fork() as temp_env:
                score = evaluate_genome(temp_env, genome)
                scores.append(score)

        gen_best = min(scores)
        gen_avg = sum(scores) / len(scores)

        if gen_best < global_best_score:
            global_best_score = gen_best
            print(f"Gen {gen}: NEW RECORD! {gen_best} (Avg: {gen_avg:.1f})")
        else:
            print(f"Gen {gen}: Best {gen_best} | Avg {gen_avg:.1f}")

        # Keep (score, genome) pairs so the selection logic below stays sorted
        sorted_pop_tuples = sorted(zip(scores, population))

        # Elitism: carry over the genomes from the top pairs
        new_population = [genome for _, genome in sorted_pop_tuples[:ELITISM_COUNT]]

        while len(new_population) < POPULATION_SIZE:
            # Tournament selection: pick two indices at random from the top half
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
    print(f"FINISHED IN {duration:.1f} seconds.")
    print(f"Greedy result: {GREEDY_RESULT}")
    print(f"EVOLUTION RESULT: {global_best_score}")

    if global_best_score < GREEDY_RESULT:
        print("\nSUCCESS! Evolution beat Greedy!")
    elif global_best_score == GREEDY_RESULT:
        print("\nTIE. The local minimum is strong.")
    else:
        print("\nGREEDY IS STILL KING. Evolution needs more time.")

    env.close()


if __name__ == "__main__":
    main()
