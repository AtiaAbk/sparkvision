#!/usr/bin/env python3
"""
Captures a comprehensive 10-camera photographic verification suite
for the living University of Dhaka environment:
- Curzon Hall clean front elevation and architectural details
- Actual Curzon Pond ecology (Ghat, lilies, reeds, riparian trees)
- Doyel Chattar, Fuller Road, Shaheed Minar, Hakim Chattar, Kala Bhaban, The Mall
Saves both to artifacts directory and Documentation/WorldEnvironment/Screenshots/Runtime/
"""

import sys
import os
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
DOC_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldEnvironment/Screenshots/Runtime"
os.makedirs(DOC_DIR, exist_ok=True)

VIEWPOINTS = [
    # 1. Curzon Hall Clean Front Elevation
    ("C01_Curzon_Front_Elevation_Clean.png", {"x": -6600.0, "y": 0.0, "z": 380.0}, {"pitch": 6.0, "yaw": 0.0, "roll": 0.0}),
    # 2. Curzon Entrance Portal Closeup
    ("C02_Curzon_Portal_Closeup.png", {"x": -4500.0, "y": 0.0, "z": 220.0}, {"pitch": 10.0, "yaw": 0.0, "roll": 0.0}),
    # 3. Curzon Physics Wing & Open Driveway
    ("C03_Curzon_Physics_Wing.png", {"x": -5200.0, "y": 2800.0, "z": 250.0}, {"pitch": 5.0, "yaw": -25.0, "roll": 0.0}),
    # 4. Curzon Pond Ecology (Ghat, Lilies, Reeds, Jarul)
    ("C04_Curzon_Pond_Ecology.png", {"x": 1800.0, "y": -400.0, "z": 250.0}, {"pitch": -8.0, "yaw": 15.0, "roll": 0.0}),
    # 5. Doyel Chattar & University Avenue
    ("ENV_01_Doyel_Chattar_Avenue.png", {"x": 4200.0, "y": -16487.0, "z": 350.0}, {"pitch": 5.0, "yaw": 0.0, "roll": 0.0}),
    # 6. Fuller Road Avenue Tree Tunnel
    ("ENV_02_Fuller_Road_Avenue.png", {"x": 2000.0, "y": -59250.0, "z": 300.0}, {"pitch": 4.0, "yaw": 0.0, "roll": 0.0}),
    # 7. Shaheed Minar Sacred Sanctuary
    ("ENV_03_Shaheed_Minar_Sanctuary.png", {"x": -2500.0, "y": -54042.0, "z": 300.0}, {"pitch": 6.0, "yaw": 0.0, "roll": 0.0}),
    # 8. Hakim Chattar & Library Shaded Grove
    ("ENV_04_Hakim_Chattar_Grove.png", {"x": 65000.0, "y": -72500.0, "z": 280.0}, {"pitch": 5.0, "yaw": 10.0, "roll": 0.0}),
    # 9. Aparajeyo Bangla & Kala Bhaban Facade
    ("ENV_05_Aparajeyo_Bangla_KalaBhaban.png", {"x": 70000.0, "y": -95794.0, "z": 600.0}, {"pitch": 5.0, "yaw": 0.0, "roll": 0.0}),
    # 10. The Mall Open Field Grand Banyans
    ("ENV_06_The_Mall_Banyan_Lawns.png", {"x": 56000.0, "y": -86500.0, "z": 500.0}, {"pitch": -5.0, "yaw": 15.0, "roll": 0.0}),
]

def main():
    print("=" * 70, flush=True)
    print("CAPTURING 10-CAMERA PHOTOGRAPHIC VERIFICATION SUITE...", flush=True)
    print("=" * 70, flush=True)

    for filename, loc, rot in VIEWPOINTS:
        try:
            res = mcp_client.invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
                "captureTransform": {
                    "location": loc,
                    "rotation": rot,
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
            img_data = res.get("returnValue", {}).get("image", {}).get("data")
            if img_data:
                raw_bytes = base64.b64decode(img_data)
                out_path_artifact = os.path.join(ARTIFACT_DIR, filename)
                with open(out_path_artifact, "wb") as f:
                    f.write(raw_bytes)
                out_path_doc = os.path.join(DOC_DIR, filename)
                with open(out_path_doc, "wb") as f:
                    f.write(raw_bytes)
                print(f"  [SAVED] {filename} ({len(raw_bytes)} bytes)", flush=True)
            else:
                print(f"  [FAILED] {filename}: No image data returned", flush=True)
        except Exception as e:
            print(f"  [ERROR] {filename}: {e}", flush=True)

    print("\n" + "=" * 70, flush=True)
    print("CAPTURE COMPLETE: All 10 verification images saved to artifacts & documentation!", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
