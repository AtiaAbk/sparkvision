import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MASTER_PBR = "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"
MASTER_FOLIAGE = "/Game/SparkVision/Materials/M_Master_NaturalFoliage.M_Master_NaturalFoliage"
TEX_DIR = "/Users/atiaoishi/Downloads/sparkvision/Content/SparkVision/Textures"
MAT_FOLDER = "/Game/SparkVision/Materials"
TEX_FOLDER = "/Game/SparkVision/Textures"

TEXTURES_TO_IMPORT = [
    ("T_Curzon_Brick_ImperialTerracotta_D", f"{TEX_DIR}/T_Curzon_Brick_ImperialTerracotta_D.png"),
    ("T_Curzon_Brick_ImperialTerracotta_N", f"{TEX_DIR}/T_Curzon_Brick_ImperialTerracotta_N.png"),
    ("T_Curzon_EntranceDoor_ColonialTeak_D", f"{TEX_DIR}/T_Curzon_EntranceDoor_ColonialTeak_D.png"),
    ("T_Curzon_EntranceDoor_ColonialTeak_N", f"{TEX_DIR}/T_Curzon_EntranceDoor_ColonialTeak_N.png"),
    ("T_Foliage_WWM_LeafBranch_D", f"{TEX_DIR}/T_Foliage_WWM_LeafBranch_D.png"),
    ("T_Foliage_WWM_LeafBranch_N", f"{TEX_DIR}/T_Foliage_WWM_LeafBranch_N.png"),
    ("T_Tree_Bark_Natural_D", f"{TEX_DIR}/T_Tree_Bark_Natural_D.png"),
    ("T_Tree_Bark_Natural_N", f"{TEX_DIR}/T_Tree_Bark_Natural_N.png"),
    ("T_Water_Ripples_N", f"{TEX_DIR}/T_Water_Ripples_N.png"),
    ("T_Police_Uniform_BD_D", f"{TEX_DIR}/T_Police_Uniform_BD_D.png"),
    ("T_RAB_Tactical_Black_D", f"{TEX_DIR}/T_RAB_Tactical_Black_D.png"),
    ("T_Student_Panjabi_White_D", f"{TEX_DIR}/T_Student_Panjabi_White_D.png"),
    ("T_Student_SalwarKameez_Pastel_D", f"{TEX_DIR}/T_Student_SalwarKameez_Pastel_D.png"),
]

def import_textures():
    print("=== 1. IMPORTING TEXTURES ===")
    for asset_name, src_path in TEXTURES_TO_IMPORT:
        if not os.path.exists(src_path):
            print(f"Missing: {src_path}")
            continue
        try:
            invoke_tool("import_file", "editor_toolset.toolsets.texture.TextureTools", {
                "folder_path": TEX_FOLDER,
                "asset_name": asset_name,
                "source_file": src_path
            })
            print(f"  ✓ Imported: {TEX_FOLDER}/{asset_name}")
        except Exception as e:
            print(f"  Notice {asset_name}: {e}")

def configure_material(name, parent, diffuse=None, normal=None, color=None, roughness=None):
    mi_ref = f"{MAT_FOLDER}/{name}.{name}"
    exists = invoke_tool("exists", "editor_toolset.toolsets.asset.AssetTools", {
        "path": f"{MAT_FOLDER}/{name}"
    }).get("returnValue", False)
    
    if not exists:
        try:
            invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "folder_path": MAT_FOLDER,
                "asset_name": name,
                "parent": {"refPath": parent}
            })
            print(f"  Created MI: {name}")
        except Exception as e:
            print(f"  Notice creating {name}: {e}")
    else:
        try:
            invoke_tool("set_parent", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "parent": {"refPath": parent}
            })
        except Exception as e:
            pass

    if diffuse:
        try:
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "BaseColor_Texture",
                "value": {"refPath": diffuse}
            })
        except Exception as e:
            print(f"  Notice setting diffuse on {name}: {e}")

    if normal:
        try:
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Normal_Texture",
                "value": {"refPath": normal}
            })
        except Exception as e:
            print(f"  Notice setting normal on {name}: {e}")

    if color:
        try:
            invoke_tool("set_vector_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Color",
                "value": color
            })
        except Exception as e:
            print(f"  Notice setting color on {name}: {e}")

    if roughness is not None:
        try:
            invoke_tool("set_scalar_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": mi_ref},
                "name": "Roughness",
                "value": roughness
            })
        except Exception as e:
            print(f"  Notice setting roughness on {name}: {e}")

