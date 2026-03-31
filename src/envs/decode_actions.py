import compiler_gym

def main():
    # 1. Samo nam treba environment da izvucemo imena, ne moramo da resetujemo benchmark
    env = compiler_gym.make("llvm-v0")
    
    # 2. Ovo je tvoja pobednicka sekvenca iz Random Search-a
    winning_sequence = [100, 16, 37, 48, 9, 50, 72, 73, 44, 61]
    
    print(f"\n{'ID':<5} | {'OPTIMIZACIJA (LLVM PASS)':<40}")
    print("-" * 50)
    
    # 3. Pretvaramo ID -> Ime
    names = env.action_space.names
    
    for action_id in winning_sequence:
        if action_id < len(names):
            action_name = names[action_id]
            print(f"{action_id:<5} | {action_name:<40}")
        else:
            print(f"{action_id:<5} | [UNKNOWN ID]")

    env.close()

if __name__ == "__main__":
    main()
