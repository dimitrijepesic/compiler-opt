import compiler_gym

def main():
	env = compiler_gym.make("llvm-v0")
	env.reset(benchmark = "cbench-v1/qsort")
	
	print("1. metadata")
	print(f"Benchmark URI: {env.benchmark}")
	
	print()	
	print("2. llvm ir prvih 20 linija")
	env.observation_space = "Ir"

	ir_code = env.reset()

	print("\n".join(ir_code.splitlines()[:20]))
	
	print("\n to je to")
	env.close()

if __name__ == "__main__":
	main()
