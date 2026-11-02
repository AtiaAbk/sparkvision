#!/usr/bin/env python3
"""
Imports the generated Where Winds Meet PBR textures into Unreal Engine
Folder: /Game/SparkVision/Textures
"""

import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

TEXTURES_DIR = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_WWM"
TARGET_FOLDER = "/Game/SparkVision/Textures"

def main():
    print("=" * 60)
    print("IMPORTING WWM PBR TEXTURES INTO UNREAL ENGINE")
    print("=" * 60)

    # Ensure target folder exists
    try:
        invoke_tool("create_folder", "editor_toolset.toolsets.asset.AssetTools", {
            "path": TARGET_FOLDER
        })
    except Exception as e:
        print(f"Folder notice: {e}")

    png_files = glob.glob(os.path.join(TEXTURES_DIR, "*.png"))
    print(f"Found {len(png_files)} textures to import:")

    for f in sorted(png_files):
        asset_name = os.path.splitext(os.path.basename(f))[0]
        print(f"Importing {asset_name} from {f}...")
        try:
            res = invoke_tool("import_file", "editor_toolset.toolsets.texture.TextureTools", {
                "folder_path": TARGET_FOLDER,
                "asset_name": asset_name,
                "source_file": f
            })
            print(f"  ✓ Imported as {TARGET_FOLDER}/{asset_name}")
        except Exception as e:
            print(f"  ✗ Failed to import {asset_name}: {e}")

    print("\n✅ Texture import complete!")

if __name__ == "__main__":
    main()
