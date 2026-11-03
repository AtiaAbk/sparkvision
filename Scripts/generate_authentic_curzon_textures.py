import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

output_dir = "Saved/Textures_WWM"
os.makedirs(output_dir, exist_ok=True)

def generate_curzon_brick():
    print("Generating T_Curzon_Brick_ImperialTerracotta_D...")
    w, h = 2048, 2048
    # Authentic Curzon deep red-oxide brick: #781E17 ~ (120, 30, 23)
    brick_w, brick_h = 128, 48
    mortar = 6
    rows = h // (brick_h + mortar) + 2
    cols = w // (brick_w + mortar) + 2
    
    np.random.seed(42)
    fine_noise = (np.random.randn(h, w) * 12).astype(np.int16)
    
    img = Image.new("RGB", (w, h), color=(185, 175, 160)) # Aged lime mortar
    draw = ImageDraw.Draw(img)
    
    colors = [
        (128, 32, 24), # Classic deep terracotta red
        (115, 26, 18), # Dark burnt red-oxide
        (138, 38, 28), # Rich vibrant red
        (108, 24, 16), # Heavy kiln fired
        (122, 30, 22), # Standard Curzon brick
    ]
    probs = [0.35, 0.25, 0.20, 0.10, 0.10]
    
    for r in range(rows):
        y1 = r * (brick_h + mortar)
        y2 = y1 + brick_h
        offset = (brick_w // 2) if (r % 2 == 1) else 0
        for c in range(-1, cols + 1):
            x1 = c * (brick_w + mortar) + offset
            x2 = x1 + brick_w
            idx = np.random.choice(len(colors), p=probs)
            variation = colors[idx]
            draw.rectangle([x1, y1, x2, y2], fill=variation)
    
    # Convert to numpy and add granular clay noise
    arr = np.array(img, dtype=np.int16)
    for ch in range(3):
        arr[:, :, ch] = np.clip(arr[:, :, ch] + fine_noise, 0, 255)
    
    weathered = arr.astype(np.uint8)
    out_img = Image.fromarray(weathered)
    out_img.save(os.path.join(output_dir, "T_Curzon_Brick_ImperialTerracotta_D.png"))
    print("Saved T_Curzon_Brick_ImperialTerracotta_D.png")

    # Generate matching Normal Map
    print("Generating T_Curzon_Brick_ImperialTerracotta_N...")
    gray = np.mean(weathered, axis=2).astype(np.float32)
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[:, 1:-1] = (gray[:, 2:] - gray[:, :-2]) * 0.5
    gy[1:-1, :] = (gray[2:, :] - gray[:-2, :]) * 0.5
    
    scale = 2.5
    nx = -gx * scale
    ny = -gy * scale
    nz = 255.0
    
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = (nx / norm * 127.5 + 127.5).astype(np.uint8)
    ny = (ny / norm * 127.5 + 127.5).astype(np.uint8)
    nz = (nz / norm * 127.5 + 127.5).astype(np.uint8)
    
    normal_img = Image.fromarray(np.stack([nx, ny, nz], axis=2))
    normal_img.save(os.path.join(output_dir, "T_Curzon_Brick_ImperialTerracotta_N.png"))
    print("Saved T_Curzon_Brick_ImperialTerracotta_N.png")

def generate_curzon_entrance_door():
    print("Generating T_Curzon_EntranceDoor_ColonialTeak_D...")
    w, h = 2048, 2048
    img = Image.new("RGB", (w, h), color=(122, 30, 22)) # Deep red terracotta surround
    draw = ImageDraw.Draw(img)
    
    # 1. Ivory Stone Archway Frame
    draw.rectangle([80, 80, 1968, 2048], fill=(225, 218, 202))
    draw.rectangle([160, 180, 1888, 2048], fill=(42, 28, 20)) # Dark teak door frame
    
    # 2. Upper Arched Fanlight
    draw.pieslice([200, 200, 1848, 1200], start=180, end=360, fill=(32, 54, 70))
    cx, cy = 1024, 700
    for deg in range(195, 360, 20):
        rad = np.radians(deg)
        x2 = int(cx + 800 * np.cos(rad))
        y2 = int(cy + 800 * np.sin(rad))
        draw.line([cx, cy, x2, y2], fill=(62, 42, 30), width=18)
    
    # 3. Main Double-Leaf Doors
    mid = 1024
    door_y_start = 720
    draw.rectangle([200, door_y_start, mid - 10, 2048], fill=(48, 32, 22))
    draw.rectangle([mid + 10, door_y_start, 1848, 2048], fill=(46, 30, 20))
    draw.rectangle([mid - 14, door_y_start, mid + 14, 2048], fill=(36, 22, 14))
    
    panel_heights = [(760, 1020), (1060, 1340), (1380, 1680), (1720, 2000)]
    for y1, y2 in panel_heights:
        # Left leaf panel
        draw.rectangle([260, y1, mid - 60, y2], fill=(38, 24, 16), outline=(78, 54, 38), width=12)
        draw.rectangle([285, y1 + 20, mid - 85, y2 - 20], fill=(54, 36, 24))
        # Right leaf panel
        draw.rectangle([mid + 60, y1, 1788, y2], fill=(38, 24, 16), outline=(78, 54, 38), width=12)
        draw.rectangle([mid + 85, y1 + 20, 1763, y2 - 20], fill=(54, 36, 24))
    
    # 4. Ornate Brass Door Knockers & Handles
    draw.ellipse([mid - 70, 1350, mid - 30, 1390], fill=(212, 168, 64), outline=(130, 96, 32), width=3)
    draw.ellipse([mid + 30, 1350, mid + 70, 1390], fill=(212, 168, 64), outline=(130, 96, 32), width=3)
    
    img.save(os.path.join(output_dir, "T_Curzon_EntranceDoor_ColonialTeak_D.png"))
    print("Saved T_Curzon_EntranceDoor_ColonialTeak_D.png")

    # Generate door normal map
    gray = np.mean(np.array(img), axis=2).astype(np.float32)
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[:, 1:-1] = (gray[:, 2:] - gray[:, :-2]) * 0.5
    gy[1:-1, :] = (gray[2:, :] - gray[:-2, :]) * 0.5
    
    scale = 3.0
    nx = -gx * scale
    ny = -gy * scale
    nz = 255.0
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx = (nx / norm * 127.5 + 127.5).astype(np.uint8)
    ny = (ny / norm * 127.5 + 127.5).astype(np.uint8)
    nz = (nz / norm * 127.5 + 127.5).astype(np.uint8)
    normal_img = Image.fromarray(np.stack([nx, ny, nz], axis=2))
    normal_img.save(os.path.join(output_dir, "T_Curzon_EntranceDoor_ColonialTeak_N.png"))
    print("Saved T_Curzon_EntranceDoor_ColonialTeak_N.png")

if __name__ == "__main__":
    generate_curzon_brick()
    generate_curzon_entrance_door()
