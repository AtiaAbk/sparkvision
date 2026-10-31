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

# Adjust Kala Bhaban so it is North of Aparajeyo Bangla, with long axis along Y (East-West)
kala_actors = call("editor_toolset.toolsets.scene.SceneTools", "find_actors", {"name": "ArtsFaculty_KalaBhaban_AcademicBlock", "tag": "", "collision_channels": []}) or []
for a in kala_actors:
    new_xf = {
        "location": {"x": 76500.0, "y": -95794.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 35.0, "y": 140.0, "z": 18.0}
    }
    res = call("editor_toolset.toolsets.actor.ActorTools", "set_actor_transform", {
        "actor": a,
        "xform": new_xf,
        "worldspace": True
    })
    print(f"Updated Kala Bhaban transform: {res}")

print("=== Kala Bhaban alignment updated ===")
