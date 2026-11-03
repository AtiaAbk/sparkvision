#!/usr/bin/env python3
"""
Build M_Master_NaturalGround: A Dedicated PBR Master Material for Campus Ground Surfaces
Features:
- BaseColor_Texture (RGB) * Color_Tint (RGB) -> MP_BaseColor
- Normal_Texture (RGB) -> MP_Normal
- Roughness (Scalar) -> MP_Roughness
- UV_Tiling (Scalar) * TexCoord -> Texture Coordinates
- Metallic (0.0) -> MP_Metallic
- Specular (0.45) -> MP_Specular
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

FOLDER = "/Game/SparkVision/Materials"
MAT_NAME = "M_Master_NaturalGround"
MAT_REF = f"{FOLDER}/{MAT_NAME}.{MAT_NAME}"
TEX_FOLDER = "/Game/SparkVision/Textures"

DIFFUSE_GRASS = f"{TEX_FOLDER}/T_Ground_Grass_D.T_Ground_Grass_D"
NORMAL_GRASS = f"{TEX_FOLDER}/T_Ground_Grass_N.T_Ground_Grass_N"
DIFFUSE_BLADES = f"{TEX_FOLDER}/T_Campus_Grass_Blades_D.T_Campus_Grass_Blades_D"
NORMAL_BLADES = f"{TEX_FOLDER}/T_Campus_Grass_Blades_N.T_Campus_Grass_Blades_N"
MASTER_FOLIAGE = f"{FOLDER}/M_Master_NaturalFoliage.M_Master_NaturalFoliage"

def add_expr(mat_ref, expr_class, x, y, props=None):
    res = invoke_tool("add_expression", "editor_toolset.toolsets.material.MaterialTools", {
        "material_or_function": {"refPath": mat_ref},
        "expression_class": {"refPath": expr_class},
        "x": x, "y": y
    })
    node_ref = res.get("returnValue", {}).get("refPath")
    if props and node_ref:
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": node_ref},
            "values": json.dumps(props)
        })
    return node_ref

def main():
    print("=" * 70)
    print("CONSTRUCTING M_MASTER_NATURALGROUND AND GROUND MATERIAL SUITE")
    print("=" * 70)

    # 1. Create or clean M_Master_NaturalGround
    try:
        invoke_tool("create_material", "editor_toolset.toolsets.material.MaterialTools", {
            "folder_path": FOLDER,
            "asset_name": MAT_NAME
        })
        print(f"Created material {MAT_NAME}")
    except Exception as e:
        print(f"Material exists/notice: {e}")

    # Set properties: DefaultLit, Opaque
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": MAT_REF},
        "values": json.dumps({
            "ShadingModel": "MSM_DefaultLit",
            "BlendMode": "BLEND_Opaque",
            "TwoSided": False
        })
    })

    # Disconnect existing outputs
    for prop in ["MP_BaseColor", "MP_Roughness", "MP_Metallic", "MP_Specular", "MP_Normal"]:
        try:
            invoke_tool("disconnect_from_output", "editor_toolset.toolsets.material.MaterialTools", {
                "material": {"refPath": MAT_REF},
                "material_property": prop
            })
        except Exception:
            pass

    # Clean unused expressions
    try:
        invoke_tool("delete_unused_expressions", "editor_toolset.toolsets.material.MaterialTools", {
            "material": {"refPath": MAT_REF}
        })
    except Exception:
        pass

    # Add Nodes
    # A. UV Tiling: TexCoord * UV_Tiling
    tex_coord = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionTextureCoordinate", -800, -200)
    uv_tiling = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", -800, -50, {
        "ParameterName": "UV_Tiling", "DefaultValue": 12.0
    })
    uv_mult = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionMultiply", -600, -150)
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": {"refPath": tex_coord}, "from_output_name": "",
        "to_expression": {"refPath": uv_mult}, "to_input_name": "A"
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": {"refPath": uv_tiling}, "from_output_name": "",
        "to_expression": {"refPath": uv_mult}, "to_input_name": "B"
    })

    # B. BaseColor: TextureSample * Color_Tint
    base_tex = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionTextureSampleParameter2D", -350, -300, {
        "ParameterName": "BaseColor_Texture",
        "Texture": {"refPath": DIFFUSE_GRASS}
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": {"refPath": uv_mult}, "from_output_name": "",
        "to_expression": {"refPath": base_tex}, "to_input_name": ""
    })

    color_tint = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionVectorParameter", -350, -100, {
        "ParameterName": "Color_Tint",
        "DefaultValue": {"R": 0.85, "G": 0.95, "B": 0.80, "A": 1.0}
    })

    color_mult = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionMultiply", -100, -200)
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": {"refPath": base_tex}, "from_output_name": "RGB",
        "to_expression": {"refPath": color_mult}, "to_input_name": "A"
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": {"refPath": color_tint}, "from_output_name": "RGB",
        "to_expression": {"refPath": color_mult}, "to_input_name": "B"
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": color_mult}, "output_name": "", "material_property": "MP_BaseColor"
    })
    print("  ✓ Connected BaseColor")

    # C. Normal Map
    norm_tex = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionTextureSampleParameter2D", -350, 150, {
        "ParameterName": "Normal_Texture",
        "Texture": {"refPath": NORMAL_GRASS}
    })
    invoke_tool("connect_expressions", "editor_toolset.toolsets.material.MaterialTools", {
        "from_expression": {"refPath": uv_mult}, "from_output_name": "",
        "to_expression": {"refPath": norm_tex}, "to_input_name": ""
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": norm_tex}, "output_name": "RGB", "material_property": "MP_Normal"
    })
    print("  ✓ Connected Normal")

    # D. Roughness
    rough_param = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", -100, 50, {
        "ParameterName": "Roughness", "DefaultValue": 0.75
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": rough_param}, "output_name": "", "material_property": "MP_Roughness"
    })
    print("  ✓ Connected Roughness")

    # E. Metallic (0.0) & Specular (0.45)
    metal_param = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", -100, -50, {
        "ParameterName": "Metallic", "DefaultValue": 0.0
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": metal_param}, "output_name": "", "material_property": "MP_Metallic"
    })
    spec_param = add_expr(MAT_REF, "/Script/Engine.MaterialExpressionScalarParameter", -100, 200, {
        "ParameterName": "Specular", "DefaultValue": 0.45
    })
    invoke_tool("connect_to_output", "editor_toolset.toolsets.material.MaterialTools", {
        "expression": {"refPath": spec_param}, "output_name": "", "material_property": "MP_Specular"
    })
    print("  ✓ Connected Metallic & Specular")

    # Recompile Master Material
    print("\nRecompiling M_Master_NaturalGround...")
    invoke_tool("recompile", "editor_toolset.toolsets.material.MaterialTools", {
        "material_or_function": {"refPath": MAT_REF}
    })
    print("  ✓ Master Material successfully compiled!")

    # 2. CREATE THE GROUND MATERIAL INSTANCES
    GROUND_INSTANCES = [
        {
            "name": "MI_Ground_Lawn_Maintained",
            "uv_tiling": 16.0,
            "roughness": 0.68,
            "tint": {"r": 0.88, "g": 0.98, "b": 0.82, "a": 1.0},
            "desc": "Maintained Bermuda grass lawn (Curzon Front Lawn, TSC Lawn, Mall Quad)"
        },
        {
            "name": "MI_Ground_Turf_Natural",
            "uv_tiling": 12.0,
            "roughness": 0.78,
            "tint": {"r": 0.72, "g": 0.82, "b": 0.65, "a": 1.0},
            "desc": "Natural mixed carpet grass (Roadside verges, campus peripheral meadows)"
        },
        {
            "name": "MI_Ground_TreeBase_Loam",
            "uv_tiling": 8.0,
            "roughness": 0.88,
            "tint": {"r": 0.48, "g": 0.40, "b": 0.32, "a": 1.0},
            "desc": "Dark moist deltaic loam (Tree root zones, Banyan/Raintree shaded bases)"
        },
        {
            "name": "MI_Ground_Garden_Soil",
            "uv_tiling": 10.0,
            "roughness": 0.82,
            "tint": {"r": 0.58, "g": 0.48, "b": 0.38, "a": 1.0},
            "desc": "Cultivated garden topsoil (Circular flowerbeds, ornamental parterres)"
        }
    ]

    for gi in GROUND_INSTANCES:
        name = gi["name"]
        mi_ref = f"{FOLDER}/{name}.{name}"
        print(f"\nConfiguring {name}...")
        try:
            invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "folder_path": FOLDER,
                "asset_name": name,
                "parent": {"refPath": MAT_REF}
            })
            print(f"  ✓ Created {name}")
        except Exception:
            pass

        invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "parent": {"refPath": MAT_REF}
        })
        invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "UV_Tiling", "value": gi["uv_tiling"]
        })
        invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "Roughness", "value": gi["roughness"]
        })
        invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "Color_Tint", "value": gi["tint"]
        })
        invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "BaseColor_Texture", "value": {"refPath": DIFFUSE_GRASS}
        })
        invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "Normal_Texture", "value": {"refPath": NORMAL_GRASS}
        })
        print(f"  ✓ Configured {name}: Tiling={gi['uv_tiling']}, Roughness={gi['roughness']}")

    # 3. Configure MI_Campus_Grass_Blades
    print("\nConfiguring MI_Campus_Grass_Blades...")
    blades_mi = f"{FOLDER}/MI_Campus_Grass_Blades.MI_Campus_Grass_Blades"
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
    print("  ✓ Configured MI_Campus_Grass_Blades")

    # 4. Save Assets
    save_list = [
        MAT_REF.split(".")[0],
        f"{FOLDER}/MI_Ground_Lawn_Maintained",
        f"{FOLDER}/MI_Ground_Turf_Natural",
        f"{FOLDER}/MI_Ground_TreeBase_Loam",
        f"{FOLDER}/MI_Ground_Garden_Soil",
        f"{FOLDER}/MI_Campus_Grass_Blades"
    ]
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": save_list
    })
    print("\n✅ All ground materials and instances successfully built and saved!")

if __name__ == "__main__":
    main()
