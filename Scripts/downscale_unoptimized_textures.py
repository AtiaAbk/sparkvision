import sys
import os
from PIL import Image

TEX_DIR = "/Users/atiaoishi/Downloads/sparkvision/Content/SparkVision/Textures"

# Texture rules:
# Landmark heroes (Curzon brick, Curzon entrance door) -> Keep at 2048x2048
# Background/Props/Vehicles/Distant foliage/Skyline/Foliage Atlas -> 1024x1024 or 512x512
RESIZE_RULES = {
    # 2048 -> 1024 (Background facades and generic foliage/materials)
    "T_ModernSkyline_Facade_CurtainWall_D.png": (1024, 1024),
    "T_ModernSkyline_Facade_CurtainWall_N.png": (1024, 1024),
    "T_TSC_Facade_DoxiadisWaffle_D.png": (1024, 1024),
    "T_TSC_Facade_DoxiadisWaffle_N.png": (1024, 1024),
    "T_KalaBhaban_Facade_ModernistWindows_D.png": (1024, 1024),
    "T_KalaBhaban_Facade_ModernistWindows_N.png": (1024, 1024),
    "T_Foliage_WWM_LeafBranch_D.png": (1024, 1024),
    "T_Foliage_WWM_LeafBranch_N.png": (1024, 1024),
    "T_Tree_Bark_Natural_D.png": (1024, 1024),
    "T_Tree_Bark_Natural_N.png": (1024, 1024),
    "T_Water_Ripples_N.png": (1024, 1024),
    "T_Police_Uniform_BD_D.png": (1024, 1024),
    "T_RAB_Tactical_Black_D.png": (1024, 1024),
    "T_Student_Panjabi_White_D.png": (1024, 1024),
    "T_Student_SalwarKameez_Pastel_D.png": (1024, 1024),
    # 1024 -> 512
    "T_Pond_KoiFish_D.png": (512, 512),
}

def run():
    print("=== DOWNSCALING HIGH-RES SOURCE TEXTURES FOR MAC M4 OPTIMIZATION ===")
    total_saved_bytes = 0
    for filename, new_sz in RESIZE_RULES.items():
        filepath = os.path.join(TEX_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename} (not found on disk)")
            continue
        orig_sz = os.path.getsize(filepath)
        im = Image.open(filepath)
        orig_res = im.size
        if orig_res == new_sz:
            print(f"  {filename} already at {new_sz}")
            continue
        print(f"  Resizing {filename}: {orig_res} -> {new_sz}...")
        # Use LANCZOS for high quality resampling
        im_resized = im.resize(new_sz, Image.Resampling.LANCZOS)
        im_resized.save(filepath, optimize=True)
        new_size = os.path.getsize(filepath)
        saved = orig_sz - new_size
        total_saved_bytes += saved
        print(f"    Saved {saved / (1024*1024):.2f} MB (New disk size: {new_size/(1024*1024):.2f} MB)")
    print(f"\nTotal disk texture reduction: {total_saved_bytes / (1024*1024):.2f} MB")
    print("Textures resized cleanly.")

if __name__ == "__main__":
    run()
