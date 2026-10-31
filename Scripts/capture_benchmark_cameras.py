import sys
import os
import json
import base64
from mcp_client import post_mcp

CAMERAS = {
    "C01_Curzon_Entrance": {
        "location": {"x": -4500.0, "y": 0.0, "z": 350.0},
        "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
        "fov": 75.0,
        "description": "Curzon Hall South Entrance Portico & Symmetrical Verandas"
    },
    "C02_Curzon_Courtyard": {
        "location": {"x": -1500.0, "y": -2200.0, "z": 550.0},
        "rotation": {"pitch": -10.0, "yaw": 60.0, "roll": 0.0},
        "fov": 80.0,
        "description": "Curzon Courtyard Lawn, Colonnade & Octagonal Tower"
    },
    "C03_Campus_Aerial": {
        "location": {"x": -8000.0, "y": -12000.0, "z": 18000.0},
        "rotation": {"pitch": -35.0, "yaw": 30.0, "roll": 0.0},
        "fov": 85.0,
        "description": "Campus Wide Aerial: Curzon to Doyel Chattar & University Avenue"
    },
    "C04_Campus_Pathway": {
        "location": {"x": -2500.0, "y": -4000.0, "z": 250.0},
        "rotation": {"pitch": -2.0, "yaw": 25.0, "roll": 0.0},
        "fov": 75.0,
        "description": "Tree-lined University Avenue Corridor"
    },
    "C05_Campus_LandmarkVista": {
        "location": {"x": -2200.0, "y": -54042.0, "z": 150.0},
        "rotation": {"pitch": 6.0, "yaw": 0.0, "roll": 0.0},
        "fov": 70.0,
        "description": "Central Shaheed Minar Memorial Plaza Vista"
    },
    "C06_ThirdPerson_Exploration": {
        "location": {"x": -3850.0, "y": 45.0, "z": 220.0},
        "rotation": {"pitch": -5.0, "yaw": 0.0, "roll": 0.0},
        "fov": 80.0,
        "description": "Third-Person Gameplay Exploration Behind Player Pawn"
    }
}

OUTPUT_DIRS = [
    "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots/Development",
    "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)

print("=== CAPTURING 6 FIXED CAMERA BENCHMARKS VIA UNREAL MCP ===")

for cam_id, config in CAMERAS.items():
    print(f"\nCapturing {cam_id}: {config['description']}...")
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
        print(f"Error capturing {cam_id}: {res.get('content')}")
        continue
        
    try:
        txt = res["content"][0]["text"]
        img_b64 = json.loads(txt)["returnValue"]["image"]["data"]
        img_bytes = base64.b64decode(img_b64)
        
        for d in OUTPUT_DIRS:
            out_path = os.path.join(d, f"{cam_id}.png")
            with open(out_path, "wb") as f:
                f.write(img_bytes)
        print(f"  -> Saved {cam_id}.png (Size: {len(img_bytes)} bytes)")
    except Exception as e:
        print(f"  -> Exception parsing {cam_id}: {e}")

print("\n=== ALL BENCHMARKS CAPTURED ===")
