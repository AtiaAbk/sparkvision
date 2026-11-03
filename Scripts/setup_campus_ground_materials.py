#!/usr/bin/env python3
"""
Create Professional Campus Ground Materials Suite for SparkVision:
1. MI_Ground_Lawn_Maintained (Curzon parterres, TSC lawn, Mall lawn)
2. MI_Ground_Turf_Natural (Open verges, campus borders)
3. MI_Ground_TreeBase_Loam (Beneath Banyan, Krishnachura, Raintree canopies)
4. MI_Ground_Garden_Soil (Inside raised flowerbeds and parterres)
5. MI_Campus_Grass_Blades (Two-sided foliage material for actual grass blade meshes)
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MASTER_PBR = "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"
MASTER_FOLIAGE = "/Game/SparkVision/Materials/M_Master_NaturalFoliage.M_Master_NaturalFoliage"
MAT_FOLDER = "/Game/SparkVision/Materials"
TEX_FOLDER = "/Game/SparkVision/Textures"

DIFFUSE_GRASS = f"{TEX_FOLDER}/T_Ground_Grass_D.T_Ground_Grass_D"
NORMAL_GRASS = f"{TEX_FOLDER}/T_Ground_Grass_N.T_Ground_Grass_N"

DIFFUSE_BLADES = f"{TEX_FOLDER}/T_Campus_Grass_Blades_D.T_Campus_Grass_Blades_D"
NORMAL_BLADES = f"{TEX_FOLDER}/T_Campus_Grass_Blades_N.T_Campus_Grass_Blades_N"

GROUND_MATERIALS = [
    {
        "name": "MI_Ground_Lawn_Maintained",
        "parent": MASTER_PBR,
        "diffuse": DIFFUSE_GRASS,
        "normal": NORMAL_GRASS,
        "roughness": 0.68,
        "tint": {"r": 0.085, "g": 0.225, "b": 0.060, "a": 1.0},
        "desc": "Maintained Bermuda grass lawn (Curzon Front Lawn, TSC Lawn, Mall Quad)"
    },
    {
        "name": "MI_Ground_Turf_Natural",
        "parent": MASTER_PBR,
        "diffuse": DIFFUSE_GRASS,
        "normal": NORMAL_GRASS,
        "roughness": 0.78,
        "tint": {"r": 0.065, "g": 0.170, "b": 0.045, "a": 1.0},
        "desc": "Natural mixed carpet grass (Roadside verges, campus peripheral meadows)"
    },
    {
        "name": "MI_Ground_TreeBase_Loam",
        "parent": MASTER_PBR,
        "diffuse": DIFFUSE_GRASS,
        "normal": NORMAL_GRASS,
        "roughness": 0.88,
        "tint": {"r": 0.090, "g": 0.065, "b": 0.045, "a": 1.0},
        "desc": "Dark moist deltaic loam (Tree root zones, Banyan/Raintree shaded bases)"
    },
    {
        "name": "MI_Ground_Garden_Soil",
        "parent": MASTER_PBR,
        "diffuse": DIFFUSE_GRASS,
        "normal": NORMAL_GRASS,
        "roughness": 0.82,
        "tint": {"r": 0.120, "g": 0.080, "b": 0.050, "a": 1.0},
        "desc": "Cultivated garden topsoil (Circular flowerbeds, ornamental parterres)"
    }
]

def main():
    print("=" * 70)
    print("CREATING PROFESSIONAL CAMPUS GROUND MATERIALS SYSTEM")
    print("=" * 70)

    # 1. Create Ground Material Instances
    for mat_def in GROUND_MATERIALS:
        name = mat_def["name"]
        print(f"\nConfiguring {name} ({mat_def['desc']})...")
        mi_ref = f"{MAT_FOLDER}/{name}.{name}"
        
        try:
            invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "folder_path": MAT_FOLDER,
                "asset_name": name,
                "parent": {"refPath": mat_def["parent"]}
            })
            print(f"  ✓ Created asset {name}")
        except Exception as e:
            print(f"  Asset note: {e}")

        # Set parent explicitly
        try:
            invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "parent": {"refPath": mat_def["parent"]}
            })
        except Exception:
            pass

        # Texture parameters
        invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "BaseColor_Texture",
            "value": {"refPath": mat_def["diffuse"]}
        })
        invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "Normal_Texture",
            "value": {"refPath": mat_def["normal"]}
        })

        # Roughness & Tint
        invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "Roughness",
            "value": mat_def["roughness"]
        })
        invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "Color",
            "value": mat_def["tint"]
        })
        print(f"  ✓ Parameters set: Roughness={mat_def['roughness']}, Tint={mat_def['tint']}")

    # 2. Update existing MI_Ground_Grass to have the authentic lawn calibration
    print("\nUpdating baseline MI_Ground_Grass...")
    invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": f"{MAT_FOLDER}/MI_Ground_Grass.MI_Ground_Grass"},
        "name": "Roughness",
        "value": 0.72
    })
    invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": f"{MAT_FOLDER}/MI_Ground_Grass.MI_Ground_Grass"},
        "name": "Color",
        "value": {"r": 0.080, "g": 0.210, "b": 0.055, "a": 1.0}
    })
    print("  ✓ Updated MI_Ground_Grass")

    # 3. Configure Grass Blades Two-Sided Foliage Material Instance
    print("\nConfiguring MI_Campus_Grass_Blades...")
    blades_mi = f"{MAT_FOLDER}/MI_Campus_Grass_Blades.MI_Campus_Grass_Blades"
    invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": blades_mi},
        "parent": {"refPath": MASTER_FOLIAGE}
    })
    invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": blades_mi},
        "name": "BaseColor_Texture",
        "value": {"refPath": DIFFUSE_BLADES}
    })
    invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": blades_mi},
        "name": "Normal_Texture",
        "value": {"refPath": NORMAL_BLADES}
    })
    invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": blades_mi},
        "name": "Roughness",
        "value": 0.70
    })
    invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
        "instance": {"refPath": blades_mi},
        "name": "SubsurfaceColor",
        "value": {"r": 0.18, "g": 0.45, "b": 0.12, "a": 1.0}
    })
    print("  ✓ MI_Campus_Grass_Blades configured with Diffuse, Normal, Roughness, and SubsurfaceColor")

    # 4. Save Assets
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": [
            f"{MAT_FOLDER}/MI_Ground_Lawn_Maintained",
            f"{MAT_FOLDER}/MI_Ground_Turf_Natural",
            f"{MAT_FOLDER}/MI_Ground_TreeBase_Loam",
            f"{MAT_FOLDER}/MI_Ground_Garden_Soil",
            f"{MAT_FOLDER}/MI_Ground_Grass",
            f"{MAT_FOLDER}/MI_Campus_Grass_Blades",
            f"{TEX_FOLDER}/T_Campus_Grass_Blades_D",
            f"{TEX_FOLDER}/T_Campus_Grass_Blades_N"
        ]
    })
    print("\n✅ All ground and grass material assets configured and saved!")

if __name__ == "__main__":
    main()
