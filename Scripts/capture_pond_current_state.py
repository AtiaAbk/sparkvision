#!/usr/bin/env python3
import sys
import os
import base64
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def main():
    print("Setting camera to view Curzon Pond...")
    # Camera looking at pond from Ghat/West side
    cam_xform = {
        "location": {"x": 2000.0, "y": 0.0, "z": 250.0},
        "rotation": {"pitch": -12.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
    invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {
        "transform": cam_xform
    })
    
    print("Capturing viewport...")
    res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
        "captureTransform": cam_xform,
        "annotations": {
            "gridSpacing": 0.0,
            "gridExtent": 0.0,
            "gridHeight": 0.0,
            "maxLabelDistance": 0.0,
            "classFilter": None,
            "maxLabels": 0
        },
        "bShowUI": False
    })
    
    img_data = res.get("returnValue", {}).get("image", {}).get("data", "")
    if img_data:
        out_path = "Documentation/Environment/CurzonPond/Reference/Current_Pond_State_Audit.png"
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(img_data))
        print(f"Saved audit capture to {out_path} ({len(img_data)} bytes)")
    else:
        print("Failed to capture viewport image")

if __name__ == "__main__":
    main()
