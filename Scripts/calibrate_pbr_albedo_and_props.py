#!/usr/bin/env python3
"""
calibrate_pbr_albedo_and_props.py

1. Calibrates T_Curzon_StonePaving_D and T_Pedestrian_Path_D to physically accurate PBR albedos
   (0.24 - 0.28, down from unphysical 0.62) to prevent specular blowout under outdoor sunlight.
2. Updates SM_Curzon_Bench_Colonial so bench slats are dark colonial teak wood (MI_Curzon_WoodDark).
3. Re-imports textures and applies them to material instances.
"""

import os
import sys
import subprocess
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

TEXTURES_SAVED_DIR = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_WWM"
BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender"

def generate_calibrated_textures():
    os.makedirs(TEXTURES_SAVED_DIR, exist_ok=True)
    stone_d_path = os.path.join(TEXTURES_SAVED_DIR, "T_Curzon_StonePaving_D.png")
    path_d_path = os.path.join(TEXTURES_SAVED_DIR, "T_Pedestrian_Path_D.png")

    blender_script = f"""
import bpy
import numpy as np

res = 1024
np.random.seed(42)

# --- 1. T_Curzon_StonePaving_D (Dhaka University Indo-Saracenic Flagstones) ---
# Grid for rectangular flagstones
x = np.linspace(0, 12 * np.pi, res)
y = np.linspace(0, 8 * np.pi, res)
xx, yy = np.meshgrid(x, y)

# Flagstone seams
mortar_x = (np.abs(np.sin(xx)) < 0.05)
mortar_y = (np.abs(np.sin(yy)) < 0.06)
mortar = mortar_x | mortar_y

# Flagstone color variation (warm weathered grey-terracotta sandstone)
# Base stone albedo: ~0.26
stone_var = np.sin(xx * 0.5) * np.cos(yy * 0.5) * 0.04
noise = np.random.uniform(-0.025, 0.025, (res, res))

r_stone = 0.27 + stone_var + noise
g_stone = 0.24 + stone_var + noise
b_stone = 0.22 + stone_var + noise

# Aged Dhaka terracotta dust / patina in corners
patina = np.clip(np.sin(xx * 2) * np.sin(yy * 2) * 0.03, 0, 0.04)
r_stone += patina * 1.5
g_stone += patina * 0.5

# Mortar is dark weathered grey-brown (~0.16)
r = np.where(mortar, 0.18 + noise * 0.5, r_stone).astype(np.float32)
g = np.where(mortar, 0.16 + noise * 0.5, g_stone).astype(np.float32)
b = np.where(mortar, 0.15 + noise * 0.5, b_stone).astype(np.float32)
a = np.ones((res, res), dtype=np.float32)

stone_pixels = np.clip(np.stack([r, g, b, a], axis=-1), 0.05, 0.40)
img1 = bpy.data.images.new("T_Curzon_StonePaving_D", width=res, height=res, alpha=True, float_buffer=False)
img1.pixels.foreach_set(stone_pixels.ravel())
img1.filepath_raw = "{stone_d_path}"
img1.file_format = 'PNG'
img1.save()
print("Saved calibrated T_Curzon_StonePaving_D.png")

# --- 2. T_Pedestrian_Path_D (Warm compact brick dust / stone promenade) ---
r_path = np.clip(0.28 + noise * 1.5, 0.15, 0.38).astype(np.float32)
g_path = np.clip(0.23 + noise * 1.2, 0.12, 0.32).astype(np.float32)
b_path = np.clip(0.19 + noise * 1.0, 0.10, 0.28).astype(np.float32)
path_pixels = np.stack([r_path, g_path, b_path, a], axis=-1).astype(np.float32)

img2 = bpy.data.images.new("T_Pedestrian_Path_D", width=res, height=res, alpha=True, float_buffer=False)
img2.pixels.foreach_set(path_pixels.ravel())
img2.filepath_raw = "{path_d_path}"
img2.file_format = 'PNG'
img2.save()
print("Saved calibrated T_Pedestrian_Path_D.png")
"""
    tmp_path = "/tmp/gen_calibrated_pbr.py"
    with open(tmp_path, "w") as f:
        f.write(blender_script)

    subprocess.run([BLENDER_BIN, "-b", "--python", tmp_path], check=True)
    return stone_d_path, path_d_path

def main():
    print("=" * 70)
    print("CALIBRATING PBR ALBEDO AND PROPS FOR SPARKVISION")
    print("=" * 70)

    # 1. Generate textures
    stone_d, path_d = generate_calibrated_textures()

    # 2. Re-import into Unreal
    for asset_name, src in [("T_Curzon_StonePaving_D", stone_d), ("T_Pedestrian_Path_D", path_d)]:
        try:
            invoke_tool("import_file", "editor_toolset.toolsets.texture.TextureTools", {
                "folder_path": "/Game/SparkVision/Textures",
                "asset_name": asset_name,
                "source_file": src
            })
            print(f"  ✓ Re-imported {asset_name}")
        except Exception as e:
            print(f"  Import note: {e}")

    # 3. Update Bench Colonial mesh so slats are dark teak wood
    print("\nUpdating SM_Curzon_Bench_Colonial material slot 1 to MI_Curzon_WoodDark...")
    try:
        invoke_tool("set_material_slot", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
            "mesh": {"refPath": "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Bench_Colonial.SM_Curzon_Bench_Colonial"},
            "slot_index": 1,
            "material": {"refPath": "/Game/SparkVision/Materials/MI_Curzon_WoodDark.MI_Curzon_WoodDark"}
        })
        print("  ✓ Updated bench slats to MI_Curzon_WoodDark")
    except Exception as e:
        print(f"  Bench update note: {e}")

    # 4. Position PedestrianPath_Curzon_SouthPromenade seamlessly
    print("\nPositioning PedestrianPath_Curzon_SouthPromenade at z=8 with MI_Curzon_StonePaving...")
    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "PedestrianPath_Curzon_SouthPromenade", "tag": "", "collision_channels": []
    })
    actors = res.get("returnValue", [])
    if actors:
        a = actors[0]
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": a,
            "xform": {
                "location": {"x": -2200, "y": 0, "z": 8},
                "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
                "scale": {"x": 45, "y": 10, "z": 0.15}
            }
        })
        comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
        if comps:
            invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": comps[0],
                "values": '{"OverrideMaterials": [{"refPath": "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving"}]}'
            })
            print("  ✓ PedestrianPath_Curzon_SouthPromenade configured with MI_Curzon_StonePaving")

    # 5. Capture verification screenshot
    print("\nCapturing verification viewport...")
    EMPTY_ANNOTATIONS = {
        "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
        "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
    }
    loc = {"x": -4100.0, "y": -250.0, "z": 160.0}
    rot = {"pitch": 2.0, "yaw": 10.0, "roll": 0.0}
    xform = {"location": loc, "rotation": rot, "scale": {"x": 1.0, "y": 1.0, "z": 1.0}}

    invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {"transform": xform})
    time.sleep(1.0)

    cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
        "captureTransform": xform,
        "annotations": EMPTY_ANNOTATIONS,
        "bShowUI": False
    })
    b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
    if b64:
        data = base64.b64decode(b64)
        out_path = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90/CALIBRATED_PBR_VISTA.png"
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"  ✓ Successfully saved {out_path} ({len(data)} bytes)")

    print("\n✅ PBR albedo calibration complete!")

if __name__ == "__main__":
    main()
