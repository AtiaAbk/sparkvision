#!/usr/bin/env python3
import json
import subprocess

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

PORTAL_ASSET = "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Entrance_Portal.SM_Curzon_Entrance_Portal"

actor = run_mcp("editor_toolset.toolsets.scene.SceneTools", "add_to_scene_from_asset", {
    "asset_path": PORTAL_ASSET,
    "name": "Curzon_Detail_EntrancePortal",
    "xform": {
        "location": {"x": -2600.0, "y": 0.0, "z": 0.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
})["returnValue"]

ref = actor["refPath"]
print("Spawned portal:", ref)

# Set outliner folder
run_mcp("editor_toolset.toolsets.scene.SceneTools", "set_actor_folder", {
    "actor": {"refPath": ref},
    "folder_path": "Hero_Buildings/Curzon_Detail"
})
print("Assigned to Hero_Buildings/Curzon_Detail")
