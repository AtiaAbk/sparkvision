import sys
import os
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

views = [
    {
        "name": "SHOWCASE_01_Curzon_Authentic_Indo_Saracenic_Doors_Windows.png",
        "loc": {"x": -4300.0, "y": 0.0, "z": 160.0},
        "rot": {"pitch": 4.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "name": "SHOWCASE_02_Curzon_Pond_Water_And_Living_Fish.png",
        "loc": {"x": 2300.0, "y": -120.0, "z": 140.0},
        "rot": {"pitch": -18.0, "yaw": 18.0, "roll": 0.0}
    },
    {
        "name": "SHOWCASE_03_Campus_Gardens_And_Police_Gate.png",
        "loc": {"x": -4400.0, "y": -220.0, "z": 140.0},
        "rot": {"pitch": 2.0, "yaw": 8.0, "roll": 0.0}
    },
]

art_dir = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"

for v in views:
    out_path = os.path.join(art_dir, v["name"])
    print(f"Capturing {v['name']}...")
    try:
        res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": {
                "location": v["loc"],
                "rotation": v["rot"],
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            },
            "annotations": {
                "gridSpacing": 0,
                "gridExtent": 0,
                "gridHeight": 0,
                "maxLabelDistance": 0,
                "classFilter": None,
                "maxLabels": 0
            },
            "bShowUI": False
        })
        img_b64 = res.get("returnValue", {}).get("image", {}).get("data")
        if img_b64:
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            print(f"  ✓ Saved {v['name']} ({os.path.getsize(out_path)} bytes)")
        else:
            print(f"  ✗ Failed to get image data for {v['name']}")
    except Exception as e:
        print(f"  ✗ Error capturing {v['name']}: {e}")

