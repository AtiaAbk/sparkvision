#!/usr/bin/env python3
import json
import subprocess

PARENT_MAT = "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
FOLDER_PATH = "/Game/SparkVision/Materials"

ENV_MATERIALS = [
    {"name": "MI_Curzon_Sandstone", "color": {"r": 0.65, "g": 0.48, "b": 0.35, "a": 1.0}, "roughness": 0.75},
    {"name": "MI_Curzon_Brass", "color": {"r": 0.72, "g": 0.56, "b": 0.22, "a": 1.0}, "roughness": 0.35},
    {"name": "MI_Curzon_Tiles", "color": {"r": 0.48, "g": 0.19, "b": 0.14, "a": 1.0}, "roughness": 0.55},
    {"name": "MI_Foliage_Banyan_Leaf", "color": {"r": 0.08, "g": 0.22, "b": 0.06, "a": 1.0}, "roughness": 0.55},
    {"name": "MI_Foliage_Raintree_Leaf", "color": {"r": 0.11, "g": 0.28, "b": 0.08, "a": 1.0}, "roughness": 0.60},
    {"name": "MI_Foliage_Krishnachura_Red", "color": {"r": 0.82, "g": 0.16, "b": 0.08, "a": 1.0}, "roughness": 0.45},
    {"name": "MI_Foliage_Radhachura_Yellow", "color": {"r": 0.86, "g": 0.72, "b": 0.12, "a": 1.0}, "roughness": 0.50},
    {"name": "MI_Foliage_Jarul_Lilac", "color": {"r": 0.58, "g": 0.28, "b": 0.65, "a": 1.0}, "roughness": 0.50},
    {"name": "MI_Foliage_Neem_Green", "color": {"r": 0.16, "g": 0.38, "b": 0.12, "a": 1.0}, "roughness": 0.60},
    {"name": "MI_Bark_Tree", "color": {"r": 0.22, "g": 0.17, "b": 0.13, "a": 1.0}, "roughness": 0.85},
    {"name": "MI_Bark_Palm", "color": {"r": 0.35, "g": 0.32, "b": 0.28, "a": 1.0}, "roughness": 0.80},
    {"name": "MI_Foliage_PalmFrond", "color": {"r": 0.12, "g": 0.32, "b": 0.09, "a": 1.0}, "roughness": 0.50},
    {"name": "MI_Stem_BambooGold", "color": {"r": 0.75, "g": 0.68, "b": 0.22, "a": 1.0}, "roughness": 0.45},
    {"name": "MI_Foliage_BambooLeaf", "color": {"r": 0.16, "g": 0.35, "b": 0.10, "a": 1.0}, "roughness": 0.55},
    {"name": "MI_Flower_Shapla", "color": {"r": 0.92, "g": 0.90, "b": 0.95, "a": 1.0}, "roughness": 0.30},
    {"name": "MI_Foliage_LilyPad", "color": {"r": 0.08, "g": 0.28, "b": 0.12, "a": 1.0}, "roughness": 0.35},
    {"name": "MI_Foliage_KashfulWhite", "color": {"r": 0.94, "g": 0.94, "b": 0.92, "a": 1.0}, "roughness": 0.75},
    {"name": "MI_Stem_ReedGreen", "color": {"r": 0.18, "g": 0.32, "b": 0.10, "a": 1.0}, "roughness": 0.60},
    {"name": "MI_Decal_KrishnachuraPetals", "color": {"r": 0.85, "g": 0.15, "b": 0.08, "a": 1.0}, "roughness": 0.60},
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("[Materials] Creating Environment Material Instances...")
for m in ENV_MATERIALS:
    mat_name = m["name"]
    ref_path = f"{FOLDER_PATH}/{mat_name}.{mat_name}"
    
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
        print(f"  Configured {mat_name}")
    except Exception as e:
        print(f"  Error setting params for {mat_name}: {e}")

print("[Materials] Environment material instances successfully created!")
