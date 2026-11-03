#!/usr/bin/env python3
"""
SparkVision — Authentic Architectural Facade Texture Generator
Creates ultra-high-detail 2048x2048 PBR Diffuse and Normal maps for:
1. Curzon Hall Indo-Saracenic Facade (Arched dark teak double doors, cusped windows, jali tracery, terracotta brick)
2. Kala Bhaban Tropical Modernist Facade (Sand concrete, horizontal ribbon windows, louvers, glass portals)
3. TSC Doxiadis Modernist Facade (White waffle louvers, terracotta panels, deep-set bronze glass entrance)
4. Modern Skyline Tower Facade (Reflective blue curtain walls, spandrels, double-height revolving glass doors)
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_WWM"
os.makedirs(OUTPUT_DIR, exist_ok=True)
RES = 2048

def save_normal_from_height(height_map, out_path, strength=3.0):
    """Calculates tangent normal map from height map using Sobel gradients."""
    h = height_map.astype(np.float32) / 255.0
    gx = np.zeros_like(h)
    gy = np.zeros_like(h)
    
    gx[:, 1:-1] = (h[:, 2:] - h[:, :-2]) * 0.5 * strength
    gy[1:-1, :] = (h[2:, :] - h[:-2, :]) * 0.5 * strength
    
    gz = np.ones_like(h)
    norm = np.sqrt(gx**2 + gy**2 + gz**2)
    norm[norm == 0] = 1.0
    
    nx = ((-gx / norm) * 0.5 + 0.5) * 255.0
    ny = ((-gy / norm) * 0.5 + 0.5) * 255.0
    nz = ((gz / norm) * 0.5 + 0.5) * 255.0
    
    normal_img = np.stack([nx, ny, nz], axis=-1).astype(np.uint8)
    Image.fromarray(normal_img, "RGB").save(out_path, "PNG")
    print(f"  ✓ Saved normal map: {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)")

# ==============================================================================
# 1. CURZON HALL INDO-SARACENIC ARCHED FACADE (DOORS & WINDOWS)
# ==============================================================================
def generate_curzon_facade():
    print("\n[1/4] Generating Curzon Hall Indo-Saracenic Facade Texture (2048x2048)...")
    im = Image.new("RGB", (RES, RES), "#8C281A") # Rich Terracotta red brick base
    draw = ImageDraw.Draw(im)
    height = Image.new("L", (RES, RES), 128)
    hdraw = ImageDraw.Draw(height)

    # Base brick texture
    brick_w, brick_h = 64, 24
    mortar_col = (195, 185, 170)
    for y in range(0, RES, brick_h):
        draw.line([(0, y), (RES, y)], fill=mortar_col, width=2)
        hdraw.line([(0, y), (RES, y)], fill=60, width=2)
        offset = (brick_w // 2) if (y // brick_h) % 2 else 0
        for x in range(offset, RES, brick_w):
            draw.line([(x, y), (x, y + brick_h)], fill=mortar_col, width=2)
            hdraw.line([(x, y), (x, y + brick_h)], fill=60, width=2)

    # Plinth at base (Sandstone)
    plinth_h = 160
    draw.rectangle([0, RES - plinth_h, RES, RES], fill="#C5B095")
    hdraw.rectangle([0, RES - plinth_h, RES, RES], fill=180)
    draw.line([0, RES - plinth_h, RES, RES - plinth_h], fill="#F0EBE1", width=8)
    hdraw.line([0, RES - plinth_h, RES, RES - plinth_h], fill=240, width=8)

    # Upper Eaves (Chhajja) & Decorative Brackets at top
    eaves_h = 140
    draw.rectangle([0, 0, RES, eaves_h], fill="#D8C8B0")
    hdraw.rectangle([0, 0, RES, eaves_h], fill=210)
    for bx in range(60, RES, 120):
        # Mughal decorative brackets
        draw.polygon([(bx - 20, 0), (bx + 20, 0), (bx + 10, eaves_h), (bx - 10, eaves_h)], fill="#FAF6EE")
        hdraw.polygon([(bx - 20, 0), (bx + 20, 0), (bx + 10, eaves_h), (bx - 10, eaves_h)], fill=255)

    # 4 Symmetrical Architectural Bays
    bay_width = RES // 4
    for i in range(4):
        cx = i * bay_width + bay_width // 2

        # White stone arch frame (Outer Islamic pointed arch)
        arch_w = 340
        arch_top = eaves_h + 120
        arch_bottom = RES - plinth_h
        left = cx - arch_w // 2
        right = cx + arch_w // 2

        # Outer carved arch border (Ivory stone)
        draw.rectangle([left - 24, arch_top + 160, right + 24, arch_bottom], fill="#EDE7DC")
        draw.chord([left - 24, arch_top, right + 24, arch_top + 340], 180, 360, fill="#EDE7DC")
        hdraw.rectangle([left - 24, arch_top + 160, right + 24, arch_bottom], fill=220)
        hdraw.chord([left - 24, arch_top, right + 24, arch_top + 340], 180, 360, fill=220)

        # Deep recess cavity
        draw.rectangle([left, arch_top + 180, right, arch_bottom], fill="#1C1816")
        draw.chord([left, arch_top + 20, right, arch_top + 340], 180, 360, fill="#1C1816")
        hdraw.rectangle([left, arch_top + 180, right, arch_bottom], fill=40)
        hdraw.chord([left, arch_top + 20, right, arch_top + 340], 180, 360, fill=40)

        if i in [1, 2]:
            # GROUND FLOOR: GRAND COLONIAL TEAK ARCHED DOUBLE DOORS
            door_top = arch_top + 450
            door_left = left + 20
            door_right = right - 20
            
            # Dark polished teak door wood
            draw.rectangle([door_left, door_top, door_right, arch_bottom], fill="#2E180E")
            hdraw.rectangle([door_left, door_top, door_right, arch_bottom], fill=110)
            
            # Center door split seam
            mid_x = (door_left + door_right) // 2
            draw.line([(mid_x, door_top), (mid_x, arch_bottom)], fill="#0D0704", width=6)
            hdraw.line([(mid_x, door_top), (mid_x, arch_bottom)], fill=20, width=6)

            # Raised wooden door panels (4 panels per leaf)
            for leaf_idx, (lx1, lx2) in enumerate([(door_left + 15, mid_x - 15), (mid_x + 15, door_right - 15)]):
                p_h = (arch_bottom - door_top - 120) // 4
                for p_idx in range(4):
                    py1 = door_top + 30 + p_idx * (p_h + 20)
                    py2 = py1 + p_h
                    draw.rectangle([lx1, py1, lx2, py2], fill="#4A2818", outline="#1A0D07", width=4)
                    hdraw.rectangle([lx1, py1, lx2, py2], fill=140, outline=60, width=4)
                    # Brass rivets / ornamental studs
                    draw.ellipse([lx1 + 10, py1 + 10, lx1 + 20, py1 + 20], fill="#D4AF37")
                    draw.ellipse([lx2 - 20, py1 + 10, lx2 - 10, py1 + 20], fill="#D4AF37")

            # Brass Ring Door Knocker Handles
            draw.ellipse([mid_x - 45, door_top + 320, mid_x - 15, door_top + 350], fill="#D4AF37", outline="#8C6E14", width=3)
            draw.ellipse([mid_x + 15, door_top + 320, mid_x + 45, door_top + 350], fill="#D4AF37", outline="#8C6E14", width=3)

            # Upper Fanlight Transom Window with Jali Tracery above door
            draw.chord([door_left, arch_top + 60, door_right, door_top], 180, 360, fill="#122428", outline="#EDE7DC", width=8)
            hdraw.chord([door_left, arch_top + 60, door_right, door_top], 180, 360, fill=80, outline=220, width=8)
            # Jali geometric lines
            for spoke_angle in np.linspace(200, 340, 7):
                rad = np.radians(spoke_angle)
                ex = cx + int(np.cos(rad) * 120)
                ey = (arch_top + 200) + int(np.sin(rad) * 120)
                draw.line([(cx, arch_top + 200), (ex, ey)], fill="#FAF6EE", width=4)
        else:
            # UPPER / FLANKING BAYS: MULTI-PANE COLONIAL SASH WINDOWS WITH CUSPED ARCH
            win_top = arch_top + 180
            win_left = left + 25
            win_right = right - 25
            win_bottom = arch_bottom - 80

            # Window frame & dark reflective colonial glass
            draw.rectangle([win_left, win_top, win_right, win_bottom], fill="#0A1820", outline="#EDE7DC", width=10)
            hdraw.rectangle([win_left, win_top, win_right, win_bottom], fill=50, outline=220, width=10)
            draw.chord([win_left, arch_top + 50, win_right, win_top + 100], 180, 360, fill="#0A1820", outline="#EDE7DC", width=10)
            hdraw.chord([win_left, arch_top + 50, win_right, win_top + 100], 180, 360, fill=50, outline=220, width=10)

            # Multi-pane wooden window mullions
            for gx in np.linspace(win_left, win_right, 4)[1:-1]:
                draw.line([(gx, win_top - 30), (gx, win_bottom)], fill="#FAF6EE", width=5)
                hdraw.line([(gx, win_top - 30), (gx, win_bottom)], fill=180, width=5)
            for gy in np.linspace(win_top, win_bottom, 7)[1:-1]:
                draw.line([(win_left, gy), (win_right, gy)], fill="#FAF6EE", width=5)
                hdraw.line([(win_left, gy), (win_right, gy)], fill=180, width=5)

            # Window glass blue reflection highlight
            for gy in np.linspace(win_top + 40, win_bottom - 40, 5):
                draw.line([(win_left + 15, gy), (win_right - 15, gy + 30)], fill="#25485E", width=3)

    diff_path = os.path.join(OUTPUT_DIR, "T_Curzon_Facade_ArchedDoorsWindows_D.png")
    norm_path = os.path.join(OUTPUT_DIR, "T_Curzon_Facade_ArchedDoorsWindows_N.png")
    im.save(diff_path, "PNG")
    print(f"  ✓ Saved diffuse map: {diff_path} ({os.path.getsize(diff_path)/1024:.1f} KB)")
    save_normal_from_height(np.array(height), norm_path)

# ==============================================================================
# 2. KALA BHABAN (FACULTY OF ARTS) TROPICAL MODERNIST FACADE
# ==============================================================================
def generate_kala_bhaban_facade():
    print("\n[2/4] Generating Kala Bhaban Tropical Modernist Facade Texture (2048x2048)...")
    # Warm sand-toned architectural concrete
    im = Image.new("RGB", (RES, RES), "#C2B49E")
    draw = ImageDraw.Draw(im)
    height = Image.new("L", (RES, RES), 140)
    hdraw = ImageDraw.Draw(height)

    # Shuttered concrete horizontal tie seams
    floor_count = 4
    floor_h = RES // floor_count
    for f in range(floor_count):
        y_top = f * floor_h
        y_bot = y_top + floor_h
        
        # Heavy horizontal concrete eyebrow sunshade (Brise-soleil louver)
        draw.rectangle([0, y_top, RES, y_top + 45], fill="#E2D8C6")
        hdraw.rectangle([0, y_top, RES, y_top + 45], fill=240)
        draw.line([0, y_top + 45, RES, y_top + 45], fill="#7A6E5C", width=6)
        hdraw.line([0, y_top + 45, RES, y_top + 45], fill=50, width=6)

        if f == 3:
            # GROUND FLOOR: INSTITUTIONAL ENTRANCE PORTAL & GLASS DOORS
            # Deep recessed porch
            draw.rectangle([0, y_top + 50, RES, y_bot], fill="#A89A84")
            hdraw.rectangle([0, y_top + 50, RES, y_bot], fill=110)

            # Central Grand Entrance Glass Doors (3 double sets)
            door_bay_w = RES // 4
            for d_idx in range(1, 4):
                dx = d_idx * door_bay_w
                dl, dr = dx - 180, dx + 180
                dt, db = y_top + 110, y_bot - 20

                # Dark bronze aluminum frame
                draw.rectangle([dl, dt, dr, db], fill="#0A141A", outline="#2B2824", width=12)
                hdraw.rectangle([dl, dt, dr, db], fill=30, outline=200, width=12)

                # Double glass doors center split
                cx = (dl + dr) // 2
                draw.line([(cx, dt), (cx, db)], fill="#3A342E", width=8)
                hdraw.line([(cx, dt), (cx, db)], fill=180, width=8)

                # Vertical Stainless Steel Door Push Handles
                draw.rectangle([cx - 24, dt + 180, cx - 12, dt + 280], fill="#E8EFF5", outline="#738290", width=2)
                draw.rectangle([cx + 12, dt + 180, cx + 24, dt + 280], fill="#E8EFF5", outline="#738290", width=2)
                hdraw.rectangle([cx - 24, dt + 180, cx - 12, dt + 280], fill=255)
                hdraw.rectangle([cx + 12, dt + 180, cx + 24, dt + 280], fill=255)

                # Transom signage band above doors ("ARTS FACULTY • কলা ভবন")
                draw.rectangle([dl, dt - 50, dr, dt], fill="#1C242B", outline="#4A453F", width=4)
                hdraw.rectangle([dl, dt - 50, dr, dt], fill=160)
        else:
            # UPPER FLOORS: HORIZONTAL TROPICAL CONTINUOUS RIBBON WINDOWS
            win_t = y_top + 70
            win_b = y_bot - 60

            # Window continuous dark aperture band
            draw.rectangle([0, win_t, RES, win_b], fill="#091822")
            hdraw.rectangle([0, win_t, RES, win_b], fill=40)

            # Rhythmic vertical concrete fins & dark window mullions
            mullion_step = RES // 16
            for m in range(16):
                mx = m * mullion_step
                # Concrete shading fin (every 4 mullions)
                if m % 4 == 0:
                    draw.rectangle([mx - 15, y_top, mx + 15, y_bot], fill="#D8CCA8", outline="#827660", width=3)
                    hdraw.rectangle([mx - 15, y_top, mx + 15, y_bot], fill=230)
                else:
                    draw.line([(mx, win_t), (mx, win_b)], fill="#1E2830", width=6)
                    hdraw.line([(mx, win_t), (mx, win_b)], fill=150, width=6)

            # Horizontal sash divider
            mid_y = (win_t + win_b) // 2
            draw.line([(0, mid_y), (RES, mid_y)], fill="#1E2830", width=6)
            hdraw.line([(0, mid_y), (RES, mid_y)], fill=150, width=6)

            # Solar glass green-blue tint sheen
            for g_bay in range(16):
                gx = g_bay * mullion_step
                draw.polygon([(gx + 10, win_t + 15), (gx + 60, win_t + 15), (gx + 30, win_b - 15), (gx + 10, win_b - 15)], fill="#143644")

    diff_path = os.path.join(OUTPUT_DIR, "T_KalaBhaban_Facade_ModernistWindows_D.png")
    norm_path = os.path.join(OUTPUT_DIR, "T_KalaBhaban_Facade_ModernistWindows_N.png")
    im.save(diff_path, "PNG")
    print(f"  ✓ Saved diffuse map: {diff_path} ({os.path.getsize(diff_path)/1024:.1f} KB)")
    save_normal_from_height(np.array(height), norm_path)

# ==============================================================================
# 3. TSC (TEACHER-STUDENT CENTRE) DOXIADIS MODERNIST FACADE
# ==============================================================================
def generate_tsc_facade():
    print("\n[3/4] Generating TSC Doxiadis Modernist Facade Texture (2048x2048)...")
    # Crisp off-white modernist plaster and concrete
    im = Image.new("RGB", (RES, RES), "#ECEAE2")
    draw = ImageDraw.Draw(im)
    height = Image.new("L", (RES, RES), 150)
    hdraw = ImageDraw.Draw(height)

    # Upper Roof: Iconic Doxiadis Waffle Slab Louvers
    waffle_h = 320
    draw.rectangle([0, 0, RES, waffle_h], fill="#F4F3EE")
    hdraw.rectangle([0, 0, RES, waffle_h], fill=210)
    grid_sz = 80
    for y in range(0, waffle_h, grid_sz):
        draw.line([(0, y), (RES, y)], fill="#CCC8BE", width=8)
        hdraw.line([(0, y), (RES, y)], fill=80, width=8)
    for x in range(0, RES, grid_sz):
        draw.line([(x, 0), (x, waffle_h)], fill="#CCC8BE", width=8)
        hdraw.line([(x, 0), (x, waffle_h)], fill=80, width=8)

    # Mid Section: Modern Terracotta Accent Panel Bays
    mid_top = waffle_h + 30
    mid_bottom = RES - 550
    draw.rectangle([0, mid_top, RES, mid_bottom], fill="#A84C34") # Rich architectural terracotta
    hdraw.rectangle([0, mid_top, RES, mid_bottom], fill=160)

    # Terracotta panel horizontal joints
    for y in range(mid_top, mid_bottom, 60):
        draw.line([(0, y), (RES, y)], fill="#5C2518", width=4)
        hdraw.line([(0, y), (RES, y)], fill=90, width=4)
    # Vertical rhythmic clerestory slot windows
    for x in range(120, RES, 240):
        draw.rectangle([x - 25, mid_top + 40, x + 25, mid_bottom - 40], fill="#0A1F1B", outline="#E2DDD2", width=6)
        hdraw.rectangle([x - 25, mid_top + 40, x + 25, mid_bottom - 40], fill=40, outline=220, width=6)

    # Ground Level: Expansive Glazed Public Lobby & Double Bronze Glass Doors
    lobby_top = mid_bottom + 20
    draw.rectangle([0, lobby_top, RES, RES], fill="#0D2420") # Tinted solar green lobby glass
    hdraw.rectangle([0, lobby_top, RES, RES], fill=50)

    # Structural white columns every 512px
    for c in range(0, RES + 1, 512):
        draw.rectangle([c - 30, lobby_top, c + 30, RES], fill="#FAF8F5", outline="#C2BEB4", width=4)
        hdraw.rectangle([c - 30, lobby_top, c + 30, RES], fill=240, outline=120, width=4)

    # Main Entrance Sets (Bronze architectural frames)
    for cx in [512, 1536]:
        dl, dr = cx - 210, cx + 210
        dt, db = lobby_top + 60, RES - 20
        draw.rectangle([dl, dt, dr, db], fill="#081815", outline="#735A38", width=14)
        hdraw.rectangle([dl, dt, dr, db], fill=30, outline=210, width=14)

        # Center door split
        draw.line([(cx, dt), (cx, db)], fill="#8C6E45", width=10)
        hdraw.line([(cx, dt), (cx, db)], fill=200, width=10)

        # Polished brass push bars
        draw.rectangle([cx - 40, dt + 200, cx - 15, dt + 270], fill="#D4AF37", outline="#8C6E14", width=3)
        draw.rectangle([cx + 15, dt + 200, cx + 40, dt + 270], fill="#D4AF37", outline="#8C6E14", width=3)
        hdraw.rectangle([cx - 40, dt + 200, cx - 15, dt + 270], fill=255)
        hdraw.rectangle([cx + 15, dt + 200, cx + 40, dt + 270], fill=255)

    diff_path = os.path.join(OUTPUT_DIR, "T_TSC_Facade_DoxiadisWaffle_D.png")
    norm_path = os.path.join(OUTPUT_DIR, "T_TSC_Facade_DoxiadisWaffle_N.png")
    im.save(diff_path, "PNG")
    print(f"  ✓ Saved diffuse map: {diff_path} ({os.path.getsize(diff_path)/1024:.1f} KB)")
    save_normal_from_height(np.array(height), norm_path)

# ==============================================================================
# 4. MODERN SKYLINE TOWER CURTAIN WALL & REVOLVING GLASS PORTAL
# ==============================================================================
def generate_skyline_facade():
    print("\n[4/4] Generating Modern Skyline Curtain Wall Facade Texture (2048x2048)...")
    # Deep reflective sky blue curtain wall glazing
    im = Image.new("RGB", (RES, RES), "#10283C")
    draw = ImageDraw.Draw(im)
    height = Image.new("L", (RES, RES), 60)
    hdraw = ImageDraw.Draw(height)

    # Modern curtain wall grid (dark titanium aluminum mullions)
    pan_w, pan_h = 128, 96
    for y in range(0, RES - 400, pan_h):
        # Spandrel dark glass band every 3 floors
        is_spandrel = ((y // pan_h) % 3 == 0)
        band_col = "#06121C" if is_spandrel else "#15334D"
        draw.rectangle([0, y, RES, y + pan_h], fill=band_col)
        draw.line([0, y, RES, y], fill="#3A4854", width=6)
        hdraw.line([0, y, RES, y], fill=190, width=6)
        
        for x in range(0, RES, pan_w):
            draw.line([x, y, x, y + pan_h], fill="#3A4854", width=6)
            hdraw.line([x, y, x, y + pan_h], fill=190, width=6)
            # Subtle sky cloud reflection highlight across glass panes
            if not is_spandrel and ((x + y) // pan_w) % 5 == 0:
                draw.rectangle([x + 6, y + 6, x + pan_w - 6, y + pan_h - 6], fill="#1C466A")

    # Ground Level Grand Double-Height Corporate Lobby
    lobby_t = RES - 400
    draw.rectangle([0, lobby_t, RES, RES], fill="#08141F")
    draw.line([0, lobby_t, RES, lobby_t], fill="#8A96A0", width=12) # Titanium beam
    hdraw.rectangle([0, lobby_t, RES, RES], fill=40)
    hdraw.line([0, lobby_t, RES, lobby_t], fill=240, width=12)

    # Grand Commercial Revolving / Double Doors (2 units)
    for cx in [600, 1448]:
        dl, dr = cx - 180, cx + 180
        dt, db = lobby_t + 80, RES - 10
        draw.rectangle([dl, dt, dr, db], fill="#040A10", outline="#B4C0C8", width=10)
        hdraw.rectangle([dl, dt, dr, db], fill=20, outline=230, width=10)

        # Revolving Door circular enclosure feel
        draw.ellipse([cx - 140, dt + 20, cx + 140, db - 20], fill="#091620", outline="#738290", width=6)
        draw.line([(cx, dt + 20), (cx, db - 20)], fill="#B4C0C8", width=6)
        draw.line([(cx - 140, (dt + db) // 2), (cx + 140, (dt + db) // 2)], fill="#B4C0C8", width=6)
        hdraw.ellipse([cx - 140, dt + 20, cx + 140, db - 20], fill=60, outline=180, width=6)

    diff_path = os.path.join(OUTPUT_DIR, "T_ModernSkyline_Facade_CurtainWall_D.png")
    norm_path = os.path.join(OUTPUT_DIR, "T_ModernSkyline_Facade_CurtainWall_N.png")
    im.save(diff_path, "PNG")
    print(f"  ✓ Saved diffuse map: {diff_path} ({os.path.getsize(diff_path)/1024:.1f} KB)")
    save_normal_from_height(np.array(height), norm_path)

def main():
    print("=" * 80)
    print("SPARKVISION: GENERATING REALISTIC ARCHITECTURAL DOORS & WINDOWS TEXTURES")
    print("=" * 80)
    generate_curzon_facade()
    generate_kala_bhaban_facade()
    generate_tsc_facade()
    generate_skyline_facade()
    print("\n✅ All 4 architectural facade texture suites generated successfully!")

if __name__ == "__main__":
    main()
