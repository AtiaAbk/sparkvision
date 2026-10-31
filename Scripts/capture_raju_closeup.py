import os
import sys
import json
import base64
sys.path.insert(0, 'Scripts')
from mcp_client import post_mcp

OUTPUT_DIRS = [
    "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots/Development",
    "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)

name = "RajuMemorial_Closeup_Verification"
config = {
    "location": {"x": 58964.0, "y": -62700.0, "z": 240.0},
    "rotation": {"pitch": -6.0, "yaw": -90.0, "roll": 0.0},
    "fov": 60.0,
    "description": "Raju Anti-Terrorism Memorial Sculpture Close-Up"
}

print(f"Capturing {name}: {config['description']}...")
res = post_mcp("tools/call", {
    "name": "call_tool",
    "arguments": {
        "toolset_name": "EditorToolset.EditorAppToolset",
        "tool_name": "CaptureViewport",
        "arguments": {
            "captureTransform": {
                "location": config["location"],
                "rotation": config["rotation"],
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": {
                "gridSpacing": 0,
                "gridExtent": 0,
                "gridHeight": 0,
                "maxLabelDistance": 0,
                "classFilter": {"refPath": "/Script/Engine.Actor"},
                "maxLabels": 0
            },
            "bShowUI": False
        }
    }
})

if res.get("isError"):
    print("Error:", res.get("content"))
    sys.exit(1)

txt = res["content"][0]["text"]
img_b64 = json.loads(txt)["returnValue"]["image"]["data"]
img_bytes = base64.b64decode(img_b64)

for d in OUTPUT_DIRS:
    out_path = os.path.join(d, f"{name}.png")
    with open(out_path, "wb") as f:
        f.write(img_bytes)
print(f"  -> Saved {name}.png ({len(img_bytes)} bytes)")
