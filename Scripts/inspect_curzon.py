#!/usr/bin/env python3
import json
import subprocess

def run_mcp(toolset, tool, args):
    res = subprocess.check_output(["/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py", "call", toolset, tool, json.dumps(args)])
    return json.loads(res)

actors = run_mcp("editor_toolset.toolsets.scene.SceneTools", "get_actors_in_folder", {"folder_path": "Hero_Buildings"})["returnValue"]

print(f"Total actors in Hero_Buildings: {len(actors)}")
for a in actors:
    ref = a["refPath"]
    lbl = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": {"refPath": ref}})["returnValue"]
    xf = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": {"refPath": ref}})["returnValue"]
    loc = xf["location"]
    scl = xf["scale"]
    rot = xf["rotation"]
    if "Curzon" in lbl:
        print(f"Label: {lbl:<35} Loc: ({loc['x']:8.1f}, {loc['y']:8.1f}, {loc['z']:8.1f}) Scale: ({scl['x']:5.1f}, {scl['y']:5.1f}, {scl['z']:5.1f}) Rot: ({rot['pitch']:4.1f}, {rot['yaw']:4.1f}, {rot['roll']:4.1f}) Ref: {ref}")
