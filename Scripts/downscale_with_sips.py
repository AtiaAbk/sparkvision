import os
import subprocess

TEX_DIR = "/Users/atiaoishi/Downloads/sparkvision/Content/SparkVision/Textures"

RESIZE_RULES = {
    # 2048 -> 1024
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
    print("=== DOWNSCALING HIGH-RES SOURCE TEXTURES USING NATIVE MACOS SIPS ===")
    total_saved = 0
    for filename, (w, h) in RESIZE_RULES.items():
        filepath = os.path.join(TEX_DIR, filename)
        if not os.path.exists(filepath):
            continue
        orig_sz = os.path.getsize(filepath)
        subprocess.check_call(["sips", "-z", str(h), str(w), filepath], stdout=subprocess.DEVNULL)
        new_sz = os.path.getsize(filepath)
        diff = orig_sz - new_sz
        total_saved += diff
        print(f"  ✓ Resized {filename} to {w}x{h} (Saved {diff / (1024*1024):.2f} MB)")
    print(f"\nTotal disk texture reduction: {total_saved / (1024*1024):.2f} MB")

if __name__ == "__main__":
    run()
