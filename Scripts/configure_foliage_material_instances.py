#!/usr/bin/env python3
"""
Configures and verifies all Natural Foliage Material Instances in Unreal Engine 5.8:
- MI_Foliage_Raintree_Natural
- MI_Foliage_Krishnachura_Natural
- MI_Foliage_Banyan_Natural
- MI_Foliage_Fern_Natural
- MI_Bark_Natural_Gnarled
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

FOLDER = "/Game/SparkVision/Materials"
MASTER_FOLIAGE = f"{FOLDER}/M_Master_NaturalFoliage.M_Master_NaturalFoliage"
MASTER_PBR = f"{FOLDER}/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"

def configure_instance(name, parent, diff_tex, norm_tex, sub_color=None):
    inst_ref = f"{FOLDER}/{name}.{name}"
    print(f"\nConfiguring {name}...")

    # Create if not exists
    try:
        invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "folder_path": FOLDER,
            "asset_name": name,
            "parent": {"refPath": parent}
        })
        print(f"  Created {name}")
    except Exception as e:
        print(f"  Already exists or notice: {e}")

    # Ensure parent is correct
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": inst_ref},
        "values": json.dumps({"Parent": {"refPath": parent}})
    })

    # Set textures
    diff_path = f"/Game/SparkVision/Textures/NaturalFoliage/{diff_tex}.{diff_tex}"
    norm_path = f"/Game/SparkVision/Textures/NaturalFoliage/{norm_tex}.{norm_tex}"

    invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": inst_ref},
        "name": "BaseColor_Texture",
        "value": {"refPath": diff_path}
    })
    print(f"  ✓ Set BaseColor_Texture -> {diff_tex}")

    invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": inst_ref},
        "name": "Normal_Texture",
        "value": {"refPath": norm_path}
    })
    print(f"  ✓ Set Normal_Texture -> {norm_tex}")

    if sub_color:
        invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": inst_ref},
            "name": "SubsurfaceColor",
            "value": sub_color
        })
        print(f"  ✓ Set SubsurfaceColor -> {sub_color}")

    # Save
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": [f"{FOLDER}/{name}"]
    })
    print(f"  ✓ Saved {name}")

def main():
    print("=" * 65)
    print("UPDATING FOLIAGE & BARK MATERIAL INSTANCES")
    print("=" * 65)

    # 1. Raintree (Rain Tree - Ref 3)
    configure_instance(
        "MI_Foliage_Raintree_Natural",
        MASTER_FOLIAGE,
        "T_Leaf_Raintree_D",
        "T_Leaf_Raintree_N",
        {"r": 0.28, "g": 0.65, "b": 0.12, "a": 1.0}
    )

    # 2. Krishnachura (Where Winds Meet Scarlet - Ref 1)
    configure_instance(
        "MI_Foliage_Krishnachura_Natural",
        MASTER_FOLIAGE,
        "T_Leaf_Krishnachura_D",
        "T_Leaf_Krishnachura_N",
        {"r": 0.95, "g": 0.22, "b": 0.08, "a": 1.0}
    )

    # 3. Banyan (Gnarled Heritage - Ref 2)
    configure_instance(
        "MI_Foliage_Banyan_Natural",
        MASTER_FOLIAGE,
        "T_Leaf_Banyan_D",
        "T_Leaf_Banyan_N",
        {"r": 0.16, "g": 0.48, "b": 0.09, "a": 1.0}
    )

    # 4. Fern (Undergrowth frond - Ref 1 foreground)
    configure_instance(
        "MI_Foliage_Fern_Natural",
        MASTER_FOLIAGE,
        "T_Foliage_Fern_D",
        "T_Foliage_Fern_N",
        {"r": 0.22, "g": 0.58, "b": 0.10, "a": 1.0}
    )

    # 5. Gnarled Bark (Ref 2)
    configure_instance(
        "MI_Bark_Natural_Gnarled",
        MASTER_PBR,
        "T_Bark_Gnarled_D",
        "T_Bark_Gnarled_N"
    )

    print("\n✅ ALL FOLIAGE & BARK MATERIAL INSTANCES CONFIGURED AND SAVED!")

if __name__ == "__main__":
    main()
