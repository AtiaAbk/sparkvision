#!/usr/bin/env python3
"""
Build M_CurzonPond_Water: A AAA Single Layer Water Master Material in Unreal Engine 5.8
and create MI_CurzonPond_Water with authentic freshwater botanical pond calibration.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MAT_PATH = "/Game/SparkVision/Materials/M_CurzonPond_Water.M_CurzonPond_Water"
MAT_REF = {"refPath": MAT_PATH}
INST_FOLDER = "/Game/SparkVision/Materials"
INST_NAME = "MI_CurzonPond_Water"
INST_REF = {"refPath": f"{INST_FOLDER}/{INST_NAME}.{INST_NAME}"}
TEXTURE_NORMAL = "/Game/SparkVision/Textures/T_Water_Ripples_N.T_Water_Ripples_N"

def add_node(mat_ref, expr_class, x, y, props=None):
    node = invoke_tool("add_expression", "editor_toolset.toolsets.material.MaterialTools", {
        "material_or_function": mat_ref,
        "expression_class": {"refPath": expr_class},
        "x": x, "y": y
    }).get("returnValue")
    if props and node:
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": node,
            "values": json.dumps(props)
        })
    return node

def main():
    print("=" * 70)
    print("CONSTRUCTING MASTER WATER MATERIAL: M_CurzonPond_Water (SingleLayerWater)")
    print("=" * 70)

    # 1. Clean unused expressions in M_CurzonPond_Water
    invoke_tool("delete_unused_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "material": MAT_REF
    })

    # Disconnect all active outputs first
    for prop in ["MP_BaseColor", "MP_Roughness", "MP_Metallic", "MP_Specular", "MP_Normal", "MP_Opacity", "MP_Refraction"]:
        try:
            invoke_tool("disconnect_from_output", "editor_toolset.toolsets.material.MaterialTools", {
                "material": MAT_REF, "material_property": prop
            })
        except Exception:
            pass

    # Ensure ShadingModel and BlendMode
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": MAT_REF,
        "values": json.dumps({
            "ShadingModel": "MSM_SingleLayerWater",
            "BlendMode": "BLEND_Opaque",
            "TwoSided": False
        })
    })

    # 2. Add EXACTLY ONE SingleLayerWater Material Output
    slw_out = add_node(MAT_REF, "/Script/Engine.MaterialExpressionSingleLayerWaterMaterialOutput", 600, 400)
    print("  Added SingleLayerWater Output:", slw_out)

    # 3. Add Scattering & Absorption & PhaseG Parameters
    scat_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionVectorParameter", 100, 300, {
        "ParameterName": "ScatteringCoefficients",
        "DefaultValue": {"R": 0.015, "G": 0.055, "B": 0.035, "A": 1.0}
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": scat_param, "from_output_name": "",
        "to_expression": slw_out, "to_input_name": "ScatteringCoefficients"
    })

    absorp_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionVectorParameter", 100, 450, {
        "ParameterName": "AbsorptionCoefficients",
        "DefaultValue": {"R": 0.080, "G": 0.040, "B": 0.020, "A": 1.0}
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": absorp_param, "from_output_name": "",
        "to_expression": slw_out, "to_input_name": "AbsorptionCoefficients"
    })

    phase_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", 100, 600, {
        "ParameterName": "PhaseG",
        "DefaultValue": 0.15
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": phase_param, "from_output_name": "",
        "to_expression": slw_out, "to_input_name": "PhaseG"
    })

    colorscale_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionVectorParameter", 100, 750, {
        "ParameterName": "ColorScaleBehindWater",
        "DefaultValue": {"R": 0.85, "G": 0.90, "B": 0.85, "A": 1.0}
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": colorscale_param, "from_output_name": "",
        "to_expression": slw_out, "to_input_name": "ColorScaleBehindWater"
    })
    print("  ✓ Configured SingleLayerWater volume optical properties")

    # 4. BaseColor (Shallow surface albedo)
    base_color_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionVectorParameter", 200, -300, {
        "ParameterName": "BaseColor_Tint",
        "DefaultValue": {"R": 0.035, "G": 0.075, "B": 0.055, "A": 1.0}
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": base_color_param, "output_name": "", "material_property": "MP_BaseColor"
    })
    print("  ✓ Connected BaseColor_Tint")

    # 5. Roughness
    rough_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", 200, -150, {
        "ParameterName": "Roughness",
        "DefaultValue": 0.08
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": rough_param, "output_name": "", "material_property": "MP_Roughness"
    })
    print("  ✓ Connected Roughness (0.08 calm mirror specular)")

    # 6. Metallic
    metal_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", 200, -50, {
        "ParameterName": "Metallic",
        "DefaultValue": 0.0
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": metal_param, "output_name": "", "material_property": "MP_Metallic"
    })
    print("  ✓ Connected Metallic (0.0 dielectric)")

    # 7. Specular
    spec_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", 200, 50, {
        "ParameterName": "Specular",
        "DefaultValue": 0.50
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": spec_param, "output_name": "", "material_property": "MP_Specular"
    })
    print("  ✓ Connected Specular (0.50)")

    # 8. Refraction
    refr_param = add_node(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", 200, 150, {
        "ParameterName": "Refraction_IOR",
        "DefaultValue": 1.333
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": refr_param, "output_name": "", "material_property": "MP_Refraction"
    })
    print("  ✓ Connected Refraction IOR (1.333 freshwater)")

    # 9. Water Ripples Normal (Dual panning normal map)
    # Layer 1: Panner 1
    panner1 = add_node(MAT_REF, "/Script/Engine.MaterialExpressionPanner", -300, -600, {
        "SpeedX": 0.012,
        "SpeedY": 0.008
    })
    texcoord1 = add_node(MAT_REF, "/Script/Engine.MaterialExpressionTextureCoordinate", -500, -600, {
        "UTiling": 2.0, "VTiling": 2.0
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": texcoord1, "from_output_name": "",
        "to_expression": panner1, "to_input_name": "Coordinate"
    })

    norm_samp1 = add_node(MAT_REF, "/Script/Engine.MaterialExpressionTextureSampleParameter2D", -100, -600, {
        "ParameterName": "NormalMap_Layer1",
        "Texture": {"refPath": TEXTURE_NORMAL}
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": panner1, "from_output_name": "",
        "to_expression": norm_samp1, "to_input_name": ""
    })

    # Layer 2: Panner 2
    panner2 = add_node(MAT_REF, "/Script/Engine.MaterialExpressionPanner", -300, -400, {
        "SpeedX": -0.010,
        "SpeedY": 0.015
    })
    texcoord2 = add_node(MAT_REF, "/Script/Engine.MaterialExpressionTextureCoordinate", -500, -400, {
        "UTiling": 3.5, "VTiling": 3.5
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": texcoord2, "from_output_name": "",
        "to_expression": panner2, "to_input_name": "Coordinate"
    })

    norm_samp2 = add_node(MAT_REF, "/Script/Engine.MaterialExpressionTextureSampleParameter2D", -100, -400, {
        "ParameterName": "NormalMap_Layer2",
        "Texture": {"refPath": TEXTURE_NORMAL}
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": panner2, "from_output_name": "",
        "to_expression": norm_samp2, "to_input_name": ""
    })

    # Blend normals via Add
    norm_add = add_node(MAT_REF, "/Script/Engine.MaterialExpressionAdd", 100, -500)
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": norm_samp1, "from_output_name": "RGB",
        "to_expression": norm_add, "to_input_name": "A"
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": norm_samp2, "from_output_name": "RGB",
        "to_expression": norm_add, "to_input_name": "B"
    })

    # Connect to Normal Output
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": norm_add, "output_name": "", "material_property": "MP_Normal"
    })
    print("  ✓ Connected dual-panning ripples normal to MP_Normal")

    # 10. Recompile Master Material
    print("\nRecompiling M_CurzonPond_Water...")
    recomp_res = invoke_tool("recompile", "editor_toolset.toolsets.material.MaterialTools", {
        "material_or_function": MAT_REF
    })
    print("  ✓ Recompile result:", recomp_res)

    # 11. Create or Update Material Instance MI_CurzonPond_Water
    print(f"\nCreating Material Instance: {INST_NAME}...")
    try:
        invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "folder_path": INST_FOLDER,
            "asset_name": INST_NAME,
            "parent": MAT_REF
        })
    except Exception as e:
        print("  Instance note:", e)

    # Set parameters on MI_CurzonPond_Water
    params_to_set = [
        ("Roughness", 0.08),
        ("Refraction_IOR", 1.333),
        ("PhaseG", 0.15)
    ]
    for pname, val in params_to_set:
        invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": INST_REF, "name": pname, "value": val
        })

    vectors_to_set = [
        ("BaseColor_Tint", {"r": 0.035, "g": 0.075, "b": 0.055, "a": 1.0}),
        ("ScatteringCoefficients", {"r": 0.015, "g": 0.055, "b": 0.035, "a": 1.0}),
        ("AbsorptionCoefficients", {"r": 0.080, "g": 0.040, "b": 0.020, "a": 1.0}),
        ("ColorScaleBehindWater", {"r": 0.85, "g": 0.90, "b": 0.85, "a": 1.0})
    ]
    for vname, vval in vectors_to_set:
        invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": INST_REF, "name": vname, "value": vval
        })

    # Save assets
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": [
            MAT_PATH,
            f"{INST_FOLDER}/{INST_NAME}"
        ]
    })

    print("=" * 70)
    print("SUCCESS: Master Material and Material Instance successfully built and compiled!")
    print("=" * 70)

if __name__ == "__main__":
    main()
