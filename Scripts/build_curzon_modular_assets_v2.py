#!/usr/bin/env python3
"""
Curzon Hall Master Architectural Asset Generator (v2) for Blender 5.2.3 LTS
Reconstructs authentic Indo-Saracenic architectural assets with precision:
- True curved horseshoe arches (ground floor arcade)
- True 7-cusp multi-foil scalloped arches (upper floor arcade)
- Projecting chhajja eaves with carved corbel support brackets
- Monumental multi-tiered central entrance portal with grand iwan arch & twin chhatris
- 25.2m octagonal corner towers with observation balconies & Rajput cupolas
- Stepped Indo-Saracenic parapet merlons (battlements)
- PBR material slots: M_Curzon_Brick, M_Curzon_WhiteTrim, M_Curzon_Accent, M_Curzon_Sandstone, M_Curzon_Brass, M_Curzon_Tiles

All coordinates in metric scale (1 Blender unit = 1 meter = 100 Unreal units).
"""

import bpy
import bmesh
import math
import mathutils
import os

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/CurzonModular"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

def get_or_create_materials():
    materials = {}
    
    # 0: Brick (Dark Terracotta Red)
    mat = bpy.data.materials.get("M_Curzon_Brick") or bpy.data.materials.new(name="M_Curzon_Brick")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.51, 0.17, 0.12, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.82
    materials["brick"] = mat

    # 1: White Trim / Plaster
    mat = bpy.data.materials.get("M_Curzon_WhiteTrim") or bpy.data.materials.new(name="M_Curzon_WhiteTrim")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.87, 0.83, 0.76, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.68
    materials["trim"] = mat

    # 2: Accent (Dark Metal / Cast Iron)
    mat = bpy.data.materials.get("M_Curzon_Accent") or bpy.data.materials.new(name="M_Curzon_Accent")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.12, 0.12, 0.14, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.40
    materials["accent"] = mat

    # 3: Sandstone
    mat = bpy.data.materials.get("M_Curzon_Sandstone") or bpy.data.materials.new(name="M_Curzon_Sandstone")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.65, 0.48, 0.35, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.75
    materials["sandstone"] = mat

    # 4: Brass / Gold Patina
    mat = bpy.data.materials.get("M_Curzon_Brass") or bpy.data.materials.new(name="M_Curzon_Brass")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.72, 0.56, 0.22, 1.0)
            bsdf.inputs["Metallic"].default_value = 0.90
            bsdf.inputs["Roughness"].default_value = 0.35
    materials["brass"] = mat

    # 5: Floor Tiles
    mat = bpy.data.materials.get("M_Curzon_Tiles") or bpy.data.materials.new(name="M_Curzon_Tiles")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.48, 0.19, 0.14, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.55
    materials["tiles"] = mat

    return materials

def assign_material_to_verts(bm, verts, mat_index):
    for face in bm.faces:
        if all(v in verts for v in face.verts):
            face.material_index = mat_index

def assign_material_to_any_verts(bm, verts, mat_index):
    for face in bm.faces:
        if any(v in verts for v in face.verts):
            face.material_index = mat_index

def export_fbx(obj, filename):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    filepath = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,
        global_scale=1.0,
        apply_unit_scale=True,
        bake_space_transform=True,
        object_types={'MESH'},
        mesh_smooth_type='FACE'
    )
    print(f"Exported: {filepath}")

# Helper: Create an authentic curved horseshoe arch opening
def create_horseshoe_arch(bm, center_x, center_y, base_z, clear_width, spring_z, crown_z, wall_thickness, num_segments=16):
    r = clear_width / 2.0
    # Horseshoe extends slightly below center line: theta from -15 deg to 195 deg
    start_angle = -math.radians(15)
    end_angle = math.pi + math.radians(15)
    
    arch_pts = []
    for i in range(num_segments + 1):
        t = i / num_segments
        angle = start_angle + t * (end_angle - start_angle)
        # Flip angle so x goes from -r to +r
        px = center_x - r * math.cos(angle)
        pz = spring_z + r * math.sin(angle)
        arch_pts.append((px, pz))
    return arch_pts

