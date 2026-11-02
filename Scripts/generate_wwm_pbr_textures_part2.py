#!/usr/bin/env python3
"""
Where Winds Meet Aesthetic PBR Texture Generator - Part 2
Generates high-fidelity 1024x1024 PBR textures for:
1. T_Curzon_Sandstone_D & N (weathered sandstone for steps, arch bases, plinths)
2. T_Curzon_WhiteTrim_D & N (aged historic lime plaster & jali screens)
3. T_Curzon_WoodDark_D & N (colonial dark teak / mahogany timber doors & louvers)
4. T_Curzon_RoofTiles_D & N (interlocking terracotta barrel tiles)
5. T_Modern_Concrete_D & N (architectural formwork concrete for modernist halls)
6. T_ArchivePedestal_D & N (ornate carved heritage lectern with ancient manuscript)
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

    # Helper: Normal map from height
    def height_to_normal(height, strength=4.0):
        # Sobel gradients
        gx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * strength
        gy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * strength
        gz = np.ones_like(height)
        norm = np.sqrt(gx**2 + gy**2 + gz**2)
        nx = 0.5 - 0.5 * (gx / norm)
        ny = 0.5 - 0.5 * (gy / norm)
        nz = 0.5 + 0.5 * (gz / norm)
        return np.stack([nx, ny, nz, np.ones_like(height)], axis=-1)

    print("=" * 60)
    print(f"Generating WWM Architectural PBR Textures ({res}x{res})...")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. CURZON SANDSTONE (Steps, plinths, cornices)
    # Warm buff / ochre sedimentary stone with chisel tooling marks
    # -------------------------------------------------------------
    print("Generating Sandstone...")
    np.random.seed(101)
    grain = np.random.normal(0, 0.04, (res, res))
    strata = np.sin(gy * 80.0 + np.sin(gx * 15.0) * 0.5) * 0.03
    chisel = np.sin(gx * 200.0) * np.cos(gy * 200.0) * 0.02
    stone_h = grain * 0.3 + strata + chisel

    # Sandstone color: warm buff / golden ochre (0.78, 0.68, 0.54)
    s_r = 0.78 + stone_h * 0.5
    s_g = 0.68 + stone_h * 0.4
    s_b = 0.52 + stone_h * 0.3
    save_tex("T_Curzon_Sandstone_D", np.stack([s_r, s_g, s_b, np.ones_like(s_r)], axis=-1))
    save_tex("T_Curzon_Sandstone_N", height_to_normal(stone_h, strength=5.0))

    # -------------------------------------------------------------
    # 2. CURZON WHITE TRIM / LIME PLASTER (Jali, balustrades, capitals)
    # Off-white aged limestone stucco with subtle porous mineral texture
    # -------------------------------------------------------------
    print("Generating White Trim / Stucco...")
    np.random.seed(202)
    plaster_noise = np.random.normal(0, 0.025, (res, res))
    plaster_pitted = np.clip(np.random.normal(0, 0.06, (res, res)), -0.05, 0.05)
    stucco_h = plaster_noise + plaster_pitted * 0.5

    # Off-white warm historic lime plaster (0.90, 0.88, 0.84)
    w_r = 0.89 + stucco_h * 0.4
    w_g = 0.87 + stucco_h * 0.4
    w_b = 0.83 + stucco_h * 0.4
    save_tex("T_Curzon_WhiteTrim_D", np.stack([w_r, w_g, w_b, np.ones_like(w_r)], axis=-1))
    save_tex("T_Curzon_WhiteTrim_N", height_to_normal(stucco_h, strength=4.0))

    # -------------------------------------------------------------
    # 3. CURZON DARK TIMBER (Colonial teak / mahogany doors & shutters)
    # Rich deep auburn wood grain with directional fibers
    # -------------------------------------------------------------
    print("Generating Dark Wood...")
    np.random.seed(303)
    fibers = np.sin(gy * 400.0 + np.sin(gx * 30.0) * 2.0) * 0.04
    knots = np.sin(np.sqrt((gx - 0.4)**2 * 4.0 + (gy - 0.5)**2) * 60.0) * 0.05
    wood_h = fibers + knots + np.random.normal(0, 0.02, (res, res))

    # Deep varnished mahogany: (0.28, 0.14, 0.08)
    wd_r = 0.28 + wood_h * 0.4
    wd_g = 0.14 + wood_h * 0.25
    wd_b = 0.08 + wood_h * 0.15
    save_tex("T_Curzon_WoodDark_D", np.stack([wd_r, wd_g, wd_b, np.ones_like(wd_r)], axis=-1))
    save_tex("T_Curzon_WoodDark_N", height_to_normal(wood_h, strength=6.0))

    # -------------------------------------------------------------
    # 4. CURZON ROOF TILES (Terracotta curved barrel tiles)
    # Interlocking fluted clay shingles with weathered terracotta patina
    # -------------------------------------------------------------
    print("Generating Terracotta Roof Tiles...")
    tile_w = res // 16
    tile_h = res // 8
    ix = (gx * res).astype(int)
    iy = (gy * res).astype(int)
    row = iy // tile_h
    col = (ix + (row % 2) * (tile_w // 2)) // tile_w
    local_x = (ix + (row % 2) * (tile_w // 2)) % tile_w
    local_y = iy % tile_h

    # Barrel tile curve across x, lip overlap across y
    curve = np.sin(local_x / tile_w * np.pi) * 0.4
    overlap = np.where(local_y < 12, 0.2, 0.0)
    tile_h_map = curve + overlap + np.random.normal(0, 0.03, (res, res))

    # Burnt orange terracotta: (0.62, 0.24, 0.12)
    rt_r = 0.60 + tile_h_map * 0.3
    rt_g = 0.23 + tile_h_map * 0.15
    rt_b = 0.11 + tile_h_map * 0.08
    save_tex("T_Curzon_RoofTiles_D", np.stack([rt_r, rt_g, rt_b, np.ones_like(rt_r)], axis=-1))
    save_tex("T_Curzon_RoofTiles_N", height_to_normal(tile_h_map, strength=8.0))

    # -------------------------------------------------------------
    # 5. MODERNIST CONCRETE (Board-formed brutalist concrete)
    # -------------------------------------------------------------
    print("Generating Modernist Concrete...")
    np.random.seed(505)
    board_lines = np.sin(gy * 40.0) * 0.03
    rough_grain = np.random.normal(0, 0.04, (res, res))
    conc_h = board_lines + rough_grain

    # Neutral warm grey concrete (0.55, 0.54, 0.52)
    c_r = 0.55 + conc_h * 0.3
    c_g = 0.54 + conc_h * 0.3
    c_b = 0.52 + conc_h * 0.3
    save_tex("T_Modern_Concrete_D", np.stack([c_r, c_g, c_b, np.ones_like(c_r)], axis=-1))
    save_tex("T_Modern_Concrete_N", height_to_normal(conc_h, strength=5.0))

    # -------------------------------------------------------------
    # 6. ARCHIVE PEDESTAL & CHRONICLE (Sacred DU Archive)
    # Carved sandstone with brass inlay and parchment pages
    # -------------------------------------------------------------
    print("Generating Archive Chronicle Pedestal PBR...")
    # Center circle for seal / crest
    cx = gx - 0.5
    cy = gy - 0.5
    rad = np.sqrt(cx**2 + cy**2)
    seal_ring = np.exp(-((rad - 0.3)**2) / 0.002) * 0.3
    seal_inner = np.where(rad < 0.28, 0.2, 0.0)
    arch_h = stone_h + seal_ring + seal_inner

    # Parchment gold & carved marble base
    a_r = 0.75 + arch_h * 0.3 + seal_ring * 0.2
    a_g = 0.65 + arch_h * 0.2 + seal_ring * 0.15
    a_b = 0.45 + arch_h * 0.1
    save_tex("T_ArchivePedestal_D", np.stack([a_r, a_g, a_b, np.ones_like(a_r)], axis=-1))
    save_tex("T_ArchivePedestal_N", height_to_normal(arch_h, strength=6.0))

    print("\n✅ All WWM PBR Part 2 textures generated successfully!")

if __name__ == "__main__":
    generate_textures()
