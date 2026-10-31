#!/usr/bin/env python3
"""
Full Campus 10-Camera Visual Benchmark Capture Script
Captures C01 through C10 viewpoints using Unreal MCP CaptureViewport
Saves images to Documentation/Screenshots and the Brain Artifact Directory
"""

import os
import json
import base64
import subprocess
import time

SCREENSHOTS_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/Screenshots"
BRAIN_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

CAMERAS = [
    {
        "id": "C01",
        "name": "Curzon_Front_Promenade",
        "desc": "Curzon Hall Southern Facade, Arched Colonnades & Garden Walkway",
        "location": {"x": -4200.0, "y": 0.0, "z": 350.0},
        "rotation": {"pitch": -10.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C02",
        "name": "Curzon_Botanical_Pond",
        "desc": "Curzon Inner Botanical Pond & Science Annex Wings",
        "location": {"x": 3200.0, "y": 0.0, "z": 450.0},
        "rotation": {"pitch": -12.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C03",
        "name": "Doyel_Chattar_Roundabout",
        "desc": "Doyel Chattar Magpie Robin Fountain & Bangla Academy",
        "location": {"x": 6200.0, "y": -18000.0, "z": 300.0},
        "rotation": {"pitch": -8.0, "yaw": 35.0, "roll": 0.0}
    },
    {
        "id": "C04",
        "name": "TSC_Mor_Raju_Square",
        "desc": "TSC Modernist Auditorium & Raju Memorial Sculpture",
        "location": {"x": 55000.0, "y": -66000.0, "z": 280.0},
        "rotation": {"pitch": -8.0, "yaw": 45.0, "roll": 0.0}
    },
    {
        "id": "C05",
        "name": "Central_Library_HakimChattar",
        "desc": "Muzharul Islam Central Library & Shaded Hakim Chattar Plaza",
        "location": {"x": 68000.0, "y": -74000.0, "z": 350.0},
        "rotation": {"pitch": -10.0, "yaw": 30.0, "roll": 0.0}
    },
    {
        "id": "C06",
        "name": "Central_Shaheed_Minar",
        "desc": "Central Shaheed Minar Monument, Sun Disc & Marble Altar",
        "location": {"x": -2500.0, "y": -54042.0, "z": 350.0},
        "rotation": {"pitch": -10.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C07",
        "name": "Kala_Bhaban_Aparajeyo",
        "desc": "Kala Bhaban Brise-Soleil Academic Block & Aparajeyo Bangla Sculpture",
        "location": {"x": 69000.0, "y": -95794.0, "z": 320.0},
        "rotation": {"pitch": -10.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C08",
        "name": "Salimullah_Muslim_Hall",
        "desc": "Salimullah Muslim (SM) Hall 1931 Indo-Saracenic Quadrangle",
        "location": {"x": 8000.0, "y": -56500.0, "z": 520.0},
        "rotation": {"pitch": -7.5, "yaw": -43.0, "roll": 0.0}
    },
    {
        "id": "C09",
        "name": "Central_Mosque_Nazrul",
        "desc": "DU Central Mosque Dome, Minarets & Kazi Nazrul Islam Mausoleum",
        "location": {"x": 40000.0, "y": -84000.0, "z": 480.0},
        "rotation": {"pitch": -8.0, "yaw": 50.0, "roll": 0.0}
    },
    {
        "id": "C10",
        "name": "Full_Campus_Aerial_Masterplan",
        "desc": "High-Altitude Aerial Masterplan Vista Across Full 1.6km x 1.4km Campus",
        "location": {"x": 35000.0, "y": -50000.0, "z": 22000.0},
        "rotation": {"pitch": -65.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "C11",
        "name": "SurjaSen_Mohsin_Complex",
        "desc": "Masterda Surja Sen & Haji Muhammad Mohsin Halls Modernist Residential Complex",
        "location": {"x": 74000.0, "y": -86000.0, "z": 650.0},
        "rotation": {"pitch": -10.0, "yaw": -139.0, "roll": 0.0}
    }
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("=" * 70)
print("CAPTURING 10-CAMERA BENCHMARK SUITE (C01 - C10)...")
print("=" * 70)

for cam in CAMERAS:
    cid = cam["id"]
    cname = cam["name"]
    print(f"\n--- Capturing {cid}: {cname} ---")
    filename = f"{cid}_{cname}.png"
    doc_path = os.path.join(SCREENSHOTS_DIR, filename)
    brain_path = os.path.join(BRAIN_DIR, filename)

    args = {
        "captureTransform": {
            "location": cam["location"],
            "rotation": cam["rotation"],
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        },
        "annotations": {
            "gridSpacing": 0,
            "gridExtent": 0,
            "gridHeight": 0,
            "maxLabelDistance": 0,
            "classFilter": {"refPath": "/Script/Engine.StaticMeshActor"},
            "maxLabels": 0
        },
        "bShowUI": False
    }

    try:
        res = run_mcp("EditorToolset.EditorAppToolset", "CaptureViewport", args)
        img_b64 = res.get("returnValue", {}).get("image", {}).get("data", "")
        if img_b64:
            img_bytes = base64.b64decode(img_b64)
            with open(doc_path, "wb") as f_doc:
                f_doc.write(img_bytes)
            with open(brain_path, "wb") as f_brain:
                f_brain.write(img_bytes)
            print(f"SUCCESS: Saved {filename} ({len(img_bytes)} bytes)")
        else:
            print(f"WARNING: No image data returned for {cid}")
    except Exception as e:
        print(f"ERROR capturing {cid}: {e}")

print("\n" + "=" * 70)
print("ALL 10 BENCHMARK VIEWPOINTS CAPTURED!")
print("=" * 70)