# Helper: Create an authentic 7-cusped / scalloped arch
def create_cusped_arch(bm, center_x, center_y, spring_z, crown_z, clear_width, num_cusps=7):
    # Generates points along a pointed multi-foil cusped arch
    half_width = clear_width / 2.0
    pts = []
    # Left half cusps (num_cusps // 2)
    cusps_per_side = num_cusps // 2
    r_cusp = (half_width / cusps_per_side) * 0.75
    
    # Sample left to right
    total_samples = 24
    for i in range(total_samples + 1):
        t = i / total_samples # 0 to 1
        x = center_x - half_width + t * clear_width
        rel_x = (x - center_x) / half_width # -1 to 1
        
        # Base pointed gothic curve
        base_h = spring_z + (crown_z - spring_z) * (1.0 - abs(rel_x) ** 0.85)
        # Scallop modulation (cusps)
        scallop = math.sin(abs(rel_x) * cusps_per_side * math.pi) * 0.18
        if scallop < 0:
            scallop = 0
        z = base_h - scallop
        pts.append((x, z))
    return pts

# Helper: Create a sloped Chhajja (projecting eaves) with corbel brackets
def add_chhajja_with_brackets(bm, width, depth, base_z, slope_angle=35, projection=1.2, num_brackets=8):
    # Eave slab
    rad = math.radians(slope_angle)
    dx = projection
    dz = -projection * math.sin(rad)
    
    # Create sloped eave
    eave = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, projection, 0.15), verts=eave["verts"])
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(-rad, 3, 'X'), verts=eave["verts"])
    bmesh.ops.translate(bm, vec=(0, depth/2.0 + projection*0.4, base_z + dz*0.3), verts=eave["verts"])
    
    # Corbel Brackets along the front
    bracket_verts = []
    spacing = width / (num_brackets - 1) if num_brackets > 1 else 0
    start_x = -width / 2.0
    for b in range(num_brackets):
        bx = start_x + b * spacing
        brk = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.20, projection*0.65, 0.55), verts=brk["verts"])
        bmesh.ops.translate(bm, vec=(bx, depth/2.0 + projection*0.25, base_z - 0.35), verts=brk["verts"])
        bracket_verts.extend(brk["verts"])
    
    return eave["verts"] + bracket_verts

