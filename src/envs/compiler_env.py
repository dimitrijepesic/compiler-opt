import compiler_gym

def make_env(benchmark="cbench-v1/qsort", reward_type="space"):
    """
    Fabrika koja kreira i konfigurise okruzenje.
    Centralizovano mesto za sva podesavanja CompilerGym-a.
    """
    env = compiler_gym.make("llvm-v0")

    try:
        env.reset(benchmark=benchmark)
    except ValueError:
        print(f"[GRESKA] Benchmark '{benchmark}' nije pronadjen. Koristim 'cbench-v1/qsort' kao fallback.")
        env.reset(benchmark="cbench-v1/qsort")

    if reward_type == "space":
        env.observation_space = "IrInstructionCount"

    elif reward_type == "execution":
        print("[INFO] Execution mod je u pripremi. Koristim IrInstructionCount kao placeholder.")
        env.observation_space = "IrInstructionCount"

    else:
        raise ValueError(f"Nepoznat tip nagrade: {reward_type}. Koristi 'space' ili 'execution'.")

    return env
