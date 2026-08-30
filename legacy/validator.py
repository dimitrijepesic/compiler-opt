# Legacy RISC-V cross-compilation validator, from a prototype unrelated to
# the paper's ARM Cortex-M cross-compilation work (scripts/measure_binary_metrics.py
# --mtriple). Kept for provenance only.
import compiler_gym
import subprocess
import os
import sys
import re


def sanitize_ir_for_riscv(ir_text):
    """Strip x86-specific attributes from LLVM IR so llc can translate it
    to RISC-V assembly without errors."""
    # 1. Change the target triple to RISC-V
    ir_text = re.sub(r'target triple = ".*?"', 'target triple = "riscv64-unknown-linux-gnu"', ir_text)

    # 2. Drop the target-cpu attribute (e.g. "target-cpu"="x86-64")
    ir_text = re.sub(r'"target-cpu"=".*?"', '', ir_text)

    # 3. Drop the target-features attribute (e.g. "target-features"="+sse,+mmx...")
    ir_text = re.sub(r'"target-features"=".*?"', '', ir_text)

    # 4. Drop x86-specific attributes from the attribute list
    lines = ir_text.split('\n')
    cleaned_lines = []
    for line in lines:
        if "attributes #" in line:
            line = line.replace(' x86_64_sysvcc', '')
        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def verify_optimization(benchmark, actions, output_dir="validation_output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\n--- RUNNING VALIDATION FOR {benchmark} ---")

    env = compiler_gym.make("llvm-v0")
    try:
        env.reset(benchmark=benchmark)
    except ValueError:
        print("[ERROR] Benchmark not found. Falling back to qsort.")
        env.reset(benchmark="cbench-v1/qsort")

    # --- 1. Generate the original files for execution (on the host) ---
    env.write_bitcode(f"{output_dir}/baseline.bc")
    original_baseline_ir = env.ir  # Keep the IR

    for action in actions:
        env.step(action)

    env.write_bitcode(f"{output_dir}/optimized.bc")
    original_optimized_ir = env.ir  # Keep the IR

    # --- 2. Generate RISC-V assembly (with sanitization) ---
    print("[INFO] Generating RISC-V assembly (.s files)...")

    # Sanitize the IR only for assembly generation
    clean_base_ir = sanitize_ir_for_riscv(original_baseline_ir)
    clean_opt_ir = sanitize_ir_for_riscv(original_optimized_ir)

    # Write the sanitized .ll files
    with open(f"{output_dir}/baseline_riscv.ll", "w") as f:
        f.write(clean_base_ir)
    with open(f"{output_dir}/optimized_riscv.ll", "w") as f:
        f.write(clean_opt_ir)

    try:
        # Invoke llc on the sanitized files
        subprocess.run(["llc", "-march=riscv64", "-mcpu=generic-rv64", "-filetype=asm", f"{output_dir}/baseline_riscv.ll", "-o", f"{output_dir}/baseline.s"], check=True)
        subprocess.run(["llc", "-march=riscv64", "-mcpu=generic-rv64", "-filetype=asm", f"{output_dir}/optimized_riscv.ll", "-o", f"{output_dir}/optimized.s"], check=True)
        print(f"RISC-V assembly saved to '{output_dir}/'")
    except FileNotFoundError:
        print("[WARNING] 'llc' command not found.")
    except Exception as e:
        print(f"[WARNING] Assembly generation failed (validation continues): {e}")

    # --- 3. Compile and run (using the original .bc files) ---
    print("[INFO] Compiling and running to verify correctness...")
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
            print("SUCCESS: the optimized code produces an identical result to the original!")
            return True
        else:
            print("FAILURE: outputs differ! The optimization broke the program.")
            return False

    except FileNotFoundError:
        print("[WARNING] 'clang' not found. Cannot execute the code.")
        return None
    except Exception as e:
        print(f"[ERROR] During execution: {e}")
        return False
    finally:
        env.close()
