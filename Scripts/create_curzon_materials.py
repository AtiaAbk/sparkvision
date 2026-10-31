#!/usr/bin/env python3
import json
import subprocess

PARENT_MAT = "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
FOLDER_PATH = "/Game/SparkVision/Materials"

MATERIALS = [
    {
        "name": "MI_Curzon_Brick",
        "color": {"r": 0.52, "g": 0.15, "b": 0.10, "a": 1.0},
        "roughness": 0.78
    },
    {
        "name": "MI_Curzon_Brick_Aged",
        "color": {"r": 0.40, "g": 0.12, "b": 0.08, "a": 1.0},
        "roughness": 0.85
    },
    {
        "name": "MI_Curzon_WhiteTrim",
        "color": {"r": 0.90, "g": 0.86, "b": 0.80, "a": 1.0},
        "roughness": 0.55
    },
    {
        "name": "MI_Curzon_Terracotta",
        "color": {"r": 0.62, "g": 0.22, "b": 0.12, "a": 1.0},
        "roughness": 0.70
    },
    {
        "name": "MI_Curzon_StonePaving",
        "color": {"r": 0.68, "g": 0.65, "b": 0.60, "a": 1.0},
        "roughness": 0.65
    },
    {
        "name": "MI_Curzon_WindowRecess",
        "color": {"r": 0.06, "g": 0.07, "b": 0.08, "a": 1.0},
        "roughness": 0.95
    },
    {
        "name": "MI_Curzon_RoofTile",
        "color": {"r": 0.35, "g": 0.14, "b": 0.10, "a": 1.0},
        "roughness": 0.80
    },
    {
        "name": "MI_Curzon_CastIron",
        "color": {"r": 0.10, "g": 0.10, "b": 0.12, "a": 1.0},
        "roughness": 0.40
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("Configuring Material Instances in Unreal Engine...")
for m in MATERIALS:
    mat_name = m["name"]
    ref_path = f"{FOLDER_PATH}/{mat_name}.{mat_name}"
    
    # Check if exists, else create
    try:
        exists_res = run_mcp("editor_toolset.toolsets.asset.AssetTools", "exists", {"path": ref_path})
        if not exists_res.get("returnValue"):
            print(f"Creating {mat_name}...")
            run_mcp("editor_toolset.toolsets.material_instance.MaterialInstanceTools", "create", {
                "folder_path": FOLDER_PATH,
                "asset_name": mat_name,
                "parent": {"refPath": PARENT_MAT}
            })
    except Exception as e:
        print(f"Notice during create {mat_name}: {e}")

    # Set parameters
    try:
        run_mcp("editor_toolset.toolsets.material_instance.MaterialInstanceTools", "set_vector_parameter", {
            "instance": {"refPath": ref_path},
            "name": "Color",
            "value": m["color"]
        })
        run_mcp("editor_toolset.toolsets.material_instance.MaterialInstanceTools", "set_scalar_parameter", {
            "instance": {"refPath": ref_path},
            "name": "Roughness",
            "value": m["roughness"]
        })
        print(f"Configured {mat_name}: Color={m['color']}, Roughness={m['roughness']}")
    except Exception as e:
        print(f"Error setting params for {mat_name}: {e}")

print("Material system configuration complete!")
