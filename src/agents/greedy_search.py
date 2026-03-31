import compiler_gym
import sys
import copy

def main():
    print("--- Pokretanje GREEDY SEARCH Eksperimenta ---")
    
    # Podesavanja
    BENCHMARK = "cbench-v1/qsort"
    STEPS = 15  # Manje koraka jer je sporo (15 * 124 simulacije!)
    
    env = compiler_gym.make("llvm-v0")
    env.reset(benchmark=BENCHMARK)
    env.observation_space = "IrInstructionCount"
    
    current_size = env.reset()
    print(f"Start: {current_size}")
    
    actions_taken = []

    for step in range(1, STEPS + 1):
        print(f"\n--- Korak {step}/{STEPS} ---")
        best_action = None
        best_reduction = 0
        best_new_size = current_size

        # Probamo svaku od 124 akcije
        # Koristimo fork() da ne bi pokvarili glavno stanje dok testiramo
        for action in range(env.action_space.n):
            # Fork je brz nacin da kopiramo stanje
            with env.fork() as temp_env:
                observation, reward, done, info = temp_env.step(action)
                
                # Ako je smanjilo kod vise nego bilo sta do sad u ovom koraku
                if observation < best_new_size:
                    best_new_size = observation
                    best_action = action
                    best_reduction = current_size - best_new_size

        # Ako smo nasli nesto sto poboljsava
        if best_action is not None:
            print(f"  Najbolja akcija: {env.action_space.to_string(best_action)}")
            print(f"  Smanjenje: {current_size} -> {best_new_size} (delta: -{best_reduction})")
            
            # Primenjujemo tu akciju na PRAVI environment
            observation, reward, done, info = env.step(best_action)
            current_size = observation
            actions_taken.append(best_action)
        else:
            print("  Nijedna akcija ne smanjuje kod. Lokalni minimum.")
            break

    print("\n" + "="*40)
    print("KONACNI REZULTATI (Greedy):")
    print(f"Start: 638") # Znamo od ranije
    print(f"Kraj:  {current_size}")
    
    improvement = (638 - current_size) / 638 * 100
    print(f"Procenat poboljsanja: {improvement:.2f}%")
    print(f"Sekvenca: {actions_taken}")
    
    env.close()

if __name__ == "__main__":
    main()
