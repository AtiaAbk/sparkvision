#!/usr/bin/env python3
"""
Procedural Super-Natural Foliage & Bark PBR Texture Generator
Creates high-fidelity 1024x1024 leaf branch cards and gnarled bark maps using Blender Python & NumPy:
1. T_Leaf_Raintree_D (Compound pinnate leaflets with vein relief & organic color variation)
2. T_Leaf_Raintree_N (Normal map with beveled leaflet pillows and rachis stem)
3. T_Leaf_Krishnachura_D & N (Flaming wuxia scarlet blossom petals & fern leaflets)
4. T_Leaf_Banyan_D & N (Broad glossy tropical ficus leaves with pale veins)
5. T_Bark_Gnarled_D & N (Deeply furrowed organic tree bark with lichen & moss)
6. T_Foliage_Fern_D & N (Feathered undergrowth fern frond)
"""

import os
import sys
import numpy as np

def create_foliage_textures():
    import bpy

    out_dir = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_NaturalFoliage"
    os.makedirs(out_dir, exist_ok=True)
    res = 1024

    print(f"Generating Natural Foliage PBR Textures at {res}x{res}...")

    # Coordinate grids normalized to [0, 1]
    u = np.linspace(0.0, 1.0, res, endpoint=False)
    v = np.linspace(0.0, 1.0, res, endpoint=False)
    gx, gy = np.meshgrid(u, v) # gy = 0 at top, 1 at bottom in standard image coords

    def save_rgba_image(name, rgba_array):
        filepath = os.path.join(out_dir, f"{name}.png")
        img = bpy.data.images.new(name, width=res, height=res, alpha=True, float_buffer=False)
        # Blender expects pixels as flat float array bottom-to-top
        # Flip Y to match Blender image orientation
        flipped = np.flipud(rgba_array)
        img.pixels.foreach_set(flipped.ravel())
        img.filepath_raw = filepath
        img.file_format = 'PNG'
        img.save()
        print(f"  ✓ Saved {name}.png ({os.path.getsize(filepath) / 1024.0:.1f} KB)")
        return filepath

    def compute_normal_map(height_map, strength=4.0):
        dzdx = (np.roll(height_map, -1, axis=1) - np.roll(height_map, 1, axis=1)) * strength
        dzdy = (np.roll(height_map, -1, axis=0) - np.roll(height_map, 1, axis=0)) * strength
        nz = np.ones((res, res), dtype=np.float32)
        len_inv = 1.0 / np.sqrt(dzdx**2 + dzdy**2 + nz**2 + 1e-6)
        nx = (-dzdx * len_inv) * 0.5 + 0.5
        ny = (-dzdy * len_inv) * 0.5 + 0.5
        nz = (nz * len_inv) * 0.5 + 0.5
        return np.clip(np.stack([nx, ny, nz, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)

    # -------------------------------------------------------------
    # 1. RAINTREE COMPOUND LEAF BRANCH CARD (Matching Ref Image 3)
    # -------------------------------------------------------------
    print("[1/5] Synthesizing Raintree Compound Leaf Branch Card...")
    # Central rachis (stem) runs from (0.5, 0.95) to (0.5, 0.15)
    stem_x = 0.50 + 0.02 * np.sin(gy * 3.5)
    dist_stem = np.abs(gx - stem_x)
    stem_mask = (dist_stem < 0.008) & (gy >= 0.15) & (gy <= 0.95)

    leaf_mask = np.zeros((res, res), dtype=np.float32)
    leaf_height = np.zeros((res, res), dtype=np.float32)
    leaf_color_r = np.zeros((res, res), dtype=np.float32)
    leaf_color_g = np.zeros((res, res), dtype=np.float32)
    leaf_color_b = np.zeros((res, res), dtype=np.float32)

    # Pairs of pinnate compound leaflets
    np.random.seed(101)
    num_pairs = 12
    for i in range(num_pairs):
        t = i / float(num_pairs - 1)
        py = 0.22 + t * 0.65
        leaf_len = 0.16 * (1.0 - 0.35 * (1.0 - t)**2)
        leaf_width = 0.048 * (1.0 - 0.2 * t)

        for side in [-1.0, 1.0]:
            angle = side * (0.35 + 0.25 * (1.0 - t))
            px = stem_x[int(py * res), int(0.5 * res)]
            
            # Local coordinates along leaflet axis
            dx = gx - px
            dy = gy - py
            cos_a = np.cos(angle)
            sin_a = np.sin(angle)
            lx = (dx * cos_a + dy * sin_a) * side
            ly = -dx * sin_a + dy * cos_a

            # Elliptical leaf shape
            in_leaf = (lx >= 0.0) & (lx <= leaf_len) & ((ly / leaf_width)**2 <= (1.0 - (lx / leaf_len - 0.5)**2 * 3.0))
            if np.any(in_leaf):
                # Normalized distance from center
                norm_d = np.clip(1.0 - np.sqrt((lx/leaf_len - 0.4)**2 * 3.0 + (ly/leaf_width)**2), 0.0, 1.0)
                leaf_mask[in_leaf] = 1.0
                leaf_height[in_leaf] = np.maximum(leaf_height[in_leaf], norm_d[in_leaf] * 0.8)

                # Color variation: Natural tropical foliage gradient
                # Base green: RGB ~ (0.16, 0.46, 0.10) to sunlit yellow-green (0.28, 0.58, 0.12)
                variation = np.random.uniform(-0.04, 0.05)
                sun_tint = (1.0 - py) * 0.12 # Leaves higher up are lighter yellow-green
                leaf_color_r[in_leaf] = 0.16 + sun_tint + variation
                leaf_color_g[in_leaf] = 0.45 + sun_tint * 1.2 + variation
                leaf_color_b[in_leaf] = 0.09 + sun_tint * 0.4

    # Terminal leaflet at tip
    tip_dx = gx - stem_x[int(0.15 * res), int(0.5 * res)]
    tip_dy = gy - 0.15
    tip_in = (np.abs(tip_dx) <= 0.04) & (tip_dy <= 0.0) & (tip_dy >= -0.12) & ((tip_dx / 0.04)**2 + (tip_dy / 0.12)**2 <= 1.0)
    leaf_mask[tip_in] = 1.0
    leaf_height[tip_in] = 0.8
    leaf_color_r[tip_in] = 0.26
    leaf_color_g[tip_in] = 0.56
    leaf_color_b[tip_in] = 0.12

    # Add stem
    stem_mask_f = stem_mask.astype(np.float32)
    leaf_color_r[stem_mask] = 0.28
    leaf_color_g[stem_mask] = 0.26
    leaf_color_b[stem_mask] = 0.16
    leaf_mask = np.maximum(leaf_mask, stem_mask_f)
    leaf_height = np.maximum(leaf_height, stem_mask_f * 0.6)

    # Texture diffuse & normal
    raintree_d = np.stack([leaf_color_r, leaf_color_g, leaf_color_b, leaf_mask], axis=-1).astype(np.float32)
    save_rgba_image("T_Leaf_Raintree_D", raintree_d)
    save_rgba_image("T_Leaf_Raintree_N", compute_normal_map(leaf_height, strength=4.5))

    # -------------------------------------------------------------
    # 2. KRISHNACHURA FLAMING RED BLOSSOM & FOLIAGE (Matching Ref 1)
    # -------------------------------------------------------------
    print("[2/5] Synthesizing Krishnachura Wuxia Scarlet Blossom & Foliage...")
    # Scarlet red blossom petals intermixed with delicate fern-green leaves
    k_mask = np.zeros((res, res), dtype=np.float32)
    k_height = np.zeros((res, res), dtype=np.float32)
    k_r = np.zeros((res, res), dtype=np.float32)
    k_g = np.zeros((res, res), dtype=np.float32)
    k_b = np.zeros((res, res), dtype=np.float32)

    # Cluster of 5-petaled flowers
    np.random.seed(202)
    flower_centers = [
        (0.50, 0.40, 0.18), (0.35, 0.55, 0.16), (0.65, 0.52, 0.16),
        (0.42, 0.25, 0.15), (0.58, 0.28, 0.14), (0.28, 0.38, 0.13),
        (0.72, 0.38, 0.13), (0.50, 0.68, 0.15)
    ]
    for fcx, fcy, frad in flower_centers:
        for p in range(5):
            pang = p * (2.0 * np.pi / 5.0) + np.random.uniform(-0.1, 0.1)
            plen = frad * np.random.uniform(0.9, 1.1)
            pw = frad * 0.45
            
            p_dx = gx - fcx
            p_dy = gy - fcy
            plx = p_dx * np.cos(pang) + p_dy * np.sin(pang)
            ply = -p_dx * np.sin(pang) + p_dy * np.cos(pang)

            in_petal = (plx >= 0.0) & (plx <= plen) & ((ply / pw)**2 <= (1.0 - (plx / plen - 0.5)**2 * 3.5))
            if np.any(in_petal):
                k_mask[in_petal] = 1.0
                k_height[in_petal] = np.maximum(k_height[in_petal], 0.85)
                # Vibrant Scarlet / Flame Orange-Red (Ref 1 aesthetic)
                k_r[in_petal] = np.random.uniform(0.85, 0.95)
                k_g[in_petal] = np.random.uniform(0.12, 0.22)
                k_b[in_petal] = np.random.uniform(0.04, 0.08)

        # Flower golden stamen center
        dist_c = np.sqrt((gx - fcx)**2 + (gy - fcy)**2)
        in_c = dist_c < (frad * 0.18)
        k_mask[in_c] = 1.0
        k_height[in_c] = 1.0
        k_r[in_c] = 0.95
        k_g[in_c] = 0.80
        k_b[in_c] = 0.15

    # Green feather leaves in the background of flowers
    bg_green = (leaf_mask > 0.5) & (k_mask < 0.5)
    k_mask[bg_green] = 1.0
    k_height[bg_green] = leaf_height[bg_green] * 0.7
    k_r[bg_green] = leaf_color_r[bg_green] * 0.9
    k_g[bg_green] = leaf_color_g[bg_green] * 0.9
    k_b[bg_green] = leaf_color_b[bg_green] * 0.9

    krishnachura_d = np.stack([k_r, k_g, k_b, k_mask], axis=-1).astype(np.float32)
    save_rgba_image("T_Leaf_Krishnachura_D", krishnachura_d)
    save_rgba_image("T_Leaf_Krishnachura_N", compute_normal_map(k_height, strength=4.0))

    # -------------------------------------------------------------
    # 3. BANYAN GLOSSY FICUS LEAF BRANCH CARD (Matching Ref 2)
    # -------------------------------------------------------------
    print("[3/5] Synthesizing Banyan Glossy Tropical Foliage...")
    b_mask = np.zeros((res, res), dtype=np.float32)
    b_height = np.zeros((res, res), dtype=np.float32)
    b_r = np.zeros((res, res), dtype=np.float32)
    b_g = np.zeros((res, res), dtype=np.float32)
    b_b = np.zeros((res, res), dtype=np.float32)

    # Broad, elliptical glossy leaves with prominent central vein
    np.random.seed(303)
    banyan_leaves = [
        (0.50, 0.45, 0.28, 0.13, 0.0),
        (0.32, 0.65, 0.24, 0.11, -0.4),
        (0.68, 0.62, 0.25, 0.12, 0.42),
        (0.25, 0.35, 0.22, 0.10, -0.75),
        (0.75, 0.32, 0.23, 0.11, 0.72),
        (0.50, 0.18, 0.20, 0.09, 0.08)
    ]
    for blx, bly, blen, bw, bang in banyan_leaves:
        dx = gx - blx
        dy = gy - bly
        lx = dx * np.cos(bang) + dy * np.sin(bang)
        ly = -dx * np.sin(bang) + dy * np.cos(bang)

        in_bl = (lx >= -blen*0.5) & (lx <= blen*0.5) & ((ly / bw)**2 <= (1.0 - (lx / (blen*0.5))**2))
        if np.any(in_bl):
            norm_d = np.clip(1.0 - np.sqrt((lx/(blen*0.5))**2 + (ly/bw)**2), 0.0, 1.0)
            b_mask[in_bl] = 1.0
            b_height[in_bl] = np.maximum(b_height[in_bl], norm_d[in_bl])

            # Deep rich emerald green (0.10, 0.32, 0.08)
            b_r[in_bl] = 0.09 + np.random.uniform(-0.02, 0.02)
            b_g[in_bl] = 0.32 + np.random.uniform(-0.03, 0.04)
            b_b[in_bl] = 0.06

            # Pale ivory central midrib
            midrib = in_bl & (np.abs(ly) < 0.005)
            b_r[midrib] = 0.35
            b_g[midrib] = 0.48
            b_b[midrib] = 0.20
            b_height[midrib] = np.maximum(b_height[midrib], 0.9)

    banyan_d = np.stack([b_r, b_g, b_b, b_mask], axis=-1).astype(np.float32)
    save_rgba_image("T_Leaf_Banyan_D", banyan_d)
    save_rgba_image("T_Leaf_Banyan_N", compute_normal_map(b_height, strength=4.0))

    # -------------------------------------------------------------
    # 4. GNARLED TREE BARK PBR (Organic Old Heritage Trunk, Ref 2)
    # -------------------------------------------------------------
    print("[4/5] Synthesizing Gnarled Heritage Tree Bark PBR...")
    np.random.seed(404)
    # Vertical fibrous ridges with organic turbulence
    turb = np.sin(gy * 24.0 + np.sin(gx * 12.0) * 2.0) * 0.25
    ridges = np.sin((gx + turb) * 48.0) * 0.5 + 0.5
    fissures = (ridges < 0.28).astype(np.float32)

    bark_noise = np.random.normal(0.0, 0.08, (res, res)).astype(np.float32)
    bark_h = np.clip(ridges + bark_noise * 0.3 - fissures * 0.4, 0.0, 1.0)

    # Warm weathered walnut brown with grey-green lichen patches
    bark_r = 0.24 + bark_h * 0.12 - fissures * 0.10
    bark_g = 0.18 + bark_h * 0.09 - fissures * 0.08
    bark_b = 0.12 + bark_h * 0.06 - fissures * 0.05

    # Lichen / Moss accents in crevices
    moss_mask = (fissures > 0.5) & (np.random.uniform(0.0, 1.0, (res, res)) < 0.45)
    bark_r[moss_mask] = 0.18
    bark_g[moss_mask] = 0.28
    bark_b[moss_mask] = 0.10

    bark_d = np.clip(np.stack([bark_r, bark_g, bark_b, np.ones((res, res))], axis=-1), 0.0, 1.0).astype(np.float32)
    save_rgba_image("T_Bark_Gnarled_D", bark_d)
    save_rgba_image("T_Bark_Gnarled_N", compute_normal_map(bark_h, strength=5.5))

    # -------------------------------------------------------------
    # 5. UNDERGROWTH FERN FROND (Matching Ref 1 Foreground)
    # -------------------------------------------------------------
    print("[5/5] Synthesizing Undergrowth Fern Frond...")
    fern_mask = np.zeros((res, res), dtype=np.float32)
    fern_height = np.zeros((res, res), dtype=np.float32)
    fern_r = np.zeros((res, res), dtype=np.float32)
    fern_g = np.zeros((res, res), dtype=np.float32)
    fern_b = np.zeros((res, res), dtype=np.float32)

    # Arched rachis from (0.5, 0.95) to (0.28, 0.10)
    fr_y = np.linspace(0.10, 0.95, res)
    fr_x = 0.50 - 0.22 * (1.0 - fr_y)**1.8

    for y_idx in range(len(fr_y)):
        cy = fr_y[y_idx]
        cx = fr_x[y_idx]
        t = (cy - 0.10) / 0.85 # 0 at tip, 1 at base
        pinna_len = 0.28 * np.sin(t * np.pi) # Widest in middle
        pinna_w = 0.016

        for side in [-1.0, 1.0]:
            p_ang = side * (0.65 - 0.25 * t)
            dx = gx - cx
            dy = gy - cy
            plx = (dx * np.cos(p_ang) + dy * np.sin(p_ang)) * side
            ply = -dx * np.sin(p_ang) + dy * np.cos(p_ang)

            in_p = (plx >= 0.0) & (plx <= pinna_len) & (np.abs(ply) <= pinna_w * (1.0 - plx/pinna_len))
            if np.any(in_p):
                fern_mask[in_p] = 1.0
                fern_height[in_p] = 0.75
                # Vivid emerald fern green
                fern_r[in_p] = 0.12 + (1.0 - t) * 0.08
                fern_g[in_p] = 0.44 + (1.0 - t) * 0.14
                fern_b[in_p] = 0.08

    fern_d = np.stack([fern_r, fern_g, fern_b, fern_mask], axis=-1).astype(np.float32)
    save_rgba_image("T_Foliage_Fern_D", fern_d)
    save_rgba_image("T_Foliage_Fern_N", compute_normal_map(fern_height, strength=4.0))

    print("\n✓ ALL 5 PBR FOLIAGE TEXTURE SETS SUCCESSFULLY SYNTHESIZED!")

if __name__ == "__main__":
    create_foliage_textures()
