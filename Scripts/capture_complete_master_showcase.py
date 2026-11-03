#!/usr/bin/env python3
"""
SparkVision — Complete Master Showcase Capture Suite
Captures all 4 Hero Vistas and 5 Distinct Architectural District Master Views.
Applies automated feathered patch to eliminate editor viewport tripod widgets,
ensuring publication-ready, pristine showcase visuals.
"""

import sys
import os
import time
import base64
import json
from PIL import Image, ImageFilter, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

SHOWCASE_DIR = "Documentation/Showcase"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
os.makedirs(SHOWCASE_DIR, exist_ok=True)
os.makedirs(ARTIFACT_DIR, exist_ok=True)

EMPTY_ANNOTATIONS = {
    "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
    "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
}

ALL_VIEWS = [
    # 4 Hero Views (Curzon & Living Campus)
    {
        "filename": "HERO_01_Curzon_Facade.png",
        "description": "Curzon Hall Heritage Facade with Prof. Jamal (Dean), Tanvir (Organizer) & Archive Terminal",
        "loc": {"x": -4200.0, "y": 0.0, "z": 180.0},
        "rot": {"pitch": -2.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "filename": "HERO_02_Promenade_Avenue.png",
        "description": "Tree-Lined Promenade Avenue with Student Pedestrians, Study Group & Curzon Vista",
        "loc": {"x": -350.0, "y": 0.0, "z": 220.0},
        "rot": {"pitch": -4.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "filename": "HERO_03_Pond_Ghat_Reflection.png",
        "description": "Curzon Pond Ghat with Ananya (Botany Researcher), Mehedi (Photographer) & Water Reflection",
        "loc": {"x": 2100.0, "y": -750.0, "z": 160.0},
        "rot": {"pitch": -6.0, "yaw": 35.0, "roll": 0.0}
    },
    {
        "filename": "HERO_04_Curzon_Sparring_Courtyard.png",
        "description": "Curzon North Courtyard Martial Arts Sparring Practice with Fahim & Kamal",
        "loc": {"x": -1850.0, "y": 1400.0, "z": 220.0},
        "rot": {"pitch": -7.0, "yaw": 80.0, "roll": 0.0}
    },
    # 5 Campus Landmark & Modern Architecture District Master Views
    {
        "filename": "DISTRICT1_CURZON_HALL_MASTER.png",
        "description": "District 1: Curzon Hall Indo-Saracenic Heritage Architecture (Authentic Terracotta Brick & Domes)",
        "loc": {"x": -4800.0, "y": 0.0, "z": 380.0},
        "rot": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "filename": "DISTRICT2_SHAHEED_MINAR_MASTER.png",
        "description": "District 2: Central Shaheed Minar (Pristine Carrara Marble, Crimson Sun & Mirror Black Granite)",
        "loc": {"x": -3400.0, "y": -54000.0, "z": 260.0},
        "rot": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "filename": "DISTRICT3_TSC_MASTER.png",
        "description": "District 3: Teacher-Student Centre (TSC White Waffle Fascia, Terracotta Panels & Green Solar Glass)",
        "loc": {"x": 55000.0, "y": -62500.0, "z": 350.0},
        "rot": {"pitch": -7.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "filename": "DISTRICT4_KALA_BHABAN_MASTER.png",
        "description": "District 4: Faculty of Arts - Kala Bhaban (Modern Sand Concrete Louvers & Ribbon Glass Windows)",
        "loc": {"x": 68800.0, "y": -95000.0, "z": 380.0},
        "rot": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "filename": "DISTRICT5_DOYEL_CHATTAR_MASTER.png",
        "description": "District 5: Doyel Chattar Monument (Turquoise Mosaic Pool, Teal Wings & Modern City Skyline Towers)",
        "loc": {"x": 30500.0, "y": -22000.0, "z": 300.0},
        "rot": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    }
]

def clean_bottom_left_widget(img_path):
    """Seamlessly patches the editor tripod widget at bottom-left corner with feathered blending."""
    try:
        im = Image.open(img_path).convert("RGB")
        w, h = im.size
        box_w = 160
        box_h = 170
        target_x = 20
        target_y = h - 190

        # Source clean ground texture to the right of the target area
        src_x = target_x + box_w + 40
        src_y = target_y

        if src_x + box_w <= w and src_y + box_h <= h:
            patch = im.crop((src_x, src_y, src_x + box_w, src_y + box_h))
            mask = Image.new("L", (box_w, box_h), 0)
            draw = ImageDraw.Draw(mask)
            feather = 15
            draw.rectangle([feather, feather, box_w - feather, box_h - feather], fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(feather / 2))
            im.paste(patch, (target_x, target_y), mask)
            im.save(img_path, "PNG")
    except Exception as e:
        print(f"  Notice patching widget on {img_path}: {e}")

def main():
    print("=" * 80)
    print("SPARKVISION: CAPTURING COMPLETE MASTER SHOWCASE SUITE")
    print("=" * 80)

    # Deselect all actors to prevent editor outlines
    try:
        invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
    except Exception:
        pass

    # Stop any running PIE
    try:
        invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
        time.sleep(1.0)
    except Exception:
        pass

    successful_captures = []

    for idx, view in enumerate(ALL_VIEWS, start=1):
        filename = view["filename"]
        desc = view["description"]
        loc = view["loc"]
        rot = view["rot"]
        xform = {"location": loc, "rotation": rot, "scale": {"x": 1.0, "y": 1.0, "z": 1.0}}

        print(f"\n[{idx}/{len(ALL_VIEWS)}] Positioning Camera: {filename}")
        print(f"      {desc}")
        invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {"transform": xform})
        time.sleep(1.2)

        print(f"      Capturing Viewport...")
        cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": xform,
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })

        b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
        if b64:
            raw_bytes = base64.b64decode(b64)
            showcase_path = os.path.join(SHOWCASE_DIR, filename)
            artifact_path = os.path.join(ARTIFACT_DIR, filename)

            # Write raw images
            with open(showcase_path, "wb") as f:
                f.write(raw_bytes)
            with open(artifact_path, "wb") as f:
                f.write(raw_bytes)

            # Clean editor widget
            clean_bottom_left_widget(showcase_path)
            clean_bottom_left_widget(artifact_path)

            file_size_kb = os.path.getsize(showcase_path) / 1024.0
            print(f"      ✓ Successfully captured & cleaned: {filename} ({file_size_kb:.1f} KB)")
            successful_captures.append((filename, desc, file_size_kb))
        else:
            print(f"      ❌ Failed to capture viewport for {filename}")

    print("\n" + "=" * 80)
    print("SHOWCASE CAPTURE SUMMARY")
    print("=" * 80)
    for fname, desc, sz in successful_captures:
        print(f"  • {fname:<36} ({sz:6.1f} KB) — {desc}")
    print(f"\nTotal Captured: {len(successful_captures)}/{len(ALL_VIEWS)} views successfully saved.")

if __name__ == "__main__":
    main()
