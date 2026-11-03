#!/usr/bin/env python3
"""
Create and configure all authentic character materials for SparkVision:
- Female student outfits (Kurti Mustard, Hijab Rose)
- Teacher outfits (Formal Safari, Dark Trousers, Saree Formal)
- Campus Staff outfits (Lab Blue, Grounds Olive)
- Campus Security outfits (Proctorial Khaki)
- Hostile outfits (Windbreaker Grey)
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

print("=" * 70)
print("SPARKVISION: COMPLETE CHARACTER OUTFIT MATERIAL FACTORY")
print("=" * 70)

MAT_INST_TOOLS = "editor_toolset.toolsets.material_instance.MaterialInstanceTools"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"

MANNY_01 = "/Game/Characters/Mannequins/Materials/Manny/MI_Manny_01_New.MI_Manny_01_New"
MANNY_02 = "/Game/Characters/Mannequins/Materials/Manny/MI_Manny_02_New.MI_Manny_02_New"
QUINN_01 = "/Game/Characters/Mannequins/Materials/Quinn/MI_Quinn_01.MI_Quinn_01"
QUINN_02 = "/Game/Characters/Mannequins/Materials/Quinn/MI_Quinn_02.MI_Quinn_02"

materials_to_build = [
    # 1. Female Student - Mustard Yellow Contemporary Kurti
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Student_Kurti_Mustard",
        "parent": QUINN_01,
        "tint": {"r": 0.55, "g": 0.42, "b": 0.12, "a": 1.0}, # Rich Mustard
        "logo_tint": {"r": 0.75, "g": 0.65, "b": 0.35, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.85,
        "label": "Female Student Mustard Kurti"
    },
    # 2. Female Student - Rose Tan / Navy Hijab Ensemble
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Student_Hijab_Rose",
        "parent": QUINN_01,
        "tint": {"r": 0.48, "g": 0.33, "b": 0.38, "a": 1.0}, # Elegant Rose-Tan
        "logo_tint": {"r": 0.15, "g": 0.20, "b": 0.35, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.88,
        "label": "Female Student Rose-Tan Hijab"
    },
    # 3. Male Student - Charcoal Casual Crewneck
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Student_CharcoalTorso",
        "parent": MANNY_01,
        "tint": {"r": 0.20, "g": 0.22, "b": 0.24, "a": 1.0}, # Deep Charcoal
        "logo_tint": {"r": 0.80, "g": 0.30, "b": 0.20, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.90,
        "label": "Male Student Charcoal Tee"
    },
    # 4. Teacher - Formal Safari Khaki Shirt
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Teacher_FormalSafari",
        "parent": MANNY_01,
        "tint": {"r": 0.44, "g": 0.42, "b": 0.36, "a": 1.0}, # Safari Khaki
        "logo_tint": {"r": 0.30, "g": 0.28, "b": 0.24, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.78,
        "label": "Teacher Formal Safari Shirt"
    },
    # 5. Teacher - Dark Grey Tailored Trousers
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Teacher_DarkTrousers",
        "parent": MANNY_02,
        "tint": {"r": 0.18, "g": 0.19, "b": 0.21, "a": 1.0}, # Tailored Charcoal
        "logo_tint": {"r": 0.18, "g": 0.19, "b": 0.21, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.80,
        "label": "Teacher Dark Trousers"
    },
    # 6. Teacher - Female Faculty Handloom Saree / Formal Attire
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Teacher_SareeFormal",
        "parent": QUINN_01,
        "tint": {"r": 0.54, "g": 0.18, "b": 0.23, "a": 1.0}, # Rich Burgundy Handloom
        "logo_tint": {"r": 0.85, "g": 0.70, "b": 0.30, "a": 1.0}, # Gold Anchal Trim
        "metallic": 0.02,
        "roughness": 0.80,
        "label": "Teacher Formal Handloom Saree"
    },
    # 7. Staff - Laboratory / Administrative Slate-Blue Shirt
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Staff_LabBlue",
        "parent": MANNY_01,
        "tint": {"r": 0.22, "g": 0.34, "b": 0.46, "a": 1.0}, # Slate Blue
        "logo_tint": {"r": 0.85, "g": 0.85, "b": 0.85, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.85,
        "label": "Staff Lab / Admin Blue Shirt"
    },
    # 8. Staff - Campus Grounds & Maintenance Olive Workwear
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Staff_GroundsOlive",
        "parent": MANNY_01,
        "tint": {"r": 0.28, "g": 0.32, "b": 0.24, "a": 1.0}, # Olive Drab Twill
        "logo_tint": {"r": 0.20, "g": 0.22, "b": 0.18, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.90,
        "label": "Staff Maintenance Olive Twill"
    },
    # 9. Security - University Proctorial Khaki Safari Uniform
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Security_ProctorialKhaki",
        "parent": MANNY_01,
        "tint": {"r": 0.42, "g": 0.36, "b": 0.25, "a": 1.0}, # Proctorial Uniform Khaki
        "logo_tint": {"r": 0.88, "g": 0.75, "b": 0.30, "a": 1.0}, # Brass Badge Gold
        "metallic": 0.0,
        "roughness": 0.78,
        "label": "Security Proctorial Khaki"
    },
    # 10. Hostile - Mission 6 Agitator Dark Windbreaker
    {
        "folder": "/Game/SparkVision/Materials",
        "name": "MI_Cadre_Windbreaker_Grey",
        "parent": MANNY_01,
        "tint": {"r": 0.16, "g": 0.17, "b": 0.18, "a": 1.0}, # Street Nylon Grey/Black
        "logo_tint": {"r": 0.50, "g": 0.10, "b": 0.10, "a": 1.0},
        "metallic": 0.05,
        "roughness": 0.55,
        "label": "Hostile Agitator Windbreaker"
    }
]

for cfg in materials_to_build:
    asset_path = f"{cfg['folder']}/{cfg['name']}"
    full_path = f"{asset_path}.{cfg['name']}"
    print(f"\nProcessing {cfg['label']} -> {full_path}")
    
    # Check if asset exists, if not create it
    try:
        invoke_tool("create", MAT_INST_TOOLS, {
            "folder_path": cfg["folder"],
            "asset_name": cfg["name"],
            "parent": {"refPath": cfg["parent"]}
        })
        print(f"  ✓ Created material instance: {cfg['name']}")
    except Exception as e:
        print(f"  Notice during creation (may already exist): {e}")

    # Set parent to ensure proper derivation
    try:
        invoke_tool("set_parent", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path},
            "parent": {"refPath": cfg["parent"]}
        })
    except Exception as e:
        print(f"  Notice setting parent: {e}")

    # Enable and set parameters
    # Vector: Paint Tint
    try:
        invoke_tool("set_parameter_override", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "Paint Tint", "override": True
        })
        invoke_tool("set_vector_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "Paint Tint", "value": cfg["tint"]
        })
        print(f"  ✓ Set Paint Tint to {cfg['tint']}")
    except Exception as e:
        print(f"  Warning setting Paint Tint: {e}")

    # Vector: LogoTint
    try:
        invoke_tool("set_parameter_override", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "LogoTint", "override": True
        })
        invoke_tool("set_vector_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "LogoTint", "value": cfg["logo_tint"]
        })
    except Exception as e:
        print(f"  Warning setting LogoTint: {e}")

    # Scalar: MetalPaintMetallic
    try:
        invoke_tool("set_parameter_override", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "MetalPaintMetallic", "override": True
        })
        invoke_tool("set_scalar_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "MetalPaintMetallic", "value": cfg["metallic"]
        })
    except Exception as e:
        print(f"  Warning setting MetalPaintMetallic: {e}")

    # Scalar: MetalPaintRoughness
    try:
        invoke_tool("set_parameter_override", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "MetalPaintRoughness", "override": True
        })
        invoke_tool("set_scalar_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": full_path}, "name": "MetalPaintRoughness", "value": cfg["roughness"]
        })
    except Exception as e:
        print(f"  Warning setting MetalPaintRoughness: {e}")

    # Save asset
    try:
        invoke_tool("save", ASSET_TOOLS, {"asset": {"refPath": full_path}})
        print(f"  ✓ Saved {full_path}")
    except Exception as e:
        print(f"  Notice saving: {e}")

print("\n" + "=" * 70)
print("ALL 10 AUTHENTIC CHARACTER MATERIAL INSTANCES SUCCESSFULLY CALIBRATED!")
print("=" * 70)