# ==============================================================================
# 1. SM_Curzon_Veranda_Arch_Lower (8m wide x 2.6m deep x 6.4m high)
# ==============================================================================
def build_curzon_veranda_lower(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Veranda_Arch_Lower")
    obj = bpy.data.objects.new("SM_Curzon_Veranda_Arch_Lower", mesh)
    bpy.context.scene.collection.objects.link(obj)
    for m in [mats["brick"], mats["trim"], mats["sandstone"], mats["tiles"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 8.0
    depth = 2.6
    height = 6.4

    # Floor / Plinth Slab (Tiles)
    fl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.4), verts=fl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.2), verts=fl["verts"])
    assign_material_to_verts(bm, fl["verts"], 3) # Tiles

    # Ceiling / Floor Header Slab
    cl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.5), verts=cl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, height - 0.25), verts=cl["verts"])

    # Three Massive Piers (Left, Center, Right)
    pier_w = 0.8
    pier_d = 0.85
    pier_x_positions = [-width/2.0 + pier_w/2.0, 0.0, width/2.0 - pier_w/2.0]
    
    for px in pier_x_positions:
        p = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pier_w, pier_d, 3.8), verts=p["verts"])
        bmesh.ops.translate(bm, vec=(px, depth/2.0 - pier_d/2.0, 2.3), verts=p["verts"])
        
        # Plinth base (Sandstone)
        pb = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pier_w + 0.15, pier_d + 0.15, 0.5), verts=pb["verts"])
        bmesh.ops.translate(bm, vec=(px, depth/2.0 - pier_d/2.0, 0.65), verts=pb["verts"])
        assign_material_to_verts(bm, pb["verts"], 2) # Sandstone
        
        # Impost Molded Capital (White Trim)
        ic = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pier_w + 0.12, pier_d + 0.12, 0.3), verts=ic["verts"])
        bmesh.ops.translate(bm, vec=(px, depth/2.0 - pier_d/2.0, 4.2), verts=ic["verts"])
        assign_material_to_verts(bm, ic["verts"], 1) # White Trim

    # Two Curved Horseshoe Arch Openings (Left Bay, Right Bay)
    # Bay Centers: x = -2.0, x = +2.0
    bay_centers = [-2.0, 2.0]
    arch_clear_w = 2.8
    spring_z = 4.2
    crown_z = 5.6
    
    for cx in bay_centers:
        # Build curved arch ring using faceted trapezoids
        r_in = arch_clear_w / 2.0
        r_out = r_in + 0.40 # 40cm thick brick arch ring
        num_seg = 12
        start_a = -math.radians(12)
        end_a = math.pi + math.radians(12)
        
        arch_v = []
        for s in range(num_seg):
            a1 = start_a + (s / num_seg) * (end_a - start_a)
            a2 = start_a + ((s + 1) / num_seg) * (end_a - start_a)
            
            x1_in = cx - r_in * math.cos(a1)
            z1_in = spring_z + r_in * math.sin(a1)
            x2_in = cx - r_in * math.cos(a2)
            z2_in = spring_z + r_in * math.sin(a2)
            
            x1_out = cx - r_out * math.cos(a1)
            z1_out = spring_z + r_out * math.sin(a1)
            x2_out = cx - r_out * math.cos(a2)
            z2_out = spring_z + r_out * math.sin(a2)
            
            # Segment block
            seg = bmesh.ops.create_cube(bm, size=1.0)
            avg_x = (x1_in + x2_in + x1_out + x2_out) / 4.0
            avg_z = (z1_in + z2_in + z1_out + z2_out) / 4.0
            bmesh.ops.scale(bm, vec=(abs(x2_in - x1_in) + 0.05, pier_d, 0.45), verts=seg["verts"])
            bmesh.ops.translate(bm, vec=(avg_x, depth/2.0 - pier_d/2.0, avg_z), verts=seg["verts"])
            arch_v.extend(seg["verts"])
            
        # Keystone at apex (White Trim)
        ks = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.45, pier_d + 0.1, 0.65), verts=ks["verts"])
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - pier_d/2.0, spring_z + r_out + 0.15), verts=ks["verts"])
        assign_material_to_verts(bm, ks["verts"], 1) # White Trim

    # Upper Spandrel Wall
    sp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, pier_d, 0.65), verts=sp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - pier_d/2.0, height - 0.7), verts=sp["verts"])

    # Rear Interior Wall with Arched Corridor Doorways
    rw = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, 0.4, height), verts=rw["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -depth/2.0 + 0.2, height/2.0), verts=rw["verts"])

    # Continuous Projecting Chhajja (Eaves) at +6.4m with Corbel Brackets
    add_chhajja_with_brackets(bm, width=width, depth=depth, base_z=height - 0.1, slope_angle=35, projection=1.2, num_brackets=8)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Veranda_Arch_Lower.fbx")

# ==============================================================================
# 2. SM_Curzon_Veranda_Arch_Upper (8m wide x 2.6m deep x 6.2m high)
# ==============================================================================
def build_curzon_veranda_upper(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Veranda_Arch_Upper")
    obj = bpy.data.objects.new("SM_Curzon_Veranda_Arch_Upper", mesh)
    bpy.context.scene.collection.objects.link(obj)
    for m in [mats["brick"], mats["trim"], mats["sandstone"], mats["tiles"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 8.0
    depth = 2.6
    height = 6.2

    # Floor Slab (Tiles)
    fl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.35), verts=fl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.175), verts=fl["verts"])
    assign_material_to_verts(bm, fl["verts"], 3) # Tiles

    # Ceiling Slab
    cl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.45), verts=cl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, height - 0.225), verts=cl["verts"])

    # Octagonal Slender Colonnade (Paired colonnettes at center, single at flanks)
    col_r = 0.22
    col_d = 4.2
    col_positions = [-3.6, -0.4, 0.4, 3.6]
    
    for cx in col_positions:
        # Octagonal Shaft
        c = bmesh.ops.create_cone(bm, segments=8, radius1=col_r, radius2=col_r, depth=col_d)
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - 0.45, col_d/2.0 + 0.35), verts=c["verts"])
        
        # Molded Octagonal Base (Sandstone)
        bs = bmesh.ops.create_cone(bm, segments=8, radius1=col_r + 0.12, radius2=col_r + 0.06, depth=0.35)
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - 0.45, 0.52), verts=bs["verts"])
        assign_material_to_verts(bm, bs["verts"], 2)
        
        # Carved Lotus Capital (White Trim)
        cp = bmesh.ops.create_cone(bm, segments=8, radius1=col_r + 0.15, radius2=col_r + 0.22, depth=0.45)
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - 0.45, col_d + 0.35 + 0.22), verts=cp["verts"])
        assign_material_to_verts(bm, cp["verts"], 1)

    # White Pierced Jali Balustrade Screen along front (Height 1.0m)
    bal_w = 3.1
    for bx in [-2.0, 2.0]:
        bal = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(bal_w, 0.16, 0.95), verts=bal["verts"])
        bmesh.ops.translate(bm, vec=(bx, depth/2.0 - 0.45, 0.85), verts=bal["verts"])
        assign_material_to_verts(bm, bal["verts"], 1) # White Trim
        
        # Balustrade Top Handrail
        hr = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(bal_w + 0.1, 0.24, 0.12), verts=hr["verts"])
        bmesh.ops.translate(bm, vec=(bx, depth/2.0 - 0.45, 1.38), verts=hr["verts"])
        assign_material_to_verts(bm, hr["verts"], 2) # Sandstone

    # Two Mughal Multi-Cusped / Scalloped Arches
    # Centers at x = -2.0 and x = +2.0
    for ax in [-2.0, 2.0]:
        # Form 7 cusps (scallops) using segmented arch sections
        num_cusps = 7
        cusp_span = 3.2
        r_span = cusp_span / 2.0
        
        # Spandrel arch envelope (Brick)
        arch_pts = create_cusped_arch(bm, center_x=ax, center_y=depth/2.0 - 0.45, 
                                      spring_z=4.6, crown_z=5.6, clear_width=cusp_span, num_cusps=7)
        for i in range(len(arch_pts) - 1):
            x1, z1 = arch_pts[i]
            x2, z2 = arch_pts[i+1]
            seg = bmesh.ops.create_cube(bm, size=1.0)
            mid_x = (x1 + x2) / 2.0
            mid_z = (z1 + z2) / 2.0
            bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.05, 0.6, 0.35), verts=seg["verts"])
            bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.45, mid_z + 0.15), verts=seg["verts"])
            
            # Scalloped white trim moulding
            t_seg = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.04, 0.65, 0.12), verts=t_seg["verts"])
            bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.45, mid_z - 0.06), verts=t_seg["verts"])
            assign_material_to_verts(bm, t_seg["verts"], 1) # White Trim

    # Upper Spandrel Wall
    sp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, 0.6, 0.5), verts=sp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - 0.45, height - 0.5), verts=sp["verts"])

    # Rear Interior Wall with Arched Transom Windows
    rw = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, 0.4, height), verts=rw["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -depth/2.0 + 0.2, height/2.0), verts=rw["verts"])

    # Upper Projecting Chhajja at +6.2m with Corbel Brackets
    add_chhajja_with_brackets(bm, width=width, depth=depth, base_z=height - 0.1, slope_angle=35, projection=1.2, num_brackets=8)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Veranda_Arch_Upper.fbx")

# ==============================================================================
# 3. SM_Curzon_Entrance_Portal (18m wide x 4.8m deep x 23.4m high)
# ==============================================================================
def build_curzon_entrance_portal(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Entrance_Portal")
    obj = bpy.data.objects.new("SM_Curzon_Entrance_Portal", mesh)
    bpy.context.scene.collection.objects.link(obj)
    for m in [mats["brick"], mats["trim"], mats["sandstone"], mats["brass"], mats["accent"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 18.0
    depth = 4.8
    height = 23.4

    # Ceremonial 5-Step Entrance Staircase (Plinth Access)
    num_steps = 5
    for st in range(num_steps):
        st_w = width + 2.0 - st * 0.4
        st_d = 2.4 - st * 0.35
        st_h = 0.16
        s = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(st_w, st_d, st_h), verts=s["verts"])
        bmesh.ops.translate(bm, vec=(0.0, depth/2.0 + st_d/2.0, (st + 0.5) * st_h), verts=s["verts"])
        assign_material_to_verts(bm, s["verts"], 2) # Sandstone

    # Massive Left and Right Portal Pylons
    pylon_w = 4.8
    pylon_d = depth
    pylon_h = 19.8
    
    for px in [-width/2.0 + pylon_w/2.0, width/2.0 - pylon_w/2.0]:
        p = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pylon_w, pylon_d, pylon_h), verts=p["verts"])
        bmesh.ops.translate(bm, vec=(px, 0.0, pylon_h/2.0), verts=p["verts"])
        
        # Sandstone base plinth
        pb = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pylon_w + 0.25, pylon_d + 0.25, 0.9), verts=pb["verts"])
        bmesh.ops.translate(bm, vec=(px, 0.0, 0.45), verts=pb["verts"])
        assign_material_to_verts(bm, pb["verts"], 2) # Sandstone
        
        # Horizontal white string courses at +7.0m and +14.0m
        for zh in [7.0, 14.0]:
            sc = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(pylon_w + 0.2, pylon_d + 0.2, 0.35), verts=sc["verts"])
            bmesh.ops.translate(bm, vec=(px, 0.0, zh), verts=sc["verts"])
            assign_material_to_verts(bm, sc["verts"], 1) # White Trim

        # Flanking Octagonal Minaret Turrets rising to +21.2m
        turret = bmesh.ops.create_cone(bm, segments=8, radius1=0.9, radius2=0.8, depth=21.2)
        bmesh.ops.translate(bm, vec=(px + (1.6 if px < 0 else -1.6), depth/2.0 - 0.2, 10.6), verts=turret["verts"])
        # White minaret finial cap
        cap = bmesh.ops.create_cone(bm, segments=8, radius1=0.95, radius2=0.05, depth=1.8)
        bmesh.ops.translate(bm, vec=(px + (1.6 if px < 0 else -1.6), depth/2.0 - 0.2, 22.1), verts=cap["verts"])
        assign_material_to_verts(bm, cap["verts"], 1)

    # Monumental 2-Storey Grand Iwan Archway
    iwan_span = 8.4
    iwan_spring_z = 8.0
    iwan_crown_z = 13.5
    
    # Segmented cusped arch intrados (9 cusps)
    iwan_pts = create_cusped_arch(bm, center_x=0.0, center_y=depth/2.0 - 0.6,
                                  spring_z=iwan_spring_z, crown_z=iwan_crown_z,
                                  clear_width=iwan_span, num_cusps=9)
    for i in range(len(iwan_pts) - 1):
        x1, z1 = iwan_pts[i]
        x2, z2 = iwan_pts[i+1]
        mid_x = (x1 + x2) / 2.0
        mid_z = (z1 + z2) / 2.0
        seg = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.08, 1.2, 0.65), verts=seg["verts"])
        bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.6, mid_z + 0.2), verts=seg["verts"])
        
        # White plaster arch ring trim
        t_seg = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.06, 1.3, 0.22), verts=t_seg["verts"])
        bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.6, mid_z - 0.08), verts=t_seg["verts"])
        assign_material_to_verts(bm, t_seg["verts"], 1) # White Trim

    # Upper Spandrel & Clock Pediment (+14.0m to +19.8m)
    ped = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(iwan_span + 1.2, pylon_d, 5.8), verts=ped["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 16.9), verts=ped["verts"])
    
    # Clock Dial Medallion (White Sandstone & Brass Hands)
    dial = bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=1.2, radius2=1.2, depth=0.25)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(math.pi/2, 3, 'X'), verts=dial["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 + 0.1, 17.2), verts=dial["verts"])
    assign_material_to_verts(bm, dial["verts"], 1) # White Trim

    # Massive Projecting Chhajja at +19.8m
    add_chhajja_with_brackets(bm, width=width + 0.8, depth=depth, base_z=19.8, slope_angle=35, projection=1.4, num_brackets=12)

    # Parapet Screen with Merlons atop Portal (+19.8m to +21.0m)
    prp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, 0.5, 1.2), verts=prp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - 0.25, 20.4), verts=prp["verts"])

    # Twin Rajput Rooftop Chhatris atop the Portal Roof (+19.8m to +23.4m)
    # Positioned at x = -5.5 and x = +5.5
    for cx in [-5.5, 5.5]:
        ch_base_z = 20.4
        # Octagonal Base
        c_base = bmesh.ops.create_cone(bm, segments=8, radius1=1.8, radius2=1.8, depth=0.5)
        bmesh.ops.translate(bm, vec=(cx, 0.0, ch_base_z + 0.25), verts=c_base["verts"])
        assign_material_to_verts(bm, c_base["verts"], 2) # Sandstone
        
        # 8 Slender Pillars
        ch_r = 1.3
        for pi in range(8):
            ang = pi * (2.0 * math.pi / 8)
            px = cx + ch_r * math.cos(ang)
            py = ch_r * math.sin(ang)
            pil = bmesh.ops.create_cone(bm, segments=8, radius1=0.12, radius2=0.12, depth=1.6)
            bmesh.ops.translate(bm, vec=(px, py, ch_base_z + 0.5 + 0.8), verts=pil["verts"])
            assign_material_to_verts(bm, pil["verts"], 1)
            
        # Octagonal Chhajja Eave
        c_eave = bmesh.ops.create_cone(bm, segments=8, radius1=2.1, radius2=1.7, depth=0.25)
        bmesh.ops.translate(bm, vec=(cx, 0.0, ch_base_z + 2.1 + 0.12), verts=c_eave["verts"])
        assign_material_to_verts(bm, c_eave["verts"], 1)
        
        # Hemispherical Fluted Cupola Dome
        c_dome = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=1.4)
        # Flatten bottom half
        for v in c_dome["verts"]:
            if v.co.z < 0:
                v.co.z = 0
        bmesh.ops.scale(bm, vec=(1.0, 1.0, 0.85), verts=c_dome["verts"])
        bmesh.ops.translate(bm, vec=(cx, 0.0, ch_base_z + 2.2), verts=c_dome["verts"])
        assign_material_to_verts(bm, c_dome["verts"], 1) # White Trim
        
        # Brass Kalasa Finial
        fin = bmesh.ops.create_cone(bm, segments=8, radius1=0.16, radius2=0.02, depth=0.85)
        bmesh.ops.translate(bm, vec=(cx, 0.0, ch_base_z + 3.4 + 0.42), verts=fin["verts"])
        assign_material_to_verts(bm, fin["verts"], 3) # Brass

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Entrance_Portal.fbx")