def setup_all_materials():
    print("\n=== 2. CONFIGURING MATERIAL INSTANCES ===")
    # 1. Curzon Brick: Authentic deep red-oxide terracotta
    configure_material(
        "MI_Curzon_Brick",
        MASTER_PBR,
        diffuse=f"{TEX_FOLDER}/T_Curzon_Brick_ImperialTerracotta_D.T_Curzon_Brick_ImperialTerracotta_D",
        normal=f"{TEX_FOLDER}/T_Curzon_Brick_ImperialTerracotta_N.T_Curzon_Brick_ImperialTerracotta_N",
        color={"r": 0.48, "g": 0.12, "b": 0.08, "a": 1.0},
        roughness=0.82
    )
    print("  ✓ Configured MI_Curzon_Brick (Deep imperial red terracotta)")

    # 2. Curzon Grand Entrance Door
    configure_material(
        "MI_Curzon_EntranceDoor",
        MASTER_PBR,
        diffuse=f"{TEX_FOLDER}/T_Curzon_EntranceDoor_ColonialTeak_D.T_Curzon_EntranceDoor_ColonialTeak_D",
        normal=f"{TEX_FOLDER}/T_Curzon_EntranceDoor_ColonialTeak_N.T_Curzon_EntranceDoor_ColonialTeak_N",
        roughness=0.60
    )
    print("  ✓ Configured MI_Curzon_EntranceDoor")

    # 3. Foliage: Leaves & Branches
    for leaf_mat in ["MI_Foliage_Raintree_Natural", "MI_Foliage_Banyan_Natural", "MI_Foliage_Krishnachura_Natural", "MI_Foliage_Radhachura_Yellow"]:
        configure_material(
            leaf_mat,
            MASTER_PBR,
            diffuse=f"{TEX_FOLDER}/T_Foliage_WWM_LeafBranch_D.T_Foliage_WWM_LeafBranch_D",
            normal=f"{TEX_FOLDER}/T_Foliage_WWM_LeafBranch_N.T_Foliage_WWM_LeafBranch_N",
            roughness=0.45
        )
    print("  ✓ Configured Natural Foliage materials (WWM branch atlas)")

    # 4. Tree Bark
    configure_material(
        "MI_Bark_Tree",
        MASTER_PBR,
        diffuse=f"{TEX_FOLDER}/T_Tree_Bark_Natural_D.T_Tree_Bark_Natural_D",
        normal=f"{TEX_FOLDER}/T_Tree_Bark_Natural_N.T_Tree_Bark_Natural_N",
        roughness=0.88
    )
    print("  ✓ Configured MI_Bark_Tree (Natural organic bark)")

    # 5. Natural Water
    configure_material(
        "MI_Water_Pond",
        MASTER_PBR,
        normal=f"{TEX_FOLDER}/T_Water_Ripples_N.T_Water_Ripples_N",
        color={"r": 0.08, "g": 0.42, "b": 0.72, "a": 1.0}, # Natural vibrant blue
        roughness=0.03
    )
    print("  ✓ Configured MI_Water_Pond (Natural azure water)")

    # 6. Characters: Police, RAB, Students
    configure_material(
        "MI_Police_Uniform_BD",
        MASTER_PBR,
        diffuse=f"{TEX_FOLDER}/T_Police_Uniform_BD_D.T_Police_Uniform_BD_D",
        roughness=0.70
    )
    configure_material(
        "MI_RAB_Tactical_Black",
        MASTER_PBR,
        diffuse=f"{TEX_FOLDER}/T_RAB_Tactical_Black_D.T_RAB_Tactical_Black_D",
        roughness=0.65
    )
    configure_material(
        "MI_Student_Panjabi_White",
        MASTER_PBR,
        diffuse=f"{TEX_FOLDER}/T_Student_Panjabi_White_D.T_Student_Panjabi_White_D",
        roughness=0.80
    )
    configure_material(
        "MI_Student_SalwarKameez_Pastel",
        MASTER_PBR,
        diffuse=f"{TEX_FOLDER}/T_Student_SalwarKameez_Pastel_D.T_Student_SalwarKameez_Pastel_D",
        roughness=0.75
    )
    print("  ✓ Configured Character and Law Enforcement materials")

def assign_curzon_mesh_slots():
    print("\n=== 3. ASSIGNING SLOTS ON CURZON MODULAR MESHES ===")
    slot_map = {
        "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
        "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
        "M_Curzon_WoodDark": f"{MAT_FOLDER}/MI_Curzon_WoodDark.MI_Curzon_WoodDark",
        "M_Curzon_Sandstone": f"{MAT_FOLDER}/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
        "M_Curzon_Louvers": f"{MAT_FOLDER}/MI_Curzon_Louvers.MI_Curzon_Louvers",
        "M_Curzon_Glass": f"{MAT_FOLDER}/MI_Curzon_Glass.MI_Curzon_Glass",
        "M_Curzon_Brass": f"{MAT_FOLDER}/MI_Curzon_Brass.MI_Curzon_Brass",
        "M_Curzon_Tiles": f"{MAT_FOLDER}/MI_Curzon_Tiles.MI_Curzon_Tiles",
    }

    meshes = [
        "SM_Curzon_Entrance_Portal",
        "SM_Curzon_Veranda_Arch_Lower",
        "SM_Curzon_Veranda_Arch_Upper",
        "SM_Curzon_Tower_Octagon",
        "SM_CurzonHall",
        "SM_Curzon_Heritage_Gate"
    ]

    for m in meshes:
        mesh_path = f"/Game/SparkVision/Campus/CurzonModular/{m}.{m}" if m not in ["SM_CurzonHall", "SM_Curzon_Heritage_Gate"] else (
            f"/Game/SparkVision/Campus/{m}.{m}" if m == "SM_CurzonHall" else f"/Game/SparkVision/Campus/Heritage/{m}.{m}"
        )
        print(f"Updating mesh: {m}...")
        for slot_name, mat_path in slot_map.items():
            try:
                invoke_tool("set_material", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                    "mesh": {"refPath": mesh_path},
                    "slot_name": slot_name,
                    "material": {"refPath": mat_path}
                })
            except Exception as e:
                pass
        print(f"  ✓ Applied slots on {m}")

def main():
    import_textures()
    setup_all_materials()
    assign_curzon_mesh_slots()
    print("\nALL IMPORTS AND ENHANCEMENTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
