import compiler_gym
import subprocess
import os
import sys
import re

def sanitize_ir_for_riscv(ir_text):
    """
    Cisti LLVM IR od x86 specificnih atributa kako bi llc
    mogao da ga prevede u RISC-V asembler bez greske.
    """
    # 1. Promeni target triple u RISC-V
    ir_text = re.sub(r'target triple = ".*?"', 'target triple = "riscv64-unknown-linux-gnu"', ir_text)
    
    # 2. Obrisi target-cpu atribut (npr. "target-cpu"="x86-64")
    ir_text = re.sub(r'"target-cpu"=".*?"', '', ir_text)
    
    # 3. Obrisi target-features atribut (npr. "target-features"="+sse,+mmx...")
    ir_text = re.sub(r'"target-features"=".*?"', '', ir_text)
    
    # 4. Obrisi x86 specificne atribute iz liste atributa
    lines = ir_text.split('\n')
    cleaned_lines = []
    for line in lines:
        if "attributes #" in line:
            # Ukloni x86 smece iz definicije atributa
            line = line.replace(' x86_64_sysvcc', '')
        cleaned_lines.append(line)
        
    return '\n'.join(cleaned_lines)

def verify_optimization(benchmark, actions, output_dir="validation_output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\n--- POKRETANJE VALIDACIJE ZA {benchmark} ---")

    env = compiler_gym.make("llvm-v0")
    try:
        env.reset(benchmark=benchmark)
    except ValueError:
        print(f"[GRESKA] Benchmark nije pronadjen. Koristim qsort.")
        env.reset(benchmark="cbench-v1/qsort")

    # --- 1. Generisanje ORIGINALNIH fajlova za izvrsavanje (na PC-u) ---
    env.write_bitcode(f"{output_dir}/baseline.bc")
    original_baseline_ir = env.ir  # Cuvamo IR
    
    for action in actions:
        env.step(action)

    env.write_bitcode(f"{output_dir}/optimized.bc")
    original_optimized_ir = env.ir # Cuvamo IR

    # --- 2. Generisanje RISC-V Asemblera (sa ciscenjem) ---
    print("[INFO] Generisanje RISC-V asemblera (.s fajlovi)...")
    
    # Cistimo IR samo za potrebe generisanja asemblera
    clean_base_ir = sanitize_ir_for_riscv(original_baseline_ir)
    clean_opt_ir = sanitize_ir_for_riscv(original_optimized_ir)

    # Pisemo ociscene .ll fajlove
    with open(f"{output_dir}/baseline_riscv.ll", "w") as f:
        f.write(clean_base_ir)
    with open(f"{output_dir}/optimized_riscv.ll", "w") as f:
        f.write(clean_opt_ir)

    try:
        # Pozivamo llc nad OCISCENIM fajlovima
        subprocess.run(["llc", "-march=riscv64", "-mcpu=generic-rv64", "-filetype=asm", f"{output_dir}/baseline_riscv.ll", "-o", f"{output_dir}/baseline.s"], check=True)
        subprocess.run(["llc", "-march=riscv64", "-mcpu=generic-rv64", "-filetype=asm", f"{output_dir}/optimized_riscv.ll", "-o", f"{output_dir}/optimized.s"], check=True)
        print(f"RISC-V asembler sacuvan u '{output_dir}/'")
    except FileNotFoundError:
        print("[UPOZORENJE] 'llc' komanda nije nadjena.")
    except Exception as e:
        print(f"[GRESKA] Generisanje asemblera nije uspelo (ali validacija se nastavlja): {e}")

    # --- 3. Kompilacija i Izvrsavanje (koristimo ORIGINALNE .bc fajlove) ---
    print("[INFO] Kompilacija i izvrsavanje radi provere ispravnosti...")
    try:
        subprocess.run(["clang", f"{output_dir}/baseline.bc", "-o", f"{output_dir}/baseline_bin", "-lm"], check=True)
        subprocess.run(["clang", f"{output_dir}/optimized.bc", "-o", f"{output_dir}/optimized_bin", "-lm"], check=True)

        res_base = subprocess.run([f"./{output_dir}/baseline_bin"], capture_output=True)
        res_opt = subprocess.run([f"./{output_dir}/optimized_bin"], capture_output=True)

        base_out = res_base.stdout.decode('utf-8', errors='replace').strip()
        opt_out = res_opt.stdout.decode('utf-8', errors='replace').strip()

        print(f"\n[DEBUG] Baseline Output:  '{base_out}'")
        print(f"[DEBUG] Optimized Output: '{opt_out}'")

        if res_base.stdout == res_opt.stdout and res_base.returncode == res_opt.returncode:
            print("USPEH: Optimizovani kod daje identican rezultat kao original!")
            return True
        else:
            print("FAILURE: Izlazi se razlikuju! Optimizacija je pokvarila program.")
            return False

    except FileNotFoundError:
        print("[UPOZORENJE] 'clang' nije nadjen. Ne mogu da izvrsim kod.")
        return None
    except Exception as e:
        print(f"[GRESKA] Pri izvrsavanju: {e}")
        return False
    finally:
        env.close()