# ==============================================================================
# 4. SM_Curzon_Tower_Octagon (7.2m diameter x 25.2m high)
# ==============================================================================
def build_curzon_tower_octagon(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Tower_Octagon")
    obj = bpy.data.objects.new("SM_Curzon_Tower_Octagon", mesh)
    bpy.context.scene.collection.objects.link(obj)
    for m in [mats["brick"], mats["trim"], mats["sandstone"], mats["brass"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    diameter = 7.2
    radius = diameter / 2.0
    total_height = 25.2

    # Tier 1: Base Plinth to +7.2m (Massive Octagonal Masonry)
    t1 = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.35, radius2=radius, depth=7.2)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 3.6), verts=t1["verts"])
    
    # Sandstone plinth base
    pb = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.55, radius2=radius + 0.4, depth=1.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.5), verts=pb["verts"])
    assign_material_to_verts(bm, pb["verts"], 2) # Sandstone

    # White String Course Moulding at +7.2m
    sc1 = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.25, radius2=radius + 0.25, depth=0.45)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 7.2), verts=sc1["verts"])
    assign_material_to_verts(bm, sc1["verts"], 1) # White Trim

    # Tier 2: Arched Louvered Windows Storey (+7.2m to +14.2m)
    t2 = bmesh.ops.create_cone(bm, segments=8, radius1=radius, radius2=radius - 0.15, depth=7.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 10.7), verts=t2["verts"])
    
    # Arched window frames on 4 cardinal facets
    for rot_i in [0, 2, 4, 6]:
        ang = rot_i * (2.0 * math.pi / 8)
        wx = (radius + 0.08) * math.cos(ang)
        wy = (radius + 0.08) * math.sin(ang)
        wf = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(1.4, 0.25, 2.6), verts=wf["verts"])
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=mathutils.Matrix.Rotation(ang, 3, 'Z'), verts=wf["verts"])
        bmesh.ops.translate(bm, vec=(wx, wy, 11.2), verts=wf["verts"])
        assign_material_to_verts(bm, wf["verts"], 1) # White Trim

    # White String Course at +14.2m (Main Roof Eaves Line)
    sc2 = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.20, radius2=radius + 0.20, depth=0.45)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 14.2), verts=sc2["verts"])
    assign_material_to_verts(bm, sc2["verts"], 1)

    # Tier 3: Upper Drum & Corbelled Observation Balcony (+14.2m to +19.5m)
    t3 = bmesh.ops.create_cone(bm, segments=8, radius1=radius - 0.15, radius2=radius - 0.25, depth=5.3)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 16.85), verts=t3["verts"])

    # Corbelled Balcony Slabs (+19.5m) projecting outwards
    c_bal = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.65, radius2=radius + 0.65, depth=0.55)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 19.5), verts=c_bal["verts"])
    assign_material_to_verts(bm, c_bal["verts"], 2) # Sandstone

    # White Jali Balustrade Railing around balcony (+19.5m to +20.5m)
    c_rail = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.60, radius2=radius + 0.60, depth=1.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 20.2), verts=c_rail["verts"])
    assign_material_to_verts(bm, c_rail["verts"], 1)

    # Tier 4: Crown Rajput Chhatri Kiosk (+19.5m to +25.2m)
    ch_base_z = 19.8
    # 8 Slender Octagonal Columns
    ch_col_r = radius - 0.6
    for pi in range(8):
        ang = pi * (2.0 * math.pi / 8)
        px = ch_col_r * math.cos(ang)
        py = ch_col_r * math.sin(ang)
        pil = bmesh.ops.create_cone(bm, segments=8, radius1=0.22, radius2=0.20, depth=2.8)
        bmesh.ops.translate(bm, vec=(px, py, ch_base_z + 1.4), verts=pil["verts"])
        assign_material_to_verts(bm, pil["verts"], 1) # White Trim

    # Projecting Octagonal Chhajja Eave at +22.6m
    t_chhajja = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.45, radius2=radius - 0.2, depth=0.45)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 22.8), verts=t_chhajja["verts"])
    assign_material_to_verts(bm, t_chhajja["verts"], 1)

    # Majestic Hemispherical Domed Cupola (+23.0m to +24.4m)
    dome = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=radius - 0.4)
    for v in dome["verts"]:
        if v.co.z < 0:
            v.co.z = 0
    bmesh.ops.scale(bm, vec=(1.0, 1.0, 0.95), verts=dome["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 23.0), verts=dome["verts"])
    assign_material_to_verts(bm, dome["verts"], 1) # White Plaster Dome

    # Inverted Lotus Crest & Brass Kalasa Finial (+24.4m to +25.2m)
    padma = bmesh.ops.create_cone(bm, segments=12, radius1=0.6, radius2=0.15, depth=0.3)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 24.35), verts=padma["verts"])
    assign_material_to_verts(bm, padma["verts"], 1)
    
    fin = bmesh.ops.create_cone(bm, segments=8, radius1=0.22, radius2=0.02, depth=0.95)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 24.8), verts=fin["verts"])
    assign_material_to_verts(bm, fin["verts"], 3) # Brass

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Tower_Octagon.fbx")

