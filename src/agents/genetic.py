from .base_agent import OptimizerAgent
import random
import time
import copy

class GeneticAgent(OptimizerAgent):
    def __init__(self, env, pop_size=50, generations=20, mutation_rate=0.1, genome_length=50, elitism_count=5):
        super().__init__(env)
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.genome_length = genome_length
        self.elitism_count = elitism_count

    def evaluate_genome(self, env, genome):
        try:
            env.reset()
            for action in genome:
                env.step(action)
            return env.observation["IrInstructionCount"]
        except Exception:
            return float('inf')

    def create_population(self, pop_size, genome_length, action_space_size):
        return [
            [random.randint(0, action_space_size - 1) for _ in range(genome_length)]
            for _ in range(pop_size)
        ]
    
    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def mutate(self, genome, action_space_size, mutation_rate):
        for i in range(len(genome)):
            if random.random() < mutation_rate:
                genome[i] = random.randint(0, action_space_size - 1)
        return genome

    def train(self):
        print(f"--- pokretanje genetic agenta na {self.env.benchmark} ---")
        start_time = time.time()
        
        action_space_size = self.env.action_space.n
        
        population = self.create_population(self.pop_size, self.genome_length, action_space_size)
        
        print(f"Populacija: {self.pop_size} | Generacija: {self.generations}")

        for gen in range(1, self.generations + 1):
            scores = []
            
            for genome in population:
                with self.env.fork() as temp_env:
                    score = self.evaluate_genome(temp_env, genome)
                    scores.append(score)

            gen_best = min(scores)
            gen_avg = sum(scores) / len(scores)
            
            best_idx = scores.index(gen_best)
            best_genome_this_gen = population[best_idx]
            
            if self.update_best(gen_best, best_genome_this_gen):
                print(f"Gen {gen}: novi rekord! {gen_best} (Avg: {gen_avg:.1f})")
            else:
                print(f"Gen {gen}: Best {gen_best} | Avg {gen_avg:.1f}")
            
            self.history.append({
                "gen": gen,
                "best": int(gen_best),
                "avg": float(gen_avg)
            })

            sorted_pop_tuples = sorted(zip(scores, population))
            
            new_population = [genome for _, genome in sorted_pop_tuples[:self.elitism_count]]
            
            while len(new_population) < self.pop_size:
                p1_idx = random.randint(0, self.pop_size // 2)
                p2_idx = random.randint(0, self.pop_size // 2)
                
                parent1 = sorted_pop_tuples[p1_idx][1]
                parent2 = sorted_pop_tuples[p2_idx][1]
                
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1, action_space_size, self.mutation_rate)
                child2 = self.mutate(child2, action_space_size, self.mutation_rate)
                
                new_population.append(child1)
                if len(new_population) < self.pop_size:
                    new_population.append(child2)
            
            population = new_population

        duration = time.time() - start_time
        print("-" * 50)
        print(f"genetic zavrsio za {duration:.1f} sekundi.")
        print(f"Najbolji rezultat: {self.best_score}")