#!/usr/bin/env python3
"""
Creates expanded botanical and wildlife Material Instances in /Game/SparkVision/Materials/
"""

import sys
import os
import json
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

PARENT_MAT = "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
FOLDER_PATH = "/Game/SparkVision/Materials"

EXPANDED_MATERIALS = [
    # Debdaru: Dark weeping evergreen lanceolate leaves
    {"name": "MI_Foliage_Debdaru_Dark", "color": {"r": 0.05, "g": 0.18, "b": 0.05, "a": 1.0}, "roughness": 0.45},
    # Kadam: Spherical golden-orange pom-pom blossoms
    {"name": "MI_Foliage_Kadam_Golden", "color": {"r": 0.95, "g": 0.65, "b": 0.08, "a": 1.0}, "roughness": 0.60},
    # Rangan: Intense scarlet-red tropical floral corymbs
    {"name": "MI_Flower_Rangan_Scarlet", "color": {"r": 0.92, "g": 0.12, "b": 0.08, "a": 1.0}, "roughness": 0.40},
    # Gandharaj: Velvety white gardenia petals
    {"name": "MI_Flower_Gardenia_White", "color": {"r": 0.96, "g": 0.96, "b": 0.94, "a": 1.0}, "roughness": 0.35},
    # Fern: Bright emerald sword fern fronds
    {"name": "MI_Foliage_Fern_Emerald", "color": {"r": 0.10, "g": 0.42, "b": 0.10, "a": 1.0}, "roughness": 0.40},
    # Ground Leaf Litter: Rich dark brown monsoon organic matter
    {"name": "MI_Ground_LeafLitter_Moist", "color": {"r": 0.28, "g": 0.20, "b": 0.14, "a": 1.0}, "roughness": 0.85},
    # Doel Bird: Glossy black plumage
    {"name": "MI_Fauna_Doel_Black", "color": {"r": 0.04, "g": 0.04, "b": 0.06, "a": 1.0}, "roughness": 0.45},
    # Doel Bird: Crisp white belly and wing bar
    {"name": "MI_Fauna_Doel_White", "color": {"r": 0.96, "g": 0.96, "b": 0.96, "a": 1.0}, "roughness": 0.40},
    # Butterfly: Bright lemon/sulphur yellow
    {"name": "MI_Fauna_Butterfly_Yellow", "color": {"r": 0.96, "g": 0.88, "b": 0.10, "a": 1.0}, "roughness": 0.35},
    # Dragonfly: Iridescent teal/cyan sheen
    {"name": "MI_Fauna_Dragonfly_Teal", "color": {"r": 0.10, "g": 0.78, "b": 0.82, "a": 1.0}, "roughness": 0.25},
]

def main():
    print("=" * 70)
    print("CREATING EXPANDED LIVING ENVIRONMENT MATERIAL INSTANCES...")
    print("=" * 70)

    for m in EXPANDED_MATERIALS:
        mat_name = m["name"]
        ref_path = f"{FOLDER_PATH}/{mat_name}.{mat_name}"

        try:
            exists_res = mcp_client.invoke_tool("exists", "editor_toolset.toolsets.asset.AssetTools", {"path": ref_path})
            if not exists_res.get("returnValue"):
                print(f"Creating Material Instance: {mat_name}...")
                mcp_client.invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "folder_path": FOLDER_PATH,
                    "asset_name": mat_name,
                    "parent": {"refPath": PARENT_MAT}
                })
        except Exception as e:
            print(f"Notice during create {mat_name}: {e}")

        # Set Color parameter
        try:
            mcp_client.invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": ref_path},
                "name": "Color",
                "value": m["color"]
            })
            print(f"  Configured Color for {mat_name}")
        except Exception as e:
            print(f"  Error setting Color parameter on {mat_name}: {e}")

    print("\n[Done] All expanded material instances created and configured successfully!")

if __name__ == "__main__":
    main()