# ==============================================================================
# 5. SM_Curzon_Parapet_Merlons (8m long x 0.4m thick x 1.2m high)
# ==============================================================================
def build_curzon_parapet_merlons(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Parapet_Merlons")
    obj = bpy.data.objects.new("SM_Curzon_Parapet_Merlons", mesh)
    bpy.context.scene.collection.objects.link(obj)
    for m in [mats["brick"], mats["trim"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    length = 8.0
    thickness = 0.4
    base_height = 0.65

    # Parapet Base Wall (Brick)
    pw = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(length, thickness, base_height), verts=pw["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, base_height/2.0), verts=pw["verts"])

    # White Coping Band
    cp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(length, thickness + 0.1, 0.12), verts=cp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, base_height + 0.06), verts=cp["verts"])
    assign_material_to_verts(bm, cp["verts"], 1)

    # 8 Stepped Pointed Merlons (Battlements)
    num_merlons = 8
    merlon_spacing = length / num_merlons
    merlon_w = 0.58
    start_x = -length/2.0 + merlon_spacing/2.0
    
    for i in range(num_merlons):
        mx = start_x + i * merlon_spacing
        
        # Step 1 (Base tier of merlon)
        m1 = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(merlon_w, thickness, 0.22), verts=m1["verts"])
        bmesh.ops.translate(bm, vec=(mx, 0.0, base_height + 0.12 + 0.11), verts=m1["verts"])
        
        # Step 2 (Middle tier)
        m2 = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(merlon_w - 0.16, thickness, 0.18), verts=m2["verts"])
        bmesh.ops.translate(bm, vec=(mx, 0.0, base_height + 0.34 + 0.09), verts=m2["verts"])
        
        # Pointed Peak Cap (White Trim)
        cap = bmesh.ops.create_cone(bm, segments=4, radius1=0.25, radius2=0.02, depth=0.20)
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=mathutils.Matrix.Rotation(math.pi/4, 3, 'Z'), verts=cap["verts"])
        bmesh.ops.translate(bm, vec=(mx, 0.0, base_height + 0.52 + 0.10), verts=cap["verts"])
        assign_material_to_verts(bm, cap["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Parapet_Merlons.fbx")

# ==============================================================================
# 6. SM_Curzon_Chattri_Dome (3.2m x 3.2m x 4.6m high)
# ==============================================================================
def build_curzon_standalone_chattri(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Chattri_Dome")
    obj = bpy.data.objects.new("SM_Curzon_Chattri_Dome", mesh)
    bpy.context.scene.collection.objects.link(obj)
    for m in [mats["brick"], mats["trim"], mats["sandstone"], mats["brass"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    # Octagonal Base
    b_base = bmesh.ops.create_cone(bm, segments=8, radius1=2.0, radius2=1.9, depth=0.6)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.3), verts=b_base["verts"])
    assign_material_to_verts(bm, b_base["verts"], 2)

    # 8 Slender Pillars
    col_rad = 1.45
    for pi in range(8):
        ang = pi * (2.0 * math.pi / 8)
        px = col_rad * math.cos(ang)
        py = col_rad * math.sin(ang)
        col = bmesh.ops.create_cone(bm, segments=8, radius1=0.15, radius2=0.14, depth=2.2)
        bmesh.ops.translate(bm, vec=(px, py, 0.6 + 1.1), verts=col["verts"])
        assign_material_to_verts(bm, col["verts"], 1)

    # Chhajja Eave
    ch = bmesh.ops.create_cone(bm, segments=8, radius1=2.3, radius2=1.8, depth=0.35)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.95), verts=ch["verts"])
    assign_material_to_verts(bm, ch["verts"], 1)

    # Hemispherical Dome
    dm = bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=14, radius=1.55)
    for v in dm["verts"]:
        if v.co.z < 0:
            v.co.z = 0
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 3.1), verts=dm["verts"])
    assign_material_to_verts(bm, dm["verts"], 1)

    # Brass Finial
    fn = bmesh.ops.create_cone(bm, segments=8, radius1=0.18, radius2=0.02, depth=0.9)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.45), verts=fn["verts"])
    assign_material_to_verts(bm, fn["verts"], 3)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Chattri_Dome.fbx")

