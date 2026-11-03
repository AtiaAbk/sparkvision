import os
import numpy as np
from PIL import Image, ImageFilter

output_dir = "Saved/Textures_WWM"
os.makedirs(output_dir, exist_ok=True)

user_branch_path = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90/.user_uploaded/media_1793672279743_794f0c55.png"
user_leaf_path = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90/.user_uploaded/media_1793672279752_ec3eb886.png"

def generate_branch_atlas():
    print("Generating T_Foliage_WWM_LeafBranch_D and N from user reference...")
    branch_src = Image.open(user_branch_path).convert("RGBA")
    # Composite into a 2048x2048 high-res atlas with multiple lush branch arrangements
    atlas = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
    
    # Place large branch top-left
    b1 = branch_src.resize((1300, 1300), Image.Resampling.LANCZOS)
    atlas.paste(b1, (50, 50), b1)
    
    # Place flipped branch bottom-right
    b2 = branch_src.transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((1100, 1100), Image.Resampling.LANCZOS)
    atlas.paste(b2, (900, 900), b2)
    
    # Place smaller leafy branch top-right
    b3 = branch_src.rotate(45, expand=True).resize((900, 900), Image.Resampling.LANCZOS)
    atlas.paste(b3, (1100, 50), b3)
    
    # Place smaller leafy branch bottom-left
    b4 = branch_src.rotate(-30, expand=True).resize((850, 850), Image.Resampling.LANCZOS)
    atlas.paste(b4, (50, 1150), b4)
    
    atlas.save(os.path.join(output_dir, "T_Foliage_WWM_LeafBranch_D.png"))
    print("Saved T_Foliage_WWM_LeafBranch_D.png")

    # Generate tangent space normal map from RGBA
    arr = np.array(atlas)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]
    
    gray = np.mean(rgb, axis=2).astype(np.float32)
    # Mask out transparent background so it doesn't create harsh bevels
    gray[alpha < 30] = 128.0
    
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[:, 1:-1] = (gray[:, 2:] - gray[:, :-2]) * 0.5
    gy[1:-1, :] = (gray[2:, :] - gray[:-2, :]) * 0.5
    
    scale = 3.5
    nx = -gx * scale
    ny = -gy * scale
    nz = 255.0
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = (nx / norm * 127.5 + 127.5).astype(np.uint8)
    ny = (ny / norm * 127.5 + 127.5).astype(np.uint8)
    nz = (nz / norm * 127.5 + 127.5).astype(np.uint8)
    
    normal_img = Image.fromarray(np.dstack([nx, ny, nz, alpha]))
    normal_img.save(os.path.join(output_dir, "T_Foliage_WWM_LeafBranch_N.png"))
    print("Saved T_Foliage_WWM_LeafBranch_N.png")

def generate_natural_bark():
    print("Generating T_Tree_Bark_Natural_D and N...")
    w, h = 2048, 2048
    np.random.seed(101)
    
    # Deep organic wood base tone: dark brownish gray #3E2F26
    base_color = np.array([62, 47, 38], dtype=np.float32)
    
    # Vertical fibrous ridges
    y_coords, x_coords = np.mgrid[0:h, 0:w]
    # Vertical stretch noise
    vertical_freq = np.sin(x_coords * 0.05 + np.sin(y_coords * 0.005) * 8.0) * 20.0
    vertical_freq += np.sin(x_coords * 0.12) * 12.0
    noise = np.random.randn(h, w) * 15.0
    
    bark = np.zeros((h, w, 3), dtype=np.float32)
    for c in range(3):
        bark[:, :, c] = base_color[c] + vertical_freq + noise
    
    # Add subtle green moss patches in crevices
    crevices = (vertical_freq < -10.0)
    moss_color = np.array([48, 72, 34], dtype=np.float32)
    bark[crevices] = bark[crevices] * 0.6 + moss_color * 0.4
    
    bark = np.clip(bark, 0, 255).astype(np.uint8)
    bark_img = Image.fromarray(bark)
    bark_img.save(os.path.join(output_dir, "T_Tree_Bark_Natural_D.png"))
    print("Saved T_Tree_Bark_Natural_D.png")

    # Bark normal map
    gray = np.mean(bark, axis=2).astype(np.float32)
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[:, 1:-1] = (gray[:, 2:] - gray[:, :-2]) * 0.5
    gy[1:-1, :] = (gray[2:, :] - gray[:-2, :]) * 0.5
    
    scale = 4.0
    nx = -gx * scale
    ny = -gy * scale
    nz = 255.0
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = (nx / norm * 127.5 + 127.5).astype(np.uint8)
    ny = (ny / norm * 127.5 + 127.5).astype(np.uint8)
    nz = (nz / norm * 127.5 + 127.5).astype(np.uint8)
    
    normal_img = Image.fromarray(np.stack([nx, ny, nz], axis=2))
    normal_img.save(os.path.join(output_dir, "T_Tree_Bark_Natural_N.png"))
    print("Saved T_Tree_Bark_Natural_N.png")

if __name__ == "__main__":
    generate_branch_atlas()
    generate_natural_bark()
