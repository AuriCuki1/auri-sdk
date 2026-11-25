#!/usr/bin/env python3
import sys
import os
import time

variables = {}
output_dir = "auri_outputs"

def resolve_vars(text):
    for k, v in variables.items():
        text = text.replace(f"${k}", str(v))
    return text

def run_auri_line(line, log_file):
    line = line.strip()
    if not line or line.startswith("~") or (line.startswith("[") and line.endswith("]")):
        return

    parts = line.split(" ")
    cmd = parts[0]

    if len(parts) >= 3 and parts[1] == "=":
        var_name = parts[0]
        raw_val = " ".join(parts[2:]).strip('"\'')
        variables[var_name] = int(raw_val) if raw_val.isdigit() else raw_val

    elif cmd in ("print", "say"):
        msg = resolve_vars(" ".join(parts[1:]).strip('"\''))
        print(msg)
        log_file.write(msg + "\n")

    elif cmd == "ask" and "->" in parts:
        arrow_idx = parts.index("->")
        question = resolve_vars(" ".join(parts[1:arrow_idx]).strip('"\''))
        var_name = parts[arrow_idx + 1]
        ans = input(question + " ")
        variables[var_name] = int(ans) if ans.isdigit() else ans
        log_file.write(f"{question} {ans}\n")

    elif cmd in ("add", "sub", "mul"):
        var_name, amount = parts[1], int(parts[2])
        if var_name in variables and isinstance(variables[var_name], int):
            if cmd == "add": variables[var_name] += amount
            elif cmd == "sub": variables[var_name] -= amount
            elif cmd == "mul": variables[var_name] *= amount

    elif cmd == "wait":
        time.sleep(float(parts[1]))

    elif cmd == "if" and len(parts) >= 5:
        var_name = parts[1]
        op = parts[2]
        val_str = parts[3]
        val = int(val_str) if val_str.isdigit() else val_str.strip('"\'')
        actual_val = variables.get(var_name, 0)
        
        condition_met = False
        if op == ">" and actual_val > val: condition_met = True
        elif op == "<" and actual_val < val: condition_met = True
        elif op == "==" and actual_val == val: condition_met = True
        
        if condition_met:
            sub_cmd = parts[4]
            if sub_cmd in ("print", "say"):
                msg = resolve_vars(" ".join(parts[5:]).strip('"\''))
                print(msg)
                log_file.write(msg + "\n")

def run_auri_file(filepath):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.basename(filepath)
    log_filename = os.path.join(output_dir, f"{base_name}_execution.log")
    
    with open(log_filename, "w") as log_file:
        log_file.write(f"Execution log for {base_name}\n")
        with open(filepath, "r") as f:
            for line in f:
                run_auri_line(line, log_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: auri <filename>")
        sys.exit(1)
    run_auri_file(sys.argv[1])
