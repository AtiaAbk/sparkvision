#!/usr/bin/env python3
"""
Imports the authentic architectural facade textures into Unreal Engine
Folder: /Game/SparkVision/Textures
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

TEXTURES_DIR = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_WWM"
TARGET_FOLDER = "/Game/SparkVision/Textures"

NEW_TEXTURES = [
    "T_Curzon_Facade_ArchedDoorsWindows_D",
    "T_Curzon_Facade_ArchedDoorsWindows_N",
    "T_KalaBhaban_Facade_ModernistWindows_D",
    "T_KalaBhaban_Facade_ModernistWindows_N",
    "T_TSC_Facade_DoxiadisWaffle_D",
    "T_TSC_Facade_DoxiadisWaffle_N",
    "T_ModernSkyline_Facade_CurtainWall_D",
    "T_ModernSkyline_Facade_CurtainWall_N",
]

def main():
    print("=" * 60)
    print("IMPORTING AUTHENTIC ARCHITECTURAL FACADE TEXTURES INTO UNREAL")
    print("=" * 60)

    for asset_name in NEW_TEXTURES:
        src = os.path.join(TEXTURES_DIR, f"{asset_name}.png")
        if not os.path.exists(src):
            print(f"  Missing file: {src}")
            continue

        print(f"Importing {asset_name}...")
        try:
            res = invoke_tool("import_file", "editor_toolset.toolsets.texture.TextureTools", {
                "folder_path": TARGET_FOLDER,
                "asset_name": asset_name,
                "source_file": src
            })
            print(f"  ✓ Successfully imported as {TARGET_FOLDER}/{asset_name}")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    print("\n✅ Texture import finished.")

if __name__ == "__main__":
    main()
