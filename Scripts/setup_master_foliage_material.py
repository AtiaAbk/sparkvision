#!/usr/bin/env python3
"""
Sets up and validates M_Master_NaturalFoliage in Unreal Engine 5.8:
- BlendMode: BLEND_Masked
- TwoSided: True
- ShadingModel: MSM_TwoSidedFoliage
- OpacityMaskClipValue: 0.33
- BaseColor_Texture (RGB -> MP_BaseColor, A -> MP_OpacityMask)
- Normal_Texture (RGB -> MP_Normal)
- SubsurfaceColor (RGB -> MP_SubsurfaceColor)
- Roughness (Scalar -> MP_Roughness)
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

FOLDER = "/Game/SparkVision/Materials"
MAT_NAME = "M_Master_NaturalFoliage"
MAT_REF = f"{FOLDER}/{MAT_NAME}.{MAT_NAME}"

def main():
    print("=" * 60)
    print("CONFIGURING M_MASTER_NATURALFOLIAGE")
    print("=" * 60)

    # 1. Ensure material exists
    try:
        invoke_tool("create_material", "editor_toolset.toolsets.material.MaterialTools", {
            "folder_path": FOLDER,
            "asset_name": MAT_NAME
        })
    except Exception as e:
        print(f"Material notice: {e}")

    # 2. Configure material settings
    props = {
        "BlendMode": "BLEND_Masked",
        "TwoSided": True,
        "ShadingModel": "MSM_TwoSidedFoliage",
        "OpacityMaskClipValue": 0.33
    }
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": MAT_REF},
        "values": json.dumps(props)
    })
    print("✓ Set BlendMode, TwoSided, ShadingModel, OpacityMaskClipValue")

    # 3. List current expressions
    exprs_res = invoke_tool("get_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "material_or_function": {"refPath": MAT_REF}
    }).get("returnValue", [])

    print(f"Current expressions count: {len(exprs_res)}")

    # We will identify or create:
    # 1) BaseColor_Texture (TextureSampleParameter2D)
    # 2) Normal_Texture (TextureSampleParameter2D)
    # 3) SubsurfaceColor (VectorParameter)
    # 4) Roughness (ScalarParameter)
    
    tex_base_ref = None
    tex_norm_ref = None
    sub_color_ref = None
    rough_ref = None

    for ex in exprs_res:
        ref = ex["refPath"]
        try:
            p = invoke_tool("get_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": ref},
                "properties": ["ParameterName"]
            })
            pname = json.loads(p.get("returnValue", "{}")).get("ParameterName", "")
            if pname == "BaseColor_Texture":
                tex_base_ref = ref
            elif pname == "Normal_Texture":
                tex_norm_ref = ref
            elif pname == "SubsurfaceColor":
                sub_color_ref = ref
            elif pname == "Roughness":
                rough_ref = ref
        except Exception:
            pass

    if not tex_base_ref:
        print("Adding BaseColor_Texture parameter...")
        tex_base_ref = invoke_tool("add_expression", "editor_toolset.toolsets.material.MaterialTools", {
            "material_or_function": {"refPath": MAT_REF},
            "expression_class": {"refPath": "/Script/Engine.MaterialExpressionTextureSampleParameter2D"},
            "x": -500, "y": -100
        })["returnValue"]["refPath"]
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": tex_base_ref},
            "values": json.dumps({
                "ParameterName": "BaseColor_Texture",
                "Texture": {"refPath": "/Game/SparkVision/Textures/NaturalFoliage/T_Leaf_Raintree_D.T_Leaf_Raintree_D"}
            })
        })

    if not tex_norm_ref:
        print("Adding Normal_Texture parameter...")
        tex_norm_ref = invoke_tool("add_expression", "editor_toolset.toolsets.material.MaterialTools", {
            "material_or_function": {"refPath": MAT_REF},
            "expression_class": {"refPath": "/Script/Engine.MaterialExpressionTextureSampleParameter2D"},
            "x": -500, "y": 250
        })["returnValue"]["refPath"]
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": tex_norm_ref},
            "values": json.dumps({
                "ParameterName": "Normal_Texture",
                "Texture": {"refPath": "/Game/SparkVision/Textures/NaturalFoliage/T_Leaf_Raintree_N.T_Leaf_Raintree_N"},
                "SamplerType": "SAMPLERTYPE_Normal"
            })
        })

    if not sub_color_ref:
        print("Adding SubsurfaceColor parameter...")
        sub_color_ref = invoke_tool("add_expression", "editor_toolset.toolsets.material.MaterialTools", {
            "material_or_function": {"refPath": MAT_REF},
            "expression_class": {"refPath": "/Script/Engine.MaterialExpressionVectorParameter"},
            "x": -500, "y": 500
        })["returnValue"]["refPath"]
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": sub_color_ref},
            "values": json.dumps({
                "ParameterName": "SubsurfaceColor",
                "DefaultValue": {"r": 0.22, "g": 0.55, "b": 0.10, "a": 1.0}
            })
        })

    if not rough_ref:
        print("Adding Roughness parameter...")
        rough_ref = invoke_tool("add_expression", "editor_toolset.toolsets.material.MaterialTools", {
            "material_or_function": {"refPath": MAT_REF},
            "expression_class": {"refPath": "/Script/Engine.MaterialExpressionScalarParameter"},
            "x": -500, "y": 100
        })["returnValue"]["refPath"]
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": rough_ref},
            "values": json.dumps({
                "ParameterName": "Roughness",
                "DefaultValue": 0.45
            })
        })

    # Connect outputs
    # 1. BaseColor (RGB -> MP_BaseColor)
    print("Connecting BaseColor...")
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": tex_base_ref},
        "output_name": "RGB",
        "material_property": "MP_BaseColor"
    })

    # 2. OpacityMask (A -> MP_OpacityMask)
    print("Connecting OpacityMask...")
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": tex_base_ref},
        "output_name": "A",
        "material_property": "MP_OpacityMask"
    })

    # 3. Normal (RGB -> MP_Normal)
    print("Connecting Normal...")
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": tex_norm_ref},
        "output_name": "RGB",
        "material_property": "MP_Normal"
    })

    # 4. SubsurfaceColor (RGB -> MP_SubsurfaceColor)
    print("Connecting SubsurfaceColor...")
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": sub_color_ref},
        "output_name": "",
        "material_property": "MP_SubsurfaceColor"
    })

    # 5. Roughness -> MP_Roughness
    print("Connecting Roughness...")
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": rough_ref},
        "output_name": "",
        "material_property": "MP_Roughness"
    })

    # Recompile material
    print("Recompiling M_Master_NaturalFoliage...")
    invoke_tool("recompile", "editor_toolset.toolsets.material.MaterialTools", {
        "material_or_function": {"refPath": MAT_REF}
    })

    # Save asset
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": [FOLDER + "/" + MAT_NAME]
    })
    print("✅ M_Master_NaturalFoliage successfully configured and saved!")

if __name__ == "__main__":
    main()
