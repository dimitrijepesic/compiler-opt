import compiler_gym
import numpy as np
import sys

def main():
    print("--- Pokretanje RANDOM SEARCH Eksperimenta ---")
    
    # Podesavanja eksperimenta
    BENCHMARK = "cbench-v1/qsort"
    EPISODES = 20        # Koliko puta cemo pokusati iz pocetka
    STEPS_PER_EP = 50    # Koliko optimizacija primenjujemo u nizu
    
    env = compiler_gym.make("llvm-v0")
    env.reset(benchmark=BENCHMARK)
    env.observation_space = "IrInstructionCount"
    
    baseline = 638 # Tvoj broj od malopre
    global_best_size = baseline
    best_actions = []

    print(f"Target Benchmark: {BENCHMARK}")
    print(f"Baseline Size: {baseline}")
    print("-" * 40)

    for ep in range(1, EPISODES + 1):
        env.reset() # Vraca na 638
        episode_actions = []
        
        for step in range(STEPS_PER_EP):
            # 1. Izaberi RANDOM akciju
            action = env.action_space.sample()
            
            # 2. Primeni je
            observation, reward, done, info = env.step(action)
            episode_actions.append(action)
            
            # 3. Proveri da li je ovo novi rekord
            current_size = observation
            if current_size < global_best_size:
                print(f"[NOVI REKORD] Epizoda {ep}, Korak {step}: {global_best_size} -> {current_size}")
                global_best_size = current_size
                best_actions = list(episode_actions) # Kopiramo listu
            
            if done: 
                break
        
        # Opcionalno: Ispis napretka
        # print(f"Kraj epizode {ep}. Zavrsna velicina: {current_size}")

    print("-" * 40)
    print("REZULTATI EKSPERIMENTA:")
    print(f"Pocetno: {baseline}")
    print(f"Najbolje pronadjeno (Random): {global_best_size}")
    
    improvement = (baseline - global_best_size) / baseline * 100
    print(f"Procenat poboljsanja: {improvement:.2f}%")
    print(f"Pobednicka sekvenca akcija (prvih 10): {best_actions[:10]}...")

    env.close()

if __name__ == "__main__":
    main()
