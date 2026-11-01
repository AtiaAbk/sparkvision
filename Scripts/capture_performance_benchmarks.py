#!/usr/bin/env python3
"""
SparkVision — Performance Benchmark and Visual Capture Suite
Captures high-resolution benchmark frames and measures frame times across:
  P01: Curzon Hall Hero Elevation
  P02: Living Campus Greenery & Pond
  P03: Full Campus Panoramic Vista
  P04: Third-Person Gameplay Traversal
  P05: Interactive Gameplay Systems
"""

import sys
import os
import json
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

BENCHMARKS = [
    {
        "id": "P01",
        "name": "Curzon Hall Hero Elevation",
        "cam_loc": {"x": -6600.0, "y": 0.0, "z": 380.0},
        "cam_rot": {"pitch": 6.0, "yaw": 0.0, "roll": 0.0},
        "filename": "P01_Curzon_Hero.png",
        "desc": "Front colonial facade, Indo-Saracenic arches, entrance promenade"
    },
    {
        "id": "P02",
        "name": "Living Campus Greenery & Pond",
        "cam_loc": {"x": 1800.0, "y": -400.0, "z": 250.0},
        "cam_rot": {"pitch": -8.0, "yaw": 15.0, "roll": 0.0},
        "filename": "P02_Living_Campus_Greenery.png",
        "desc": "Curzon pond ecology, riparian trees, water lilies, reeds"
    },
    {
        "id": "P03",
        "name": "Full Campus Panoramic Vista",
        "cam_loc": {"x": 56000.0, "y": -86500.0, "z": 500.0},
        "cam_rot": {"pitch": -5.0, "yaw": 15.0, "roll": 0.0},
        "filename": "P03_Full_Campus_Vista.png",
        "desc": "The Mall open field, Arts Faculty, distant skyline"
    },
    {
        "id": "P04",
        "name": "Third-Person Gameplay Traversal",
        "cam_loc": {"x": -3300.0, "y": 0.0, "z": 160.0},
        "cam_rot": {"pitch": -5.0, "yaw": 0.0, "roll": 0.0},
        "filename": "P04_ThirdPerson_Gameplay.png",
        "desc": "Active player pawn locomotion at Curzon South Portico landing"
    },
    {
        "id": "P05",
        "name": "Interactive Gameplay Systems",
        "cam_loc": {"x": 58900.0, "y": -63600.0, "z": 180.0},
        "cam_rot": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "filename": "P05_Interactive_Gameplay.png",
        "desc": "TSC Raju Memorial, Student NPC Fahim, Archive Terminal 03, active HUD"
    }
]

def capture_suite(target_dir):
    os.makedirs(target_dir, exist_ok=True)
    print(f"Executing Performance Benchmark Suite -> Target: {target_dir}")
    print("=" * 70)
    
    results = []
    
    for b in BENCHMARKS:
        b_id = b["id"]
        b_name = b["name"]
        print(f"\n[Benchmark {b_id}] — {b_name}...")
        
        # Warmup and measurement
        t_start = time.time()
        res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": b["cam_loc"],
                "rotation": b["cam_rot"],
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": {
                "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
                "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
            },
            "bShowUI": False
        })
        t_elapsed = time.time() - t_start
        
        ret = res.get("returnValue", {})
        img_data = ret.get("image", {}).get("data", "")
        file_path = os.path.join(target_dir, b["filename"])
        
        file_size = 0
        if img_data:
            raw_bytes = base64.b64decode(img_data)
            with open(file_path, "wb") as f:
                f.write(raw_bytes)
            file_size = len(raw_bytes)
            print(f"  Frame captured: {b['filename']} ({file_size:,} bytes) in {t_elapsed:.2f}s")
        else:
            print(f"  Warning: No image data returned for {b_id}")
            
        results.append({
            "id": b_id,
            "name": b_name,
            "description": b["desc"],
            "elapsed_s": round(t_elapsed, 3),
            "file": b["filename"],
            "size_bytes": file_size
        })
        
    summary_path = os.path.join(target_dir, "benchmark_metrics.json")
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "=" * 70)
    print(f"Benchmark Suite Completed. Metrics written to {summary_path}")
    print("=" * 70)
    return results

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    target = "Documentation/Performance/Visual_Baseline" if mode == "baseline" else "Documentation/Performance/Visual_After"
    capture_suite(target)
