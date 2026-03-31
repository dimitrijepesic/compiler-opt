import compiler_gym
import subprocess
import os
import sys
import shutil
from src.agents.greedy import GreedyAgent

# TVOJA PUTANJA KOJU SI NASAO
CLANG_CMD = "/home/dimit/.local/share/compiler_gym/llvm-v0/bin/clang"

SOURCE_FILE = "demo/test.c"
ABS_PATH_SOURCE = os.path.abspath(SOURCE_FILE)
BC_FILE = "demo/test.bc"
ABS_PATH_BC = os.path.abspath(BC_FILE)

def main():
    print(f"\nPOKRETANJE DEMO MODA NA: {SOURCE_FILE}")
    
    # Provera da li fajl postoji
    if not os.path.exists(CLANG_CMD):
        print(f"GRESKA: Nije nadjen clang na putanji: {CLANG_CMD}")
        sys.exit(1)

    print(f"[1/5] Priprema koda koristeci interni clang...")
    
    try:
        subprocess.run([CLANG_CMD, "-O0", "-Xclang", "-disable-O0-optnone", "-emit-llvm", "-c", SOURCE_FILE, "-o", BC_FILE], check=True)
    except Exception as e:
        print(f"Greska pri kompilaciji: {e}")
        sys.exit(1)

    print("[2/5] Ucitavanje tvog koda u CompilerGym...")
    env = compiler_gym.make("llvm-v0")
    
    benchmark_uri = f"file://{ABS_PATH_BC}"
    
    try:
        env.reset(benchmark=benchmark_uri)
    except ValueError as e:
        print(f"GRESKA pri ucitavanju fajla: {e}")
        sys.exit(1)

    print(f"   Pocetna velicina instrukcija: {env.observation['IrInstructionCount']}")

    print("[3/5] Agent optimizuje tvoj kod...")
    agent = GreedyAgent(env)
    agent.train(steps=15) 
    
    env.write_bitcode("demo/optimized.bc")
    
    print("[4/5] Pravljenje izvrsnih fajlova (.bin)...")
    
    # KORISTIMO SISTEMSKI CLANG ZA OVO JER ON ZNA GDE SU BIBLIOTEKE
    SYSTEM_CLANG = "clang" 
    
    # Ako ovo pukne, znaci da nemas obican clang instaliran (sudo apt install clang)
    subprocess.run([SYSTEM_CLANG, BC_FILE, "-o", "demo/baseline_bin", "-lm"], check=True)
    subprocess.run([SYSTEM_CLANG, "demo/optimized.bc", "-o", "demo/optimized_bin", "-lm"], check=True)

    print("\n" + "="*50)
    print("REZULTATI")
    print("="*50)

    print("\n--- 1. ORIGINALNI KOD OUTPUT ---")
    out_base = subprocess.run(["./demo/baseline_bin"], capture_output=True, text=True)
    print(out_base.stdout.strip())

    print("\n--- 2. OPTIMIZOVANI KOD OUTPUT ---")
    out_opt = subprocess.run(["./demo/optimized_bin"], capture_output=True, text=True)
    print(out_opt.stdout.strip())

    if out_base.stdout == out_opt.stdout:
        print("\nVALIDACIJA USPESNA: Rezultati su IDENTICNI!")
    else:
        print("\nGRESKA: Agent je pokvario kod!")

    size_base = os.path.getsize("demo/baseline_bin")
    size_opt = os.path.getsize("demo/optimized_bin")
    
    bc_size_base = os.path.getsize(BC_FILE)
    bc_size_opt = os.path.getsize("demo/optimized.bc")

    print("\n--- STATISTIKA VELICINE (BITCODE) ---")
    print(f"Original:    {bc_size_base} bytes")
    print(f"Optimizovan: {bc_size_opt} bytes")
    print(f"USTEDA:      {bc_size_base - bc_size_opt} bytes manje!")

    env.close()

if __name__ == "__main__":
    main()