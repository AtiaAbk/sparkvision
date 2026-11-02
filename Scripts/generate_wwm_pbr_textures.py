#!/usr/bin/env python3
"""
Where Winds Meet Aesthetic PBR Texture Generator for SparkVision (Dhaka University)
Generates high-fidelity 1024x1024 PBR texture maps using Blender's Python & NumPy:
1. T_Curzon_Brick_D (Terracotta Red Brick with burnt clay variation & mortar)
2. T_Curzon_Brick_N (Tangent Normal map with beveled brick edges & porous noise)
3. T_Curzon_Brick_ORM (Packed Ambient Occlusion, Roughness, Metallic)
4. T_Curzon_StonePaving_D & N (Heritage stone walkways & flags)
5. T_Water_Normal (Organic fluid wave normal map for Curzon Pond)
"""

import os
import sys
import numpy as np

def generate_textures():
    import bpy

    output_dir = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_WWM"
    os.makedirs(output_dir, exist_ok=True)
    res = 1024

    print(f"Generating WWM PBR Textures at {res}x{res}...")

    # -------------------------------------------------------------
    # 1. CURZON BRICK DIFFUSE & HEIGHT
    # -------------------------------------------------------------
    print("Generating Curzon Terracotta Brick...")
    brick_w, brick_h = 128, 48
    mortar_t = 6

    u = np.linspace(0, res, res, endpoint=False)
    v = np.linspace(0, res, res, endpoint=False)
    grid_x, grid_y = np.meshgrid(u, v)

    row = (grid_y // brick_h).astype(int)
    shifted_x = grid_x + (row % 2) * (brick_w // 2)
    col = (shifted_x // brick_w).astype(int)

    in_brick_x = shifted_x % brick_w
    in_brick_y = grid_y % brick_h

    # Mortar mask
    is_mortar = (in_brick_x < mortar_t) | (in_brick_y < mortar_t)

    # Random brick color variation based on cell hash
    np.random.seed(42)
    cell_hash = np.sin(row * 12.9898 + col * 78.233) * 43758.5453
    cell_var = (cell_hash - np.floor(cell_hash)) * 0.3 - 0.15 # [-0.15, 0.15]

    # Authentic Curzon Terracotta Red Brick Base: RGB ~ (0.54, 0.14, 0.09)
    base_r = 0.52 + cell_var * 0.2
    base_g = 0.13 + cell_var * 0.08
    base_b = 0.08 + cell_var * 0.05

    # Micro surface noise
    noise = np.random.normal(0, 0.03, (res, res))
    base_r += noise
    base_g += noise * 0.5
    base_b += noise * 0.3

    # Mortar color: Historic lime-surki mortar (warm pale grey/buff)
    mortar_noise = np.random.normal(0, 0.02, (res, res))
    base_r[is_mortar] = 0.72 + mortar_noise[is_mortar]
    base_g[is_mortar] = 0.68 + mortar_noise[is_mortar]
    base_b[is_mortar] = 0.60 + mortar_noise[is_mortar]

    diffuse = np.clip(np.stack([base_r, base_g, base_b, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)

    # Save Diffuse
    img_diff = bpy.data.images.new("T_Curzon_Brick_D", width=res, height=res, alpha=True, float_buffer=False)
    img_diff.pixels.foreach_set(diffuse.ravel())
    img_diff.filepath_raw = os.path.join(output_dir, "T_Curzon_Brick_D.png")
    img_diff.file_format = 'PNG'
    img_diff.save()
    print(f"  ✓ Saved {img_diff.filepath_raw}")

    # -------------------------------------------------------------
    # 2. CURZON BRICK NORMAL MAP & ORM
    # -------------------------------------------------------------
    height = np.ones((res, res), dtype=np.float32)
    dist_x = np.minimum(in_brick_x, brick_w - in_brick_x)
    dist_y = np.minimum(in_brick_y, brick_h - in_brick_y)
    dist_edge = np.minimum(dist_x, dist_y)

    # Bevel curve at mortar transition
    height = np.clip(dist_edge / float(mortar_t + 2), 0.0, 1.0)
    height += noise * 0.15
    height = np.clip(height, 0.0, 1.0).astype(np.float32)

    # Compute Sobel / central differences for normal map
    dzdx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * 3.0
    dzdy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * 3.0
    nz = np.ones((res, res), dtype=np.float32)

    length = np.sqrt(dzdx**2 + dzdy**2 + nz**2)
    nx = (-dzdx / length) * 0.5 + 0.5
    ny = (-dzdy / length) * 0.5 + 0.5
    nz = (nz / length) * 0.5 + 0.5

    normal_map = np.clip(np.stack([nx, ny, nz, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)

    img_norm = bpy.data.images.new("T_Curzon_Brick_N", width=res, height=res, alpha=True, float_buffer=False)
    img_norm.pixels.foreach_set(normal_map.ravel())
    img_norm.filepath_raw = os.path.join(output_dir, "T_Curzon_Brick_N.png")
    img_norm.file_format = 'PNG'
    img_norm.save()
    print(f"  ✓ Saved {img_norm.filepath_raw}")

    # ORM Map: R = AO, G = Roughness, B = Metallic
    ao = np.clip(height * 0.6 + 0.4, 0.0, 1.0)
    roughness = np.full((res, res), 0.72, dtype=np.float32) + noise * 0.2
    roughness[is_mortar] = 0.94 # Mortar is chalky and diffuse
    roughness = np.clip(roughness, 0.2, 1.0)
    metallic = np.zeros((res, res), dtype=np.float32)

    orm_map = np.clip(np.stack([ao, roughness, metallic, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)
    img_orm = bpy.data.images.new("T_Curzon_Brick_ORM", width=res, height=res, alpha=True, float_buffer=False)
    img_orm.pixels.foreach_set(orm_map.ravel())
    img_orm.filepath_raw = os.path.join(output_dir, "T_Curzon_Brick_ORM.png")
    img_orm.file_format = 'PNG'
    img_orm.save()
    print(f"  ✓ Saved {img_orm.filepath_raw}")

    # -------------------------------------------------------------
    # 3. WATER NORMAL MAP (DUAL GERSTNER RIPPLES)
    # -------------------------------------------------------------
    print("Generating Curzon Pond Water Normal Map...")
    kx1, ky1 = 2.0 * np.pi / 128.0, 2.0 * np.pi / 256.0
    kx2, ky2 = -2.0 * np.pi / 96.0, 2.0 * np.pi / 160.0
    kx3, ky3 = 2.0 * np.pi / 64.0, -2.0 * np.pi / 64.0

    w_height = (
        np.sin(kx1 * grid_x + ky1 * grid_y) * 0.5 +
        np.sin(kx2 * grid_x + ky2 * grid_y + 1.2) * 0.35 +
        np.sin(kx3 * grid_x + ky3 * grid_y + 2.5) * 0.15
    ).astype(np.float32)

    w_dzdx = (np.roll(w_height, -1, axis=1) - np.roll(w_height, 1, axis=1)) * 4.0
    w_dzdy = (np.roll(w_height, -1, axis=0) - np.roll(w_height, 1, axis=0)) * 4.0
    w_nz = np.ones((res, res), dtype=np.float32)

    w_len = np.sqrt(w_dzdx**2 + w_dzdy**2 + w_nz**2)
    w_nx = (-w_dzdx / w_len) * 0.5 + 0.5
    w_ny = (-w_dzdy / w_len) * 0.5 + 0.5
    w_nz = (w_nz / w_len) * 0.5 + 0.5

    water_normal = np.clip(np.stack([w_nx, w_ny, w_nz, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)
    img_w_norm = bpy.data.images.new("T_Water_Normal", width=res, height=res, alpha=True, float_buffer=False)
    img_w_norm.pixels.foreach_set(water_normal.ravel())
    img_w_norm.filepath_raw = os.path.join(output_dir, "T_Water_Normal.png")
    img_w_norm.file_format = 'PNG'
    img_w_norm.save()
    print(f"  ✓ Saved {img_w_norm.filepath_raw}")

    # -------------------------------------------------------------
    # 4. HERITAGE STONE PAVING (DIFFUSE & NORMAL)
    # -------------------------------------------------------------
    print("Generating Heritage Stone Paving...")
    tile_s = 96
    tile_u = (grid_x // tile_s).astype(int)
    tile_v = (grid_y // tile_s).astype(int)
    tile_hash = np.sin(tile_u * 37.1 + tile_v * 91.7) * 43758.5453
    tile_var = (tile_hash - np.floor(tile_hash)) * 0.2 - 0.1

    stone_base = 0.65 + tile_var + noise * 0.8
    stone_is_grout = ((grid_x % tile_s) < 4) | ((grid_y % tile_s) < 4)
    stone_r = stone_base * 0.98
    stone_g = stone_base * 0.95
    stone_b = stone_base * 0.90
    stone_r[stone_is_grout] = 0.45
    stone_g[stone_is_grout] = 0.44
    stone_b[stone_is_grout] = 0.42

    stone_diff = np.clip(np.stack([stone_r, stone_g, stone_b, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)
    img_stone_d = bpy.data.images.new("T_Curzon_StonePaving_D", width=res, height=res, alpha=True, float_buffer=False)
    img_stone_d.pixels.foreach_set(stone_diff.ravel())
    img_stone_d.filepath_raw = os.path.join(output_dir, "T_Curzon_StonePaving_D.png")
    img_stone_d.file_format = 'PNG'
    img_stone_d.save()
    print(f"  ✓ Saved {img_stone_d.filepath_raw}")

    stone_h = np.ones((res, res), dtype=np.float32)
    s_dist_x = np.minimum(grid_x % tile_s, tile_s - (grid_x % tile_s))
    s_dist_y = np.minimum(grid_y % tile_s, tile_s - (grid_y % tile_s))
    stone_h = np.clip(np.minimum(s_dist_x, s_dist_y) / 6.0, 0.0, 1.0) + noise * 0.1

    s_dzdx = (np.roll(stone_h, -1, axis=1) - np.roll(stone_h, 1, axis=1)) * 3.0
    s_dzdy = (np.roll(stone_h, -1, axis=0) - np.roll(stone_h, 1, axis=0)) * 3.0
    s_nz = np.ones((res, res), dtype=np.float32)
    s_len = np.sqrt(s_dzdx**2 + s_dzdy**2 + s_nz**2)

    stone_norm = np.clip(np.stack([(-s_dzdx / s_len) * 0.5 + 0.5, (-s_dzdy / s_len) * 0.5 + 0.5, (s_nz / s_len) * 0.5 + 0.5, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)
    img_stone_n = bpy.data.images.new("T_Curzon_StonePaving_N", width=res, height=res, alpha=True, float_buffer=False)
    img_stone_n.pixels.foreach_set(stone_norm.ravel())
    img_stone_n.filepath_raw = os.path.join(output_dir, "T_Curzon_StonePaving_N.png")
    img_stone_n.file_format = 'PNG'
    img_stone_n.save()
    print(f"  ✓ Saved {img_stone_n.filepath_raw}")

    print("\n✅ All Where Winds Meet PBR Textures successfully generated!")

if __name__ == "__main__":
    generate_textures()
