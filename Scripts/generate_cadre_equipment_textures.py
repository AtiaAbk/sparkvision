#!/usr/bin/env python3
"""
Generate equipment textures for July 2024 Confrontation:
1. T_Cadre_NoukaCap_D.png: Cap with hand-drawn Bengali boat (Nouka) emblem
2. T_Cadre_Helmet_D.png: Black motorcycle helmet texture with reflective visor
3. T_Bamboo_Lathi_D.png & _N.png: Natural Bengali bamboo stick (lathi)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/Content/SparkVision/Textures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_nouka_cap():
    size = 1024
    img = Image.new("RGBA", (size, size), (25, 30, 28, 255)) # Dark green/charcoal fabric
    draw = ImageDraw.Draw(img)

    # Fabric texture noise
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, 10, (size, size, 1))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8))
    draw = ImageDraw.Draw(img)

    # Circular Badge in the center
    cx, cy = size // 2, size // 2 - 40
    badge_radius = 240
    # Gold rim
    draw.ellipse([cx - badge_radius, cy - badge_radius, cx + badge_radius, cy + badge_radius], fill=(212, 175, 55, 255))
    # Inner dark green circle
    inner_r = badge_radius - 14
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=(18, 55, 30, 255))

    # Traditional Bengali Country Boat (Nouka / নৌকা) hand-drawn
    # Hull points (crescent bottom)
    hull_w = 260
    hull_h = 75
    hull_y = cy + 40
    # Draw curved boat hull
    hull_points = []
    for x_offset in range(-hull_w // 2, hull_w // 2 + 1, 4):
        # Quadratic curve for boat bottom
        norm_x = (x_offset / (hull_w // 2))
        y_val = hull_y + int((1.0 - norm_x**2) * 45)
        hull_points.append((cx + x_offset, y_val))
    # Deck top line
    hull_points.append((cx + hull_w // 2, hull_y - 10))
    hull_points.append((cx - hull_w // 2, hull_y - 10))

    # Fill boat hull with warm golden wood
    draw.polygon(hull_points, fill=(235, 195, 80, 255), outline=(255, 230, 140, 255))

    # Canopy / Hood (chhoi / ছই) on the boat
    canopy_w = 110
    canopy_h = 60
    draw.chord([cx - canopy_w // 2, hull_y - 10 - canopy_h, cx + canopy_w // 2, hull_y - 10 + canopy_h // 2],
               start=180, end=0, fill=(220, 160, 60, 255), outline=(255, 220, 120, 255), width=3)

    # Mast & Oar (baitha / বৈঠা)
    draw.line([cx - 30, hull_y - 65, cx - 30, hull_y - 10], fill=(180, 120, 40, 255), width=5)
    # Long steering oar at stern
    draw.line([cx + hull_w // 2 - 10, hull_y + 10, cx + hull_w // 2 + 45, hull_y + 65], fill=(230, 180, 70, 255), width=6)
    draw.ellipse([cx + hull_w // 2 + 35, hull_y + 55, cx + hull_w // 2 + 55, hull_y + 75], fill=(230, 180, 70, 255))

    # Water ripple waves beneath boat
    for i in range(-2, 3):
        wave_y = hull_y + 55 + i * 14
        wave_pts = []
        for x in range(cx - 160, cx + 160, 8):
            wy = wave_y + int(math.sin((x - cx) * 0.08) * 5)
            wave_pts.append((x, wy))
        draw.line(wave_pts, fill=(240, 240, 255, 220), width=3)

    # Badge decorative border stars
    draw.text((cx - 95, cy + badge_radius - 55), "★ BCL SQUAD ★", fill=(240, 220, 120, 255))

    # Visor seam line
    draw.arc([100, size - 260, size - 100, size + 100], start=200, end=340, fill=(40, 45, 42, 255), width=8)

    path = os.path.join(OUTPUT_DIR, "T_Cadre_NoukaCap_D.png")
    img.save(path)
    print(f"Generated Nouka Cap: {path}")

def generate_motorcycle_helmet():
    size = 1024
    img = Image.new("RGBA", (size, size), (22, 24, 28, 255)) # Glossy midnight black
    draw = ImageDraw.Draw(img)

    # Large Visor window in center
    vx1, vy1 = 160, 280
    vx2, vy2 = size - 160, 560
    draw.rounded_rectangle([vx1, vy1, vx2, vy2], radius=45, fill=(12, 14, 18, 255), outline=(80, 85, 95, 255), width=6)

    # Tinted visor glass gradient with reflection slash
    for y in range(vy1 + 10, vy2 - 10):
        t = (y - vy1) / (vy2 - vy1)
        r = int(20 + 35 * (1.0 - t))
        g = int(35 + 50 * (1.0 - t))
        b = int(45 + 75 * (1.0 - t))
        draw.line([vx1 + 10, y, vx2 - 10, y], fill=(r, g, b, 255))

    # Diagonal reflection highlight across visor
    draw.polygon([(vx1 + 120, vy1 + 10), (vx1 + 220, vy1 + 10), (vx1 + 80, vy2 - 10), (vx1, vy2 - 10)],
                 fill=(140, 180, 210, 160))

    # Helmet chin vents & aerodynamic contours
    draw.rectangle([size//2 - 60, vy2 + 40, size//2 + 60, vy2 + 70], fill=(10, 10, 12, 255), outline=(50, 55, 60, 255), width=2)
    for x in range(size//2 - 45, size//2 + 50, 15):
        draw.line([x, vy2 + 45, x, vy2 + 65], fill=(5, 5, 6, 255), width=4)

    # Bold Cadre Red racing stripe along top
    draw.rectangle([size//2 - 30, 40, size//2 + 30, vy1 - 10], fill=(195, 30, 30, 255))
    draw.rectangle([size//2 - 45, 40, size//2 - 35, vy1 - 10], fill=(220, 220, 220, 255))
    draw.rectangle([size//2 + 35, 40, size//2 + 45, vy1 - 10], fill=(220, 220, 220, 255))

    path = os.path.join(OUTPUT_DIR, "T_Cadre_Helmet_D.png")
    img.save(path)
    print(f"Generated Helmet: {path}")

def generate_bamboo_lathi():
    width = 256
    height = 1024
    img = Image.new("RGBA", (width, height), (210, 175, 95, 255)) # Bamboo golden cane
    draw = ImageDraw.Draw(img)

    # Bamboo longitudinal grain noise
    arr = np.array(img, dtype=np.float32)
    v_lines = np.random.normal(0, 12, (1, width, 1))
    arr[:, :, :3] += v_lines * 0.7
    noise = np.random.normal(0, 6, (height, width, 1))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8))
    draw = ImageDraw.Draw(img)

    # Bamboo Segment Nodes (rings every 180 pixels)
    node_positions = [120, 310, 500, 690, 880]
    height_map = np.zeros((height, width), dtype=np.float32)

    for ny in node_positions:
        # Dark node ring line
        draw.line([0, ny, width, ny], fill=(110, 80, 40, 255), width=4)
        draw.line([0, ny - 3, width, ny - 3], fill=(240, 215, 140, 255), width=2)
        draw.line([0, ny + 4, width, ny + 4], fill=(140, 105, 55, 255), width=3)

        # Height bump for normal map
        for dy in range(-12, 13):
            val = (1.0 - abs(dy) / 12.0) * 0.8
            y_coord = np.clip(ny + dy, 0, height - 1)
            height_map[y_coord, :] += val

    diffuse_path = os.path.join(OUTPUT_DIR, "T_Bamboo_Lathi_D.png")
    img.save(diffuse_path)
    print(f"Generated Bamboo Diffuse: {diffuse_path}")

    # Generate Normal Map from height map
    grad_y, grad_x = np.gradient(height_map)
    normal = np.zeros((height, width, 4), dtype=np.uint8)
    # X = -grad_x, Y = -grad_y, Z = 1.0
    nx = np.clip((-grad_x * 4.0 + 1.0) * 0.5 * 255, 0, 255).astype(np.uint8)
    ny_map = np.clip((-grad_y * 4.0 + 1.0) * 0.5 * 255, 0, 255).astype(np.uint8)
    nz = np.full((height, width), 245, dtype=np.uint8)
    normal[:, :, 0] = nx
    normal[:, :, 1] = ny_map
    normal[:, :, 2] = nz
    normal[:, :, 3] = 255

    norm_img = Image.fromarray(normal)
    norm_path = os.path.join(OUTPUT_DIR, "T_Bamboo_Lathi_N.png")
    norm_img.save(norm_path)
    print(f"Generated Bamboo Normal: {norm_path}")

if __name__ == "__main__":
    generate_nouka_cap()
    generate_motorcycle_helmet()
    generate_bamboo_lathi()
