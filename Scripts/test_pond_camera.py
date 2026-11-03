#!/usr/bin/env python3
import sys
import os
import base64
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def capture_view(name, loc, rot, out_file):
    cam_xform = {
        "location": loc,
        "rotation": rot,
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
    invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {
        "transform": cam_xform
    })
    res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
        "captureTransform": cam_xform,
        "annotations": {
            "gridSpacing": 0.0, "gridExtent": 0.0, "gridHeight": 0.0,
            "maxLabelDistance": 0.0, "classFilter": None, "maxLabels": 0
        },
        "bShowUI": False
    })
    img_data = res.get("returnValue", {}).get("image", {}).get("data", "")
    if img_data:
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(img_data))
        print(f"[{name}] Saved capture to {out_file} ({len(img_data)} bytes)")
    else:
        print(f"[{name}] Failed to capture image")

def main():
    # View 1: East bank looking West across pond towards Ghat and Curzon Hall
    capture_view(
        "East_Bank_Curzon_View",
        {"x": 6800.0, "y": 0.0, "z": 160.0},
        {"pitch": -6.0, "yaw": 180.0, "roll": 0.0},
        "Documentation/Environment/CurzonPond/Reference/Test_East_Bank_View.png"
    )

if __name__ == "__main__":
    main()
