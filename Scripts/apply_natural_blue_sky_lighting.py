import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

print("=== ADJUSTING LIGHTING FOR NATURAL BLUE SKY & DAYLIGHT ===")

# 1. Directional Light
dir_lights = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": "DirectionalLight", "tag": "", "collision_channels": []}).get("returnValue", [])
for a in dir_lights:
    ref = a.get("refPath")
    # Set transform: higher sun angle (-48 pitch)
    invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
        "actor": {"refPath": ref},
        "xform": {
            "location": {"x": 0.0, "y": 0.0, "z": 0.0},
            "rotation": {"pitch": -48.0, "yaw": -125.0, "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
    })
    # Set light component properties
    comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": {"refPath": ref}}).get("returnValue", [])
    for c in comps:
        cref = c.get("refPath")
        if "DirectionalLightComponent" in cref:
            vals = json.dumps({
                "intensity": 68000.0,
                "temperature": 6000.0,
                "bUseTemperature": True,
                "lightColor": {"r": 1.0, "g": 0.99, "b": 0.98, "a": 1.0}
            })
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": {"refPath": cref},
                "values": vals
            })
            print("  ✓ Updated DirectionalLightComponent (Midday crisp sun, 6000K)")

# 2. PostProcessVolume
pp_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": "PostProcessVolume", "tag": "", "collision_channels": []}).get("returnValue", [])
for a in pp_actors:
    ref = a.get("refPath")
    vals = json.dumps({
        "settings": {
            "bOverride_WhiteTemp": True,
            "whiteTemp": 6500.0, # Natural neutral white balance (D65)
            "bOverride_ColorSaturation": True,
            "colorSaturation": {"x": 1.05, "y": 1.05, "z": 1.05, "w": 1.0},
            "bOverride_ColorContrast": True,
            "colorContrast": {"x": 1.02, "y": 1.02, "z": 1.02, "w": 1.0}
        }
    })
    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
        "instance": {"refPath": ref},
        "values": vals
    })
    print("  ✓ Updated PostProcessVolume (Neutral daylight balance, 6500K)")

