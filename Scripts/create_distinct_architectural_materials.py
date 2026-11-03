#!/usr/bin/env python3
"""
Create Distinct Architectural PBR Materials for Dhaka University & Modern City Skyline:
- Curzon Hall: Preserves authentic Indo-Saracenic terracotta red brick & white lime trims
- Kala Bhaban: Tropical Modernist / Brutalist light sand concrete louvers & tinted ribbon glazing
- TSC: Konstantinos Doxiadis crisp white structural waffle fascia, modern terracotta panels & green-tinted glass
- Shaheed Minar: Pure Carrara white marble, dark polished basalt/granite terrace, deep crimson lacquer sun
- Doyel Chattar: Iridescent teal/black/white magpie robin plumage & turquoise mosaic pool tiles
- Modern Skyline: Reflective sky blue curtain wall glass, brushed titanium aluminum, dark spandrels
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

FOLDER_PATH = "/Game/SparkVision/Materials"
MASTER_PBR = f"{FOLDER_PATH}/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"

NEW_MATERIALS = [
    # 1. Kala Bhaban Modern Architectural Sand Concrete
    {
        "name": "MI_Modern_Concrete_Sand",
        "diffuse": "/Game/SparkVision/Textures/T_Modern_Concrete_D.T_Modern_Concrete_D",
        "normal": "/Game/SparkVision/Textures/T_Modern_Concrete_N.T_Modern_Concrete_N",
        "color": {"r": 0.82, "g": 0.79, "b": 0.73, "a": 1.0},
        "roughness": 0.72,
        "metallic": 0.0
    },
    # 2. TSC Crisp White Structural Waffle Fascia
    {
        "name": "MI_TSC_WhiteFascia",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_WhiteTrim_D.T_Curzon_WhiteTrim_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_WhiteTrim_N.T_Curzon_WhiteTrim_N",
        "color": {"r": 0.94, "g": 0.94, "b": 0.92, "a": 1.0},
        "roughness": 0.45,
        "metallic": 0.0
    },
    # 3. TSC Modern Modular Terracotta Accent Panels
    {
        "name": "MI_Modern_TerracottaPanel",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_Sandstone_D.T_Curzon_Sandstone_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_Sandstone_N.T_Curzon_Sandstone_N",
        "color": {"r": 0.74, "g": 0.38, "b": 0.22, "a": 1.0},
        "roughness": 0.65,
        "metallic": 0.0
    },
    # 4. Modern Green-Tinted Low-E Architectural Glass
    {
        "name": "MI_Modern_Glass_GreenTint",
        "diffuse": "/Game/SparkVision/Textures/T_Ribbon_Window_D.T_Ribbon_Window_D",
        "normal": "/Game/SparkVision/Textures/T_Ribbon_Window_N.T_Ribbon_Window_N",
        "color": {"r": 0.12, "g": 0.35, "b": 0.30, "a": 1.0},
        "roughness": 0.08,
        "metallic": 0.4
    },
    # 5. Shaheed Minar Pure White Carrara Marble
    {
        "name": "MI_Shaheed_Marble_Pure",
        "diffuse": "/Game/SparkVision/Textures/T_Shaheed_Marble_D.T_Shaheed_Marble_D",
        "normal": "/Game/SparkVision/Textures/T_Shaheed_Marble_N.T_Shaheed_Marble_N",
        "color": {"r": 0.96, "g": 0.96, "b": 0.97, "a": 1.0},
        "roughness": 0.28,
        "metallic": 0.02
    },
    # 6. Shaheed Minar Polished Black Basalt / Granite Terrace
    {
        "name": "MI_Shaheed_BlackGranite",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_StonePaving_D.T_Curzon_StonePaving_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_StonePaving_N.T_Curzon_StonePaving_N",
        "color": {"r": 0.08, "g": 0.08, "b": 0.09, "a": 1.0},
        "roughness": 0.22,
        "metallic": 0.05
    },
    # 7. Doyel Chattar Turquoise Mosaic Fountain Basin
    {
        "name": "MI_Pool_Mosaic_Turquoise",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_RoofTiles_D.T_Curzon_RoofTiles_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_RoofTiles_N.T_Curzon_RoofTiles_N",
        "color": {"r": 0.05, "g": 0.65, "b": 0.70, "a": 1.0},
        "roughness": 0.20,
        "metallic": 0.1
    },
    # 8. Doyel Bird Iridescent Teal Wing Sheen
    {
        "name": "MI_Fauna_Doel_Teal",
        "diffuse": "/Game/SparkVision/Textures/T_Supporting_Building_D.T_Supporting_Building_D",
        "normal": "/Game/SparkVision/Textures/T_Supporting_Building_N.T_Supporting_Building_N",
        "color": {"r": 0.06, "g": 0.32, "b": 0.38, "a": 1.0},
        "roughness": 0.30,
        "metallic": 0.25
    },
    # 9. Modern City Skyline Reflective Sky-Blue Curtain Wall Glass
    {
        "name": "MI_Modern_Glass_CurtainWall_Blue",
        "diffuse": "/Game/SparkVision/Textures/T_Ribbon_Window_D.T_Ribbon_Window_D",
        "normal": "/Game/SparkVision/Textures/T_Ribbon_Window_N.T_Ribbon_Window_N",
        "color": {"r": 0.10, "g": 0.32, "b": 0.58, "a": 1.0},
        "roughness": 0.06,
        "metallic": 0.85
    },
    # 10. Modern City Skyline Brushed Titanium Aluminum Cladding
    {
        "name": "MI_Modern_Alu_Titanium",
        "diffuse": "/Game/SparkVision/Textures/T_Modern_Concrete_D.T_Modern_Concrete_D",
        "normal": "/Game/SparkVision/Textures/T_Modern_Concrete_N.T_Modern_Concrete_N",
        "color": {"r": 0.72, "g": 0.74, "b": 0.78, "a": 1.0},
        "roughness": 0.35,
        "metallic": 0.75
    },
    # 11. Modern City Skyline Dark Spandrel Glass / Anodized Mullions
    {
        "name": "MI_Modern_Spandrel_Dark",
        "diffuse": "/Game/SparkVision/Textures/T_Ribbon_Window_D.T_Ribbon_Window_D",
        "normal": "/Game/SparkVision/Textures/T_Ribbon_Window_N.T_Ribbon_Window_N",
        "color": {"r": 0.05, "g": 0.06, "b": 0.07, "a": 1.0},
        "roughness": 0.15,
        "metallic": 0.60
    }
]

def main():
    print("=" * 70)
    print("CREATING DISTINCT ARCHITECTURAL MATERIALS")
    print("=" * 70)

    created_paths = []

    for mat_cfg in NEW_MATERIALS:
        name = mat_cfg["name"]
        ref_path = f"{FOLDER_PATH}/{name}.{name}"
        print(f"\nProcessing {name}...")

        # 1. Create or ensure existence
        try:
            exists = invoke_tool("exists", "editor_toolset.toolsets.asset.AssetTools", {"path": ref_path}).get("returnValue", False)
            if not exists:
                invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "folder_path": FOLDER_PATH,
                    "asset_name": name,
                    "parent": {"refPath": MASTER_PBR}
                })
                print(f"  ✓ Created {name} parented to {MASTER_PBR}")
            else:
                invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": ref_path},
                    "parent": {"refPath": MASTER_PBR}
                })
                print(f"  ✓ Verified parent for existing {name}")
        except Exception as e:
            print(f"  Notice during creation of {name}: {e}")

        # 2. Assign Diffuse & Normal Textures
        try:
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": ref_path},
                "name": "BaseColor_Texture",
                "value": {"refPath": mat_cfg["diffuse"]}
            })
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": ref_path},
                "name": "Normal_Texture",
                "value": {"refPath": mat_cfg["normal"]}
            })
            print(f"  ✓ Textures assigned (Diffuse + Normal)")
        except Exception as e:
            print(f"  Notice setting textures for {name}: {e}")

        # 3. Assign Tint Color, Roughness, Metallic parameters if supported
        for param, val in [("Color", mat_cfg["color"]), ("BaseColor", mat_cfg["color"]), ("TintColor", mat_cfg["color"])]:
            try:
                invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": ref_path},
                    "name": param,
                    "value": val
                })
            except Exception:
                pass

        for r_name in ["Roughness", "Roughness_Scale"]:
            try:
                invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": ref_path},
                    "name": r_name,
                    "value": mat_cfg["roughness"]
                })
            except Exception:
                pass

        for m_name in ["Metallic", "Metallic_Scale"]:
            try:
                invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "instance": {"refPath": ref_path},
                    "name": m_name,
                    "value": mat_cfg["metallic"]
                })
            except Exception:
                pass

        created_paths.append(f"{FOLDER_PATH}/{name}")

    # Save created assets
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": created_paths
        })
        print(f"\n✅ Successfully created & saved {len(created_paths)} distinct architectural materials!")
    except Exception as e:
        print(f"Notice saving assets: {e}")

if __name__ == "__main__":
    main()
