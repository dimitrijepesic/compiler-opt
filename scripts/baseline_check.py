import compiler_gym
import sys

def main():
    print("--- Pokretanje CompilerGym Eksperimenta ---")
    
    try:
        # 1. Kreiramo okruženje
        env = compiler_gym.make("llvm-v0")
        print("[SUCCESS] Okruzenje kreirano.")

        # 2. Učitavamo qsort
        env.reset(benchmark="cbench-v1/qsort")
        print("[SUCCESS] Benchmark 'qsort' ucitan.")

        # 3. Postavljamo metriku
        env.observation_space = "IrInstructionCount"
        
        # 4. Uzimamo Baseline
        pocetni_broj = env.reset()
        print(f"\n>>> BASELINE BROJ INSTRUKCIJA: {pocetni_broj}")
        
        # 5. Broj akcija
        broj_akcija = env.action_space.n
        print(f">>> VELICINA ACTION SPACE-A: {broj_akcija}")

        # 6. Zatvaramo
        env.close()
        print("\n--- Eksperiment uspesno zavrsen ---")

    except Exception as e:
        print(f"\n[CRITICAL ERROR]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