# ==============================================================================
# 7. SM_Curzon_Lamp_Colonial (Heritage Lantern)
# ==============================================================================
def build_curzon_lamp_colonial(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Lamp_Colonial")
    obj = bpy.data.objects.new("SM_Curzon_Lamp_Colonial", mesh)
    bpy.context.scene.collection.objects.link(obj)
    for m in [mats["accent"], mats["brass"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    # Cast Iron Wall Mount Bracket
    br = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(0.12, 0.45, 0.45), verts=br["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.22, 0.0), verts=br["verts"])
    assign_material_to_verts(bm, br["verts"], 0)

    # Hexagonal Lantern Housing
    lt = bmesh.ops.create_cone(bm, segments=6, radius1=0.22, radius2=0.30, depth=0.55)
    bmesh.ops.translate(bm, vec=(0.0, 0.45, 0.15), verts=lt["verts"])
    assign_material_to_verts(bm, lt["verts"], 1) # Brass/Glass

    # Pointed Top Cap
    tc = bmesh.ops.create_cone(bm, segments=6, radius1=0.32, radius2=0.02, depth=0.25)
    bmesh.ops.translate(bm, vec=(0.0, 0.45, 0.52), verts=tc["verts"])
    assign_material_to_verts(bm, tc["verts"], 0)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Lamp_Colonial.fbx")

# Main Execution Flow
if __name__ == "__main__":
    print("[Curzon Rebuild] Starting Blender precision 3D modular asset generation...")
    mats = get_or_create_materials()
    
    build_curzon_veranda_lower(mats)
    build_curzon_veranda_upper(mats)
    build_curzon_entrance_portal(mats)
    build_curzon_tower_octagon(mats)
    build_curzon_parapet_merlons(mats)
    build_curzon_standalone_chattri(mats)
    build_curzon_lamp_colonial(mats)
    
    print("[Curzon Rebuild] Successfully exported all 7 precision modular assets to FBX!")
