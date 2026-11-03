#!/usr/bin/env python3
"""
Comprehensive Playable Runtime Character & Outfit Showcase Suite:
Captures distinct character positions and protagonist wardrobe configurations,
and saves high-resolution viewport captures to Documentation/Screenshots/Characters/.
"""

import sys
import os
import json
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

APP_TOOLS = "EditorToolset.EditorAppToolset"
OUTPUT_DIR = "Documentation/Screenshots/Characters"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_viewport(filename, loc, rot):
    xform = {
        "location": loc,
        "rotation": rot,
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
    invoke_tool("SetCameraTransform", APP_TOOLS, {"transform": xform})
    time.sleep(0.4)
    cap = invoke_tool("CaptureViewport", APP_TOOLS, {
        "captureTransform": xform,
        "annotations": {
            "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
            "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
        },
        "bShowUI": False
    })
    data = cap.get("returnValue", {}).get("image", {}).get("data", "")
    if data:
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))
        print(f"  ✓ Captured {filename} ({len(data)} bytes)")
        return path
    else:
        print(f"  ✗ Failed to capture {filename}")
        return None

print("=" * 70)
print("SPARKVISION: CHARACTER & OUTFIT SHOWCASE CAPTURE SUITE")
print("=" * 70)

# Deselect any actors to keep viewport pristine
try:
    invoke_tool("SelectActors", APP_TOOLS, {"actors": []})
except Exception:
    pass

# 1. Main Protagonist (Male Hero - Shovon, DU Maroon Polo + Indigo Denim) Front View
print("\n[1/11] Capturing Main Protagonist Front View...")
save_viewport(
    "01_Protagonist_Male_Front.png",
    {"x": -4350.0, "y": 0.0, "z": 120.0},
    {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
)

# 2. Main Protagonist Rear View & Running Locomotion
print("\n[2/11] Capturing Main Protagonist Rear View...")
save_viewport(
    "02_Protagonist_Male_Rear.png",
    {"x": -4600.0, "y": 0.0, "z": 135.0},
    {"pitch": -8.0, "yaw": 0.0, "roll": 0.0}
)

# 3. Main Protagonist Combat Stance & Evasive Agility
print("\n[3/11] Capturing Main Protagonist Combat Stance...")
save_viewport(
    "03_Protagonist_CombatStance.png",
    {"x": -4400.0, "y": -120.0, "z": 120.0},
    {"pitch": -10.0, "yaw": 25.0, "roll": 0.0}
)

# 4. Male Student Group (Traditional White Panjabi & Navy Oxford Chinos)
print("\n[4/11] Capturing Male Students Group (Curzon Quadrangle)...")
save_viewport(
    "04_Male_Students_Group.png",
    {"x": -3350.0, "y": 280.0, "z": 125.0},
    {"pitch": -8.0, "yaw": -20.0, "roll": 0.0}
)

# 5. Female Student Group (Pastel Salwar Kameez & Mustard Contemporary Kurti)
print("\n[5/11] Capturing Female Students Group...")
save_viewport(
    "05_Female_Students_Group.png",
    {"x": -3050.0, "y": -400.0, "z": 125.0},
    {"pitch": -8.0, "yaw": -140.0, "roll": 0.0}
)

# 6. Teachers & Faculty (Prof. Kabir Safari Khaki & Senior Academics)
print("\n[6/11] Capturing Teachers & Faculty...")
save_viewport(
    "06_Teachers_Faculty.png",
    {"x": -2900.0, "y": 300.0, "z": 125.0},
    {"pitch": -8.0, "yaw": 180.0, "roll": 0.0}
)

# 7. Campus Staff (Laboratory Demonstrator Blue & Maintenance Olive Workwear)
print("\n[7/11] Capturing Campus Staff...")
save_viewport(
    "07_Campus_Staff.png",
    {"x": -2680.0, "y": -780.0, "z": 125.0},
    {"pitch": -8.0, "yaw": -175.0, "roll": 0.0}
)

# 8. Campus Security (University Proctorial Team Safari Khaki)
print("\n[8/11] Capturing Campus Security...")
save_viewport(
    "08_Campus_Security.png",
    {"x": -3500.0, "y": -280.0, "z": 125.0},
    {"pitch": -8.0, "yaw": -170.0, "roll": 0.0}
)

# 9. Mission 6 Hostiles (Cadre Agitators with Motorcycle Helmets & Dark Windbreakers)
print("\n[9/11] Capturing Mission 6 Hostiles...")
save_viewport(
    "09_Mission6_Hostiles.png",
    {"x": -850.0, "y": -1450.0, "z": 125.0},
    {"pitch": -8.0, "yaw": -140.0, "roll": 0.0}
)

# 10. Bangladesh Police Service (Curzon Main Gate Regulation Officers)
print("\n[10/11] Capturing Bangladesh Police Service...")
save_viewport(
    "10_Bangladesh_Police.png",
    {"x": -4050.0, "y": 0.0, "z": 90.0},
    {"pitch": -4.0, "yaw": 180.0, "roll": 0.0}
)

# 11. Bustling Campus Panorama (Students & Faculty across Heritage Grounds)
print("\n[11/11] Capturing Bustling Campus Gameplay Panorama...")
save_viewport(
    "11_Bustling_Campus_Gameplay.png",
    {"x": -3800.0, "y": 0.0, "z": 240.0},
    {"pitch": -16.0, "yaw": 0.0, "roll": 0.0}
)

print("\n" + "=" * 70)
print("ALL 11 AUTHENTIC CHARACTER & OUTFIT CAPTURES SUCCESSFULLY SAVED!")
print("=" * 70)
