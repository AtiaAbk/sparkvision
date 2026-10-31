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

LANDMARK_VIEWS = {
    "DoyelChattar_Verification": {
        "location": {"x": 10500.0, "y": -15000.0, "z": 250.0},
        "rotation": {"pitch": -5.0, "yaw": -180.0, "roll": 0.0},
        "fov": 75.0,
        "description": "Doyel Chattar Roundabout & Magpie-Robin Fountain"
    },
    "TSC_Raju_Verification": {
        "location": {"x": 58964.0, "y": -60800.0, "z": 220.0},
        "rotation": {"pitch": -2.0, "yaw": -180.0, "roll": 0.0},
        "fov": 75.0,
        "description": "TSC Mor, Raju Memorial Sculpture & TSC Auditorium"
    },
    "CentralLibrary_Verification": {
        "location": {"x": 67500.0, "y": -71699.0, "z": 450.0},
        "rotation": {"pitch": -2.0, "yaw": 0.0, "roll": 0.0},
        "fov": 75.0,
        "description": "DU Central Library (Muzharul Islam 1953 Modernist Pilotis & Louvers)"
    },
    "AparajeyoBangla_Verification": {
        "location": {"x": 71800.0, "y": -95794.0, "z": 240.0},
        "rotation": {"pitch": 3.0, "yaw": 0.0, "roll": 0.0},
        "fov": 75.0,
        "description": "Aparajeyo Bangla Freedom Fighter Trio & Arts Faculty Plaza"
    }
}

for name, config in LANDMARK_VIEWS.items():
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
        print(f"Error capturing {name}: {res.get('content')}")
        continue
        
    try:
        txt = res["content"][0]["text"]
        img_b64 = json.loads(txt)["returnValue"]["image"]["data"]
        img_bytes = base64.b64decode(img_b64)
        
        for d in OUTPUT_DIRS:
            out_path = os.path.join(d, f"{name}.png")
            with open(out_path, "wb") as f:
                f.write(img_bytes)
        print(f"  -> Saved {name}.png ({len(img_bytes)} bytes)")
    except Exception as e:
        print(f"  -> Exception parsing {name}: {e}")

print("=== LANDMARK VERIFICATION CAPTURES COMPLETE ===")
