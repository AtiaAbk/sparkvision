import sys
import json
sys.path.insert(0, 'Scripts')
from mcp_client import post_mcp

def call(toolset, tool, args):
    res = post_mcp("tools/call", {
        "name": "call_tool",
        "arguments": {
            "toolset_name": toolset,
            "tool_name": tool,
            "arguments": args
        }
    })
    txt = res.get("content", [{}])[0].get("text", "{}")
    try:
        return json.loads(txt).get("returnValue")
    except Exception:
        return txt

ground_targets = [
    ("Hero_CentralLibrary_Building", 20.0),
    ("Hero_TSC_AuditoriumComplex", 20.0),
    ("Hero_RajuMemorial_Sculpture", 20.0),
    ("Hero_AparajeyoBangla_Sculpture", 20.0),
    ("ArtsFaculty_KalaBhaban_AcademicBlock", 20.0),
    ("TSC_Cafeteria_CourtyardRing", 20.0)
]

for name, target_z in ground_targets:
    actors = call("editor_toolset.toolsets.scene.SceneTools", "find_actors", {"name": name, "tag": "", "collision_channels": []}) or []
    for a in actors:
        lbl = call("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": a})
        xf = call("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": a})
        if xf:
            loc = xf.get("location", {})
            rot = xf.get("rotation", {"pitch": 0.0, "yaw": 0.0, "roll": 0.0})
            scale = xf.get("scale", {"x": 1.0, "y": 1.0, "z": 1.0})
            new_xf = {
                "location": {"x": loc.get("x", 0.0), "y": loc.get("y", 0.0), "z": target_z},
                "rotation": rot,
                "scale": scale
            }
            res = call("editor_toolset.toolsets.actor.ActorTools", "set_actor_transform", {
                "actor": a,
                "xform": new_xf,
                "worldspace": True
            })
            print(f"Grounded {lbl} to Z={target_z} (Result: {res})")

# Assign MI_Hero_Modern to ArtsFaculty_KalaBhaban_AcademicBlock
kala_actors = call("editor_toolset.toolsets.scene.SceneTools", "find_actors", {"name": "ArtsFaculty_KalaBhaban_AcademicBlock", "tag": "", "collision_channels": []}) or []
for a in kala_actors:
    comps = call("editor_toolset.toolsets.actor.ActorTools", "get_components", {"actor": a}) or []
    for c in comps:
        if "StaticMeshComponent" in c.get("refPath", ""):
            call("editor_toolset.toolsets.object.ObjectTools", "set_properties", {
                "instance": c,
                "values": json.dumps({"OverrideMaterials": ["/Game/SparkVision/Materials/MI_Hero_Modern.MI_Hero_Modern"]})
            })
            print("Assigned MI_Hero_Modern to ArtsFaculty_KalaBhaban_AcademicBlock")

print("=== Landmark Grounding & Polishing Complete ===")
