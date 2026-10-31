#!/usr/bin/env python3
import json
import subprocess

UE_FOLDER = "/Game/SparkVision/Campus/CurzonModular"
MAT_FOLDER = "/Game/SparkVision/Materials"

SLOT_MAPPINGS = {
    "M_Curzon_Brick": f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick",
    "M_Curzon_WhiteTrim": f"{MAT_FOLDER}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    "M_Curzon_Accent": f"{MAT_FOLDER}/MI_Curzon_CastIron.MI_Curzon_CastIron"
}

ASSET_NAMES = [
    "SM_Curzon_Veranda_Arch_Lower",
    "SM_Curzon_Veranda_Arch_Upper",
    "SM_Curzon_Entrance_Portal",
    "SM_Curzon_Chattri_Dome",
    "SM_Curzon_Tower_Octagon",
    "SM_Curzon_Parapet_Merlons",
    "SM_Curzon_Bench_Colonial",
    "SM_Curzon_Lamp_Colonial"
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("Assigning materials to all modular assets...")
for name in ASSET_NAMES:
    mesh_ref = f"{UE_FOLDER}/{name}.{name}"
    slots_res = run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "get_material_slots", {"mesh": {"refPath": mesh_ref}})
    slots = slots_res.get("returnValue", [])
    print(f"\n{name} has slots: {slots}")
    for slot_name in slots:
        mat_ref = SLOT_MAPPINGS.get(slot_name)
        if not mat_ref:
            # Fallback
            mat_ref = f"{MAT_FOLDER}/MI_Curzon_Brick.MI_Curzon_Brick"
        set_res = run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "set_material", {
            "mesh": {"refPath": mesh_ref},
            "slot_name": slot_name,
            "material": {"refPath": mat_ref}
        })
        print(f"  Assigned {slot_name} -> {mat_ref}: {set_res.get('returnValue')}")

print("\nAll modular asset materials assigned successfully!")
