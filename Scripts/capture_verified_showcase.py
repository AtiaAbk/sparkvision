#!/usr/bin/env python3
"""
Captures high-fidelity showcase screenshots of Dhaka University architecture
and gameplay elements.
"""

import os
import sys
import json
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

ARTIFACTS_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

VIEWS = [
    {
        "filename": "SHOWCASE_01_Curzon_Authentic_Indo_Saracenic_Doors_Windows.png",
        "cam": {
            "location": {"x": -4800.0, "y": 0.0, "z": 320.0},
            "rotation": {"pitch": -4.0, "yaw": 0.0, "roll": 0.0},
            "scale": {"x": 1, "y": 1, "z": 1}
        },
        "desc": "Curzon Hall South Portico showing authentic Indo-Saracenic red-brick arches, teak double doors with brass rivets, and arched transom windows"
    },
    {
        "filename": "SHOWCASE_02_Kala_Bhaban_Modernist_Ribbon_Windows.png",
        "cam": {
            "location": {"x": 68800.0, "y": -95000.0, "z": 380.0},
            "rotation": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0},
            "scale": {"x": 1, "y": 1, "z": 1}
        },
        "desc": "Faculty of Arts (Kala Bhaban) showing horizontal solar-tinted ribbon windows, concrete brise-soleil sunshades, and double glass entrance"
    },
    {
        "filename": "SHOWCASE_03_TSC_Doxiadis_Waffle_Louvers.png",
        "cam": {
            "location": {"x": 55000.0, "y": -62500.0, "z": 350.0},
            "rotation": {"pitch": -7.0, "yaw": 0.0, "roll": 0.0},
            "scale": {"x": 1, "y": 1, "z": 1}
        },
        "desc": "Teacher-Student Centre (TSC) showing Doxiadis waffle slab louvers, terracotta brick panels, and recessed entrance doors"
    },
    {
        "filename": "SHOWCASE_04_Climax_Cadre_Squad_Nouka_Cap.png",
        "cam": {
            "location": {"x": -1850.0, "y": 1300.0, "z": 180.0},
            "rotation": {"pitch": -4.0, "yaw": 90.0, "roll": 0.0},
            "scale": {"x": 1, "y": 1, "z": 1}
        },
        "desc": "Climax Cadre Squad at Curzon North Courtyard showing Leader with Nouka Cap emblem, helmeted cadres, and bamboo lathis"
    }
]

def main():
    print("=" * 70)
    print("CAPTURING AUTHENTIC ARCHITECTURAL & GAMEPLAY SHOWCASE SCREENSHOTS")
    print("=" * 70)

    for v in VIEWS:
        fname = v["filename"]
        out_path = os.path.join(ARTIFACTS_DIR, fname)
        print(f"\nCapturing: {fname}...")

        try:
            res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
                "captureTransform": v["cam"],
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

            ret = res.get("returnValue", {})
            img_info = ret.get("image", {})
            b64_data = img_info.get("data", "")
            if b64_data:
                img_bytes = base64.b64decode(b64_data)
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  ✓ Saved to: {out_path} ({len(img_bytes)} bytes)")
            else:
                print("  ✗ No image data returned")
        except Exception as e:
            print(f"  ✗ Capture error: {e}")

    print("\n✅ Showcase screenshot capture complete!")

if __name__ == "__main__":
    main()
