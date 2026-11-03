import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

PANJABI_MAT = "/Game/SparkVision/Materials/MI_Student_Panjabi_White.MI_Student_Panjabi_White"
KAMEEZ_MAT = "/Game/SparkVision/Materials/MI_Student_SalwarKameez_Pastel.MI_Student_SalwarKameez_Pastel"
POLICE_MAT = "/Game/SparkVision/Materials/MI_Police_Uniform_BD.MI_Police_Uniform_BD"
RAB_MAT = "/Game/SparkVision/Materials/MI_RAB_Tactical_Black.MI_RAB_Tactical_Black"
DENIM_MAT = "/Game/SparkVision/Materials/MI_Student_DenimLegs.MI_Student_DenimLegs"
MAROON_MAT = "/Game/SparkVision/Materials/MI_Student_MaroonTorso.MI_Student_MaroonTorso"

MANNY_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"
QUINN_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple"

print("=== ASSIGNING AUTHENTIC DU STUDENT & LAW ENFORCEMENT ATTIRE ===")

# 1. Update Existing NPCs
student_assignments = {
    # Female students -> Quinn mesh + Salwar Kameez
    "NPC_Ananya_Botany": (QUINN_MESH, [KAMEEZ_MAT, KAMEEZ_MAT]),
    "NPC_Sadia_TSC": (QUINN_MESH, [KAMEEZ_MAT, KAMEEZ_MAT]),
    "NPC_Nabila_FineArts": (QUINN_MESH, [KAMEEZ_MAT, KAMEEZ_MAT]),
    "NPC_Nusrat_Library": (QUINN_MESH, [KAMEEZ_MAT, KAMEEZ_MAT]),
    # Male students -> Traditional Panjabi or Casual Polo
    "NPC_Sabbir_Curzon": (MANNY_MESH, [DENIM_MAT, PANJABI_MAT]),
    "NPC_Rifat_Curzon": (MANNY_MESH, [DENIM_MAT, MAROON_MAT]),
    "NPC_Tanvir_Curzon": (MANNY_MESH, [DENIM_MAT, PANJABI_MAT]),
    "NPC_Farhan_Shaheed": (MANNY_MESH, [DENIM_MAT, MAROON_MAT]),
    "NPC_Arif_Cultural": (MANNY_MESH, [DENIM_MAT, PANJABI_MAT]),
    "NPC_Prof_Jamal_Curzon": (MANNY_MESH, [DENIM_MAT, PANJABI_MAT]),
    "NPC_Prof_Rahman_Arts": (MANNY_MESH, [DENIM_MAT, PANJABI_MAT]),
}

for name, (mesh_path, mats) in student_assignments.items():
    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": name, "tag": "", "collision_channels": []}).get("returnValue", [])
    for a in res:
        ref = a.get("refPath")
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": {"refPath": ref}}).get("returnValue", [])
        for c in comps:
            cref = c.get("refPath")
            if "SkeletalMeshComponent" in cref or "CharacterMesh" in cref or "Mesh" in cref:
                vals = json.dumps({
                    "skeletalMesh": {"refPath": mesh_path},
                    "overrideMaterials": [{"refPath": m} for m in mats]
                })
                invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                    "instance": {"refPath": cref},
                    "values": vals
                })
                print(f"  ✓ Updated attire for {name} ({'Female Salwar Kameez' if mesh_path == QUINN_MESH else 'Traditional Panjabi/Casual'})")

# 2. Spawn Bangladesh Police Officers near the Curzon Gate Checkpoint (-4200, y = -150 to 150)
police_spawns = [
    ("Police_Officer_01_CurzonGate", -4150, -180, 10, 45.0, POLICE_MAT),
    ("Police_Officer_02_CurzonGate", -4150, 180, 10, -45.0, POLICE_MAT),
    ("RAB_Tactical_01_HighCourtRoad", -4350, 0, 10, 0.0, RAB_MAT),
]

for name, x, y, z, yaw, mat in police_spawns:
    try:
        # Check if already exists
        exists = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": name, "tag": "", "collision_channels": []}).get("returnValue", [])
        if not exists:
            actor_ref = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": MANNY_MESH,
                "name": name,
                "xform": {
                    "location": {"x": float(x), "y": float(y), "z": float(z)},
                    "rotation": {"pitch": 0.0, "yaw": float(yaw), "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
                }
            }).get("returnValue", {}).get("refPath")
            
            if actor_ref:
                comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": {"refPath": actor_ref}}).get("returnValue", [])
                for c in comps:
                    cref = c.get("refPath")
                    if "SkeletalMeshComponent" in cref:
                        vals = json.dumps({"overrideMaterials": [{"refPath": mat}, {"refPath": mat}]})
                        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                            "instance": {"refPath": cref},
                            "values": vals
                        })
                print(f"  ✓ Spawned {name} with official uniform at ({x}, {y})")
        else:
            print(f"  {name} already exists in scene")
    except Exception as e:
        print(f"Notice spawning {name}:", e)

