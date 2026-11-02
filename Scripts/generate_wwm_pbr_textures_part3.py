#!/usr/bin/env python3
"""
Where Winds Meet Aesthetic PBR Texture Generator - Part 3
Generates high-fidelity 1024x1024 PBR textures for:
1. T_Debdaru_Leaf_D & N (deep lustrous dark emerald green foliage for weeping mast trees)
2. T_Ribbon_Window_D & N (architectural ribbon windows with mullions and tinted glazing)
3. T_Road_Asphalt_D & N (weathered DU campus bitumen roadway with micro-aggregate)
4. T_Shaheed_Marble_D & N (pure white polished marble altar with delicate grey veining)
5. T_Curzon_CastIron_D & N (historic wrought black iron with subtle hammer pitting)
6. T_Supporting_Building_D & N (architectural red brick and concrete floorplate facade)
7. T_WaterLily_Pad_D & N (waxy lotus pad with radial vein relief)
"""

import os
import sys
import numpy as np

def generate_textures():
    import bpy

    output_dir = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_WWM"
    os.makedirs(output_dir, exist_ok=True)
    res = 1024

    u = np.linspace(0, 1, res, endpoint=False)
    v = np.linspace(0, 1, res, endpoint=False)
    gx, gy = np.meshgrid(u, v)

    def save_tex(name, rgba):
        rgba = np.clip(rgba, 0.0, 1.0).astype(np.float32)
        img = bpy.data.images.new(name, width=res, height=res, alpha=True, float_buffer=False)
        img.pixels.foreach_set(rgba.ravel())
        img.filepath_raw = os.path.join(output_dir, f"{name}.png")
        img.file_format = 'PNG'
        img.save()
        print(f"  ✓ Saved {img.filepath_raw}")

    def height_to_normal(height, strength=4.0):
        gx_g = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * strength
        gy_g = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * strength
        gz_g = np.ones_like(height)
        norm = np.sqrt(gx_g**2 + gy_g**2 + gz_g**2)
        nx = 0.5 - 0.5 * (gx_g / norm)
        ny = 0.5 - 0.5 * (gy_g / norm)
        nz = 0.5 + 0.5 * (gz_g / norm)
        return np.stack([nx, ny, nz, np.ones_like(height)], axis=-1)

    print("=" * 60)
    print(f"Generating WWM PBR Textures Part 3 ({res}x{res})...")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. DEBDARU COLUMNAR FOLIAGE (Polyalthia longifolia)
    # Deep, glossy forest emerald green with dense overlapping lanceolate leaves
    # -------------------------------------------------------------
    print("Generating Debdaru Foliage...")
    np.random.seed(301)
    noise_leaf = np.sin(gx * 60.0 + np.sin(gy * 80.0) * 1.5) * np.cos(gy * 70.0)
    grain = np.random.normal(0, 0.03, (res, res))
    height_deb = noise_leaf * 0.15 + grain
    
    # Base dark lustrous emerald: R:0.04-0.08, G:0.18-0.28, B:0.06-0.12
    r_deb = 0.06 + 0.03 * noise_leaf + grain * 0.02
    g_deb = 0.22 + 0.08 * noise_leaf + grain * 0.04
    b_deb = 0.08 + 0.04 * noise_leaf + grain * 0.02
    deb_diff = np.stack([r_deb, g_deb, b_deb, np.ones_like(r_deb)], axis=-1)
    save_tex("T_Debdaru_Leaf_D", deb_diff)
    save_tex("T_Debdaru_Leaf_N", height_to_normal(height_deb, strength=3.5))

    # -------------------------------------------------------------
    # 2. RIBBON WINDOWS (Modernist academic block glazing)
    # Horizontal glass ribbons, dark bronze/charcoal mullions, subtle sky reflection
    # -------------------------------------------------------------
    print("Generating Ribbon Window...")
    # Repeat pattern: 8 window panes horizontally, 4 floors vertically
    panes_x = (gx * 8.0) % 1.0
    panes_y = (gy * 4.0) % 1.0
    mullion_mask = (panes_x < 0.06) | (panes_x > 0.94) | (panes_y < 0.08) | (panes_y > 0.92)
    
    # Glass pane: deep reflective twilight cyan-black with subtle gradient
    r_win = np.where(mullion_mask, 0.08, 0.12 + 0.04 * panes_y)
    g_win = np.where(mullion_mask, 0.08, 0.18 + 0.05 * panes_y)
    b_win = np.where(mullion_mask, 0.10, 0.24 + 0.06 * panes_y)
    win_diff = np.stack([r_win, g_win, b_win, np.ones_like(r_win)], axis=-1)
    
    # Mullion frames pop out in height map
    height_win = np.where(mullion_mask, 0.25, 0.0)
    save_tex("T_Ribbon_Window_D", win_diff)
    save_tex("T_Ribbon_Window_N", height_to_normal(height_win, strength=6.0))

    # -------------------------------------------------------------
    # 3. ROADWAY BITUMEN ASPHALT (Curzon to Doyel Chattar & Fuller Rd)
    # Weathered dark grey asphalt with crushed basalt aggregate & fine tire polishing
    # -------------------------------------------------------------
    print("Generating Road Asphalt...")
    np.random.seed(302)
    agg_fine = np.random.normal(0, 0.06, (res, res))
    agg_coarse = np.sin(gx * 120.0) * np.cos(gy * 120.0) * 0.04
    wear_track = np.exp(-((gx - 0.5) ** 2) / 0.1) * 0.03
    height_road = agg_fine + agg_coarse
    
    base_lum = 0.18 + agg_fine * 0.5 + wear_track
    r_road = base_lum * 0.95
    g_road = base_lum * 0.96
    b_road = base_lum * 1.00 # slight cool blue-grey asphalt tone
    road_diff = np.stack([r_road, g_road, b_road, np.ones_like(r_road)], axis=-1)
    save_tex("T_Road_Asphalt_D", road_diff)
    save_tex("T_Road_Asphalt_N", height_to_normal(height_road, strength=4.5))

    # -------------------------------------------------------------
    # 4. SHAHEED MINAR PRISTINE WHITE MARBLE
    # Crystalline Makarana marble, warm ivory white with fine grey dolomite veining
    # -------------------------------------------------------------
    print("Generating Shaheed Marble...")
    np.random.seed(303)
    vein1 = np.sin(gx * 12.0 + gy * 18.0 + np.sin(gx * 25.0) * 1.2)
    vein2 = np.cos(gx * 30.0 - gy * 15.0 + np.cos(gy * 20.0) * 0.8)
    vein_mask = np.exp(-(vein1**2) * 8.0) * 0.18 + np.exp(-(vein2**2) * 14.0) * 0.12
    marble_base = 0.94 - vein_mask
    
    r_mrb = marble_base * 0.98
    g_mrb = marble_base * 0.97
    b_mrb = marble_base * 0.95 # warm ivory
    mrb_diff = np.stack([r_mrb, g_mrb, b_mrb, np.ones_like(r_mrb)], axis=-1)
    height_mrb = np.random.normal(0, 0.015, (res, res)) - vein_mask * 0.05
    save_tex("T_Shaheed_Marble_D", mrb_diff)
    save_tex("T_Shaheed_Marble_N", height_to_normal(height_mrb, strength=2.5))

    # -------------------------------------------------------------
    # 5. CURZON CAST IRON (Ornamental gates, boundary grilles, finials)
    # Hammered black iron with charcoal micro-relief and bronze edge highlights
    # -------------------------------------------------------------
    print("Generating Cast Iron...")
    np.random.seed(304)
    pit_noise = np.random.normal(0, 0.08, (res, res))
    height_iron = pit_noise * 0.12
    r_iron = 0.09 + pit_noise * 0.02
    g_iron = 0.09 + pit_noise * 0.02
    b_iron = 0.10 + pit_noise * 0.02
    iron_diff = np.stack([r_iron, g_iron, b_iron, np.ones_like(r_iron)], axis=-1)
    save_tex("T_Curzon_CastIron_D", iron_diff)
    save_tex("T_Curzon_CastIron_N", height_to_normal(height_iron, strength=4.0))

    # -------------------------------------------------------------
    # 6. SUPPORTING CAMPUS BUILDING FACADE (Colonial/Modernist background)
    # Dhaka red-brick piers, lime mortar joints, horizontal concrete spandrels
    # -------------------------------------------------------------
    print("Generating Supporting Building Facade...")
    brick_x = (gx * 32.0) % 1.0
    brick_y = (gy * 64.0) % 1.0
    mortar = (brick_x < 0.08) | (brick_y < 0.08)
    spandrel = ((gy * 8.0) % 1.0) < 0.18 # concrete floor bands
    
    r_bld = np.where(spandrel, 0.72, np.where(mortar, 0.78, 0.52))
    g_bld = np.where(spandrel, 0.68, np.where(mortar, 0.75, 0.22))
    b_bld = np.where(spandrel, 0.62, np.where(mortar, 0.70, 0.15))
    bld_diff = np.stack([r_bld, g_bld, b_bld, np.ones_like(r_bld)], axis=-1)
    height_bld = np.where(spandrel, 0.2, np.where(mortar, 0.0, 0.12))
    save_tex("T_Supporting_Building_D", bld_diff)
    save_tex("T_Supporting_Building_N", height_to_normal(height_bld, strength=5.0))

    # -------------------------------------------------------------
    # 7. WATER LILY / SHAPLA PADS (Curzon pond floating flora)
    # Waxy emerald pad with radial vein bifurcation and notched edge
    # -------------------------------------------------------------
    print("Generating Water Lily Pad...")
    cx, cy = gx - 0.5, gy - 0.5
    radius = np.sqrt(cx**2 + cy**2) * 2.0
    angle = np.arctan2(cy, cx)
    radial_veins = np.cos(angle * 16.0) * 0.08 * (1.0 - radius)
    pad_mask = radius <= 0.95
    notch = (np.abs(angle) < 0.18) & (radius > 0.05)
    pad_mask = pad_mask & (~notch)
    
    r_pad = np.where(pad_mask, 0.10 + radial_veins * 0.5, 0.0)
    g_pad = np.where(pad_mask, 0.38 + radial_veins * 1.0, 0.0)
    b_pad = np.where(pad_mask, 0.14 + radial_veins * 0.4, 0.0)
    a_pad = np.where(pad_mask, 1.0, 0.0)
    pad_diff = np.stack([r_pad, g_pad, b_pad, a_pad], axis=-1)
    height_pad = np.where(pad_mask, radial_veins + 0.15, 0.0)
    save_tex("T_WaterLily_Pad_D", pad_diff)
    save_tex("T_WaterLily_Pad_N", height_to_normal(height_pad, strength=3.0))

    print("\n✅ Successfully generated all 7 PBR Texture Sets (14 textures total)!")

if __name__ == "__main__":
    generate_textures()
