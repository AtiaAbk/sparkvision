import sys
import os
import time
import json
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

def get_system_memory():
    # vm_stat
    vm_out = subprocess.check_output(["vm_stat"]).decode("utf-8")
    vm_lines = {line.split(":")[0].strip(): line.split(":")[1].strip().rstrip(".") for line in vm_out.splitlines() if ":" in line}
    
    # swapusage
    swap_out = subprocess.check_output(["sysctl", "vm.swapusage"]).decode("utf-8")
    
    # ps for UnrealEditor
    ps_out = subprocess.check_output(["ps", "-A", "-o", "pid,rss,%mem,command"]).decode("utf-8")
    ue_procs = [line for line in ps_out.splitlines() if "Unreal" in line and not "grep" in line and not "measure_memory" in line]
    
    return {
        "vm_stat": vm_lines,
        "swap": swap_out.strip(),
        "unreal_processes": ue_procs
    }

def run():
    print("=== MEASURING SITUATION A: EDITOR OPENED WITHOUT PLAY ===")
    state_a = get_system_memory()
    print("Unreal Processes (A):", state_a["unreal_processes"])
    print("Swap (A):", state_a["swap"])
    
    print("\n=== STARTING PIE FOR SITUATION B: GAMEPLAY INSIDE EDITOR ===")
    mcp_client.invoke_tool("StartPIE", "EditorToolset.EditorAppToolset", {
        "options": {"bSimulate": False, "playMode": "PlayMode_InViewPort", "warmupSeconds": 2.0}
    })
    time.sleep(3.0)
    
    # Warmup and take gameplay camera view
    print("Capturing active gameplay view...")
    mcp_client.invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
        "captureTransform": {
            "location": {"x": -3300.0, "y": 0.0, "z": 160.0},
            "rotation": {"pitch": -5.0, "yaw": 0.0, "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        },
        "annotations": {
            "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
            "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
        },
        "bShowUI": False
    })
    
    state_b = get_system_memory()
    print("Unreal Processes (B):", state_b["unreal_processes"])
    print("Swap (B):", state_b["swap"])
    
    print("Stopping PIE...")
    mcp_client.invoke_tool("StopPIE", "EditorToolset.EditorAppToolset", {})
    
    # Save raw baseline
    out_dir = "Documentation/Performance/Diagnostics"
    os.makedirs(out_dir, exist_ok=True)
    baseline_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "situation_a_editor_idle": state_a,
        "situation_b_pie_gameplay": state_b
    }
    with open(f"{out_dir}/memory_baseline_raw.json", "w") as f:
        json.dump(baseline_data, f, indent=2)
    print(f"\nSaved raw diagnostic capture to {out_dir}/memory_baseline_raw.json")

if __name__ == "__main__":
    run()
