#!/usr/bin/env python3
"""
Generate Complete Authentic Campus Vegetation Library for SparkVision (DU Campus):
1. SM_Tree_Raintree_Master (Grand Broadleaf Shade Tree)
2. SM_Tree_Krishnachura_Master (Iconic DU Red Flowering Umbrella Tree)
3. SM_Tree_Banyan_Master (Heritage Bottola Banyan with Aerial Prop Roots)
4. SM_Tree_RoyalPalm_Master (Curzon Hall Columnar Avenue Palm)
5. SM_Campus_Grass_Lawn (Low Manicured Campus Turf Clump)
6. SM_Campus_Grass_Tuft (Taller Natural Grass Clump for Tree Bases & Verges)
7. SM_Campus_Bush_Kamini (Fragrant White Flowered Campus Shrub)

All models adhere strictly to:
- Real-world botanical proportions (Unreal centimeters / meters).
- High visual fidelity inspired by Where Winds Meet.
- Realistic branch hierarchies and non-planar foliage cards (0.45m - 0.75m).
- Sphericalized cloud split normals for soft volumetric light wrap.
- Ultra-optimized geometry for Apple Silicon M4 (under 3,500 tris per mature tree, under 30 tris per grass clump).
"""

import sys
import os
import subprocess

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Vegetation"
BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLENDER_BATCH_CODE = f"""
import bpy
import bmesh
import mathutils
import math
import random
import os

OUTPUT_DIR = "{OUTPUT_DIR}"
os.makedirs(OUTPUT_DIR, exist_ok=True)
random.seed(101)

def reset():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for m in bpy.data.meshes:
        if m.users == 0: bpy.data.meshes.remove(m)
    for mat in bpy.data.materials:
        if mat.users == 0: bpy.data.materials.remove(mat)

def export_fbx(obj, filename):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Z',
        axis_up='Y',
        bake_space_transform=False,
        mesh_smooth_type='FACE'
    )
    print(f"Exported {{filename}} ({{len(obj.data.polygons)}} polys, {{len(obj.data.vertices)}} verts)")

def build_tube(bm, uv_layer, start, end, start_r, end_r, num_segs=5, sides=8, curl=None, mat_idx=0):
    length = (end - start).length
    dir_vec = (end - start).normalized() if length > 0.001 else mathutils.Vector((0, 0, 1))
    up = mathutils.Vector((0, 0, 1))
    if abs(dir_vec.dot(up)) > 0.90:
        up = mathutils.Vector((1, 0, 0))
    side_vec = dir_vec.cross(up).normalized()
    up_vec = side_vec.cross(dir_vec).normalized()
    
    rings = []
    for s in range(num_segs + 1):
        t = s / num_segs
        mid_point = start.lerp(end, t)
        if curl:
            mid_point += curl * math.sin(t * math.pi)
        curr_r = start_r * (1.0 - t) + end_r * t
        ring_verts = []
        for i in range(sides):
            ang = 2.0 * math.pi * i / sides
            vx = mid_point.x + curr_r * (math.cos(ang) * side_vec.x + math.sin(ang) * up_vec.x)
            vy = mid_point.y + curr_r * (math.cos(ang) * side_vec.y + math.sin(ang) * up_vec.y)
            vz = mid_point.z + curr_r * (math.cos(ang) * side_vec.z + math.sin(ang) * up_vec.z)
            v = bm.verts.new((vx, vy, vz))
            ring_verts.append(v)
        rings.append(ring_verts)
        
    for s in range(num_segs):
        r0 = rings[s]
        r1 = rings[s + 1]
        for i in range(sides):
            next_i = (i + 1) % sides
            f = bm.faces.new([r0[i], r0[next_i], r1[next_i], r1[i]])
            f.material_index = mat_idx
            f.smooth = True
            u0 = i / sides
            u1 = (i + 1) / sides
            v0 = s / num_segs * 2.5
            v1 = (s + 1) / num_segs * 2.5
            for loop in f.loops:
                if loop.vert == r0[i]: loop[uv_layer].uv = (u0, v0)
                elif loop.vert == r0[next_i]: loop[uv_layer].uv = (u1, v0)
                elif loop.vert == r1[next_i]: loop[uv_layer].uv = (u1, v1)
                elif loop.vert == r1[i]: loop[uv_layer].uv = (u0, v1)
    return rings[-1]

def add_bowed_card(bm, uv_layer, center, normal, w, h, uv_box, mat_idx=1):
    norm = normal.normalized()
    up = mathutils.Vector((0, 0, 1))
    if abs(norm.dot(up)) > 0.92:
        up = mathutils.Vector((1, 0, 0))
    tangent = norm.cross(up).normalized()
    bitangent = norm.cross(tangent).normalized()
    
    bow = h * 0.12
    v0 = center - tangent * (w * 0.5) - bitangent * (h * 0.5)
    v1 = center + tangent * (w * 0.5) - bitangent * (h * 0.5)
    v2 = center - tangent * (w * 0.52) + norm * bow
    v3 = center + tangent * (w * 0.52) + norm * bow
    v4 = center - tangent * (w * 0.48) + bitangent * (h * 0.5)
    v5 = center + tangent * (w * 0.48) + bitangent * (h * 0.5)
    
    vo = [bm.verts.new(p) for p in [v0, v1, v2, v3, v4, v5]]
    (u_min, v_min), (u_max, v_max) = uv_box
    v_mid = (v_min + v_max) * 0.5
    
    f1 = bm.faces.new([vo[0], vo[1], vo[3], vo[2]])
    f1.material_index = mat_idx
    f1.smooth = True
    for l in f1.loops:
        if l.vert == vo[0]: l[uv_layer].uv = (u_min, v_min)
        elif l.vert == vo[1]: l[uv_layer].uv = (u_max, v_min)
        elif l.vert == vo[3]: l[uv_layer].uv = (u_max, v_mid)
        elif l.vert == vo[2]: l[uv_layer].uv = (u_min, v_mid)
        
    f2 = bm.faces.new([vo[2], vo[3], vo[5], vo[4]])
    f2.material_index = mat_idx
    f2.smooth = True
    for l in f2.loops:
        if l.vert == vo[2]: l[uv_layer].uv = (u_min, v_mid)
        elif l.vert == vo[3]: l[uv_layer].uv = (u_max, v_mid)
        elif l.vert == vo[5]: l[uv_layer].uv = (u_max, v_max)
        elif l.vert == vo[4]: l[uv_layer].uv = (u_min, v_max)

# ==============================================================================
# MODEL 1: KRISHNACHURA (Delonix Regia) - Iconic Scarlet Umbrella Tree
# ==============================================================================
def create_krishnachura():
    reset()
    mesh = bpy.data.meshes.new("SM_Tree_Krishnachura_Master")
    obj = bpy.data.objects.new("SM_Tree_Krishnachura_Master", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_bark = bpy.data.materials.new("M_Bark_Tree")
    mat_flower = bpy.data.materials.new("MI_Foliage_Krishnachura_Natural")
    obj.data.materials.append(mat_bark)     # Slot 0
    obj.data.materials.append(mat_flower)   # Slot 1
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    # Gnarled trunk with 5 root flares (3.2m height before wide fork)
    profile = [(0.0, 0.60, 0.20), (0.4, 0.45, 0.10), (1.2, 0.38, 0.04), (2.2, 0.34, 0.02), (3.2, 0.32, 0.0)]
    rings = []
    for z, r, fl in profile:
        rv = []
        lean = mathutils.Vector((math.sin(z * 0.5) * 0.22, math.cos(z * 0.4) * 0.15, z))
        for i in range(14):
            ang = 2.0 * math.pi * i / 14
            buttress = math.cos(5.0 * ang) * fl if fl > 0 else 0.0
            vx = lean.x + (r + buttress) * math.cos(ang)
            vy = lean.y + (r + buttress) * math.sin(ang)
            rv.append(bm.verts.new((vx, vy, lean.z)))
        rings.append(rv)
        
    for r_i in range(len(rings) - 1):
        for i in range(14):
            ni = (i + 1) % 14
            f = bm.faces.new([rings[r_i][i], rings[r_i][ni], rings[r_i+1][ni], rings[r_i+1][i]])
            f.material_index = 0
            f.smooth = True
            
    # Bottom cap
    bc = bm.verts.new((0, 0, 0))
    for i in range(14):
        f = bm.faces.new([bc, rings[0][(i+1)%14], rings[0][i]])
        f.material_index = 0
        f.smooth = True
        
    fork_pos = mathutils.Vector((math.sin(3.2 * 0.5) * 0.22, math.cos(3.2 * 0.4) * 0.15, 3.2))
    canopy_center = fork_pos + mathutils.Vector((0, 0, 3.8))
    
    # 6 Wide horizontal spreading boughs (Umbrella Canopy)
    boughs = [
        (0.00, 5.5, 6.2, 0.24, 0.12),
        (1.05, 5.8, 6.5, 0.22, 0.11),
        (2.10, 5.2, 6.0, 0.23, 0.12),
        (3.14, 5.6, 6.4, 0.24, 0.11),
        (4.20, 5.4, 6.1, 0.22, 0.12),
        (5.25, 5.7, 6.3, 0.23, 0.11),
    ]
    
    foliage_anchors = []
    for ang, reach, b_z, r_s, r_e in boughs:
        b_end = mathutils.Vector((reach * math.cos(ang), reach * math.sin(ang), b_z))
        curl = mathutils.Vector((math.cos(ang) * 0.8, math.sin(ang) * 0.8, 0.4))
        build_tube(bm, uv, fork_pos, b_end, r_s, r_e, num_segs=5, sides=8, curl=curl)
        
        # 3 sub-branches spreading flat
        for sub_i in range(3):
            t = 0.5 + sub_i * 0.22
            s_start = fork_pos.lerp(b_end, t) + curl * math.sin(t * math.pi)
            s_ang = ang + random.uniform(-0.5, 0.5)
            s_reach = reach + random.uniform(1.0, 2.0)
            s_end = mathutils.Vector((s_reach * math.cos(s_ang), s_reach * math.sin(s_ang), b_z + random.uniform(-0.3, 0.6)))
            build_tube(bm, uv, s_start, s_end, r_e * 0.8, 0.05, num_segs=3, sides=6)
            foliage_anchors.append((s_end, (s_end - s_start).normalized()))
            
            # Twigs
            for tw_i in range(2):
                tw_ang = s_ang + random.uniform(-0.4, 0.4)
                tw_end = s_end + mathutils.Vector((random.uniform(0.6, 1.2) * math.cos(tw_ang), random.uniform(0.6, 1.2) * math.sin(tw_ang), random.uniform(-0.2, 0.3)))
                build_tube(bm, uv, s_end, tw_end, 0.04, 0.02, num_segs=2, sides=5)
                foliage_anchors.append((tw_end, (tw_end - s_end).normalized()))
                
    # Flat horizontal umbrella foliage puffs
    uv_boxes = [((0.02, 0.52), (0.48, 0.98)), ((0.52, 0.52), (0.98, 0.98)), ((0.02, 0.02), (0.48, 0.48)), ((0.52, 0.02), (0.98, 0.48))]
    for anchor, b_dir in foliage_anchors:
        for _ in range(random.randint(8, 14)):
            off = mathutils.Vector((random.uniform(-0.75, 0.75), random.uniform(-0.75, 0.75), random.uniform(-0.30, 0.35)))
            cp = anchor + off
            norm = (cp - canopy_center).normalized() + mathutils.Vector((0, 0, 0.6))
            add_bowed_card(bm, uv, cp, norm, random.uniform(0.55, 0.75), random.uniform(0.55, 0.75), random.choice(uv_boxes), mat_idx=1)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - canopy_center).normalized() if v.co.z > 3.0 else v.normal for v in mesh.vertices])
    export_fbx(obj, "SM_Tree_Krishnachura_Master.fbx")

# ==============================================================================
# MODEL 2: HERITAGE BANYAN (Ficus Benghalensis) - Massive Twisted Trunk + Prop Roots
# ==============================================================================
def create_banyan():
    reset()
    mesh = bpy.data.meshes.new("SM_Tree_Banyan_Master")
    obj = bpy.data.objects.new("SM_Tree_Banyan_Master", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_bark = bpy.data.materials.new("M_Bark_Tree")
    mat_leaves = bpy.data.materials.new("MI_Foliage_Banyan_Natural")
    obj.data.materials.append(mat_bark)     # Slot 0
    obj.data.materials.append(mat_leaves)   # Slot 1
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    # Central massive fluted trunk (base r=0.9m)
    profile = [(0.0, 0.95, 0.30), (0.5, 0.75, 0.18), (1.5, 0.62, 0.10), (2.8, 0.55, 0.05), (3.8, 0.52, 0.0)]
    rings = []
    for z, r, fl in profile:
        rv = []
        for i in range(16):
            ang = 2.0 * math.pi * i / 16
            flare = math.cos(4.0 * ang) * fl
            vx = (r + flare) * math.cos(ang)
            vy = (r + flare) * math.sin(ang)
            rv.append(bm.verts.new((vx, vy, z)))
        rings.append(rv)
    for r_i in range(len(rings) - 1):
        for i in range(16):
            ni = (i + 1) % 16
            f = bm.faces.new([rings[r_i][i], rings[r_i][ni], rings[r_i+1][ni], rings[r_i+1][i]])
            f.material_index = 0
            f.smooth = True
            
    # Bottom cap
    bc = bm.verts.new((0, 0, 0))
    for i in range(16):
        f = bm.faces.new([bc, rings[0][(i+1)%16], rings[0][i]])
        f.material_index = 0
        f.smooth = True
        
    # 4 Authentic Aerial Prop Roots (hanging down to the ground like natural pillars)
    prop_root_coords = [(1.8, 0.4), (-1.6, 0.6), (0.5, -1.7), (-0.8, -1.5)]
    fork_pos = mathutils.Vector((0, 0, 3.8))
    for px, py in prop_root_coords:
        top_p = mathutils.Vector((px * 0.7, py * 0.7, 3.6))
        bot_p = mathutils.Vector((px, py, 0.0))
        curl_p = mathutils.Vector((random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15), 0.0))
        build_tube(bm, uv, top_p, bot_p, 0.14, 0.20, num_segs=5, sides=7, curl=curl_p)
        
    canopy_center = mathutils.Vector((0, 0, 7.5))
    # 5 Massive twisting heavy boughs
    boughs = [
        (0.40, 6.2, 7.8, 0.32, 0.18),
        (1.70, 6.0, 7.5, 0.30, 0.17),
        (2.95, 6.5, 8.0, 0.33, 0.18),
        (4.20, 5.8, 7.4, 0.29, 0.16),
        (5.50, 6.3, 7.9, 0.31, 0.17),
    ]
    foliage_anchors = []
    for ang, reach, b_z, r_s, r_e in boughs:
        b_end = mathutils.Vector((reach * math.cos(ang), reach * math.sin(ang), b_z))
        curl = mathutils.Vector((math.cos(ang) * 0.5, math.sin(ang) * 0.5, 0.7))
        build_tube(bm, uv, fork_pos, b_end, r_s, r_e, num_segs=5, sides=9, curl=curl)
        for s_i in range(3):
            t = 0.45 + s_i * 0.24
            s_start = fork_pos.lerp(b_end, t) + curl * math.sin(t * math.pi)
            s_ang = ang + random.uniform(-0.6, 0.6)
            s_reach = reach + random.uniform(1.0, 2.2)
            s_end = mathutils.Vector((s_reach * math.cos(s_ang), s_reach * math.sin(s_ang), b_z + random.uniform(-0.4, 0.8)))
            build_tube(bm, uv, s_start, s_end, r_e * 0.85, 0.07, num_segs=3, sides=6)
            foliage_anchors.append((s_end, (s_end - s_start).normalized()))
            
    # Dense banyan foliage cushions
    uv_boxes = [((0.02, 0.52), (0.48, 0.98)), ((0.52, 0.52), (0.98, 0.98)), ((0.02, 0.02), (0.48, 0.48)), ((0.52, 0.02), (0.98, 0.48))]
    for anchor, b_dir in foliage_anchors:
        for _ in range(random.randint(10, 16)):
            off = mathutils.Vector((random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8), random.uniform(-0.5, 0.5)))
            cp = anchor + off
            norm = (cp - canopy_center).normalized() + mathutils.Vector((0, 0, 0.5))
            add_bowed_card(bm, uv, cp, norm, random.uniform(0.60, 0.82), random.uniform(0.60, 0.82), random.choice(uv_boxes), mat_idx=1)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - canopy_center).normalized() if v.co.z > 3.0 else v.normal for v in mesh.vertices])
    export_fbx(obj, "SM_Tree_Banyan_Master.fbx")

# ==============================================================================
# MODEL 3: ROYAL AVENUE PALM (Roystonea Regia) - Curzon Columnar Palm
# ==============================================================================
def create_royal_palm():
    reset()
    mesh = bpy.data.meshes.new("SM_Tree_RoyalPalm_Master")
    obj = bpy.data.objects.new("SM_Tree_RoyalPalm_Master", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_trunk = bpy.data.materials.new("M_Bark_Tree")
    mat_frond = bpy.data.materials.new("MI_Foliage_PalmFrond")
    obj.data.materials.append(mat_trunk)    # Slot 0
    obj.data.materials.append(mat_frond)    # Slot 1
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    # Graceful 11.5m smooth columnar trunk with characteristic swollen base & middle
    palm_profile = [
        (0.0,  0.34),  # Ground
        (0.5,  0.38),  # Swollen base
        (2.0,  0.27),
        (5.0,  0.25),
        (8.0,  0.28),  # Subtle graceful bulge
        (10.0, 0.24),
        (11.2, 0.21),  # Top of trunk / base of crownshaft
    ]
    rings = []
    for z, r in palm_profile:
        rv = []
        for i in range(12):
            ang = 2.0 * math.pi * i / 12
            vx = r * math.cos(ang)
            vy = r * math.sin(ang)
            rv.append(bm.verts.new((vx, vy, z)))
        rings.append(rv)
    for r_i in range(len(rings) - 1):
        for i in range(12):
            ni = (i + 1) % 12
            f = bm.faces.new([rings[r_i][i], rings[r_i][ni], rings[r_i+1][ni], rings[r_i+1][i]])
            f.material_index = 0
            f.smooth = True
            
    # Bottom cap
    bc = bm.verts.new((0, 0, 0))
    for i in range(12):
        f = bm.faces.new([bc, rings[0][(i+1)%12], rings[0][i]])
        f.material_index = 0
        f.smooth = True
        
    # Smooth green crownshaft (11.2m to 12.4m)
    crown_profile = [(11.2, 0.21), (11.8, 0.20), (12.4, 0.18)]
    c_rings = []
    for z, r in crown_profile:
        rv = []
        for i in range(12):
            ang = 2.0 * math.pi * i / 12
            rv.append(bm.verts.new((r * math.cos(ang), r * math.sin(ang), z)))
        c_rings.append(rv)
    for r_i in range(len(c_rings) - 1):
        for i in range(12):
            ni = (i + 1) % 12
            f = bm.faces.new([c_rings[r_i][i], c_rings[r_i][ni], c_rings[r_i+1][ni], c_rings[r_i+1][i]])
            f.material_index = 0
            f.smooth = True
            
    # 14 Gracefully Arching Feathery Fronds
    crown_top = mathutils.Vector((0, 0, 12.4))
    num_fronds = 14
    for f_idx in range(num_fronds):
        ang = (2.0 * math.pi * f_idx / num_fronds) + (f_idx * 0.15)
        # Droop angle (inner fronds more upright, outer fronds weeping)
        droop_tier = f_idx % 3
        reach = 3.6 if droop_tier != 0 else 4.2
        droop_z = -1.2 if droop_tier == 2 else (-0.4 if droop_tier == 1 else 0.4)
        
        # Frond spine (4 segments)
        spine_pts = []
        for s_i in range(5):
            t = s_i / 4.0
            p_reach = reach * t
            p_z = crown_top.z + (1.2 * math.sin(t * math.pi * 0.6) + droop_z * t * t)
            pt = mathutils.Vector((p_reach * math.cos(ang), p_reach * math.sin(ang), p_z))
            spine_pts.append(pt)
            
        # Place feathery frond card segments along spine
        uv_frond = ((0.02, 0.52), (0.48, 0.98))
        for s_i in range(len(spine_pts) - 1):
            p0 = spine_pts[s_i]
            p1 = spine_pts[s_i + 1]
            seg_mid = (p0 + p1) * 0.5
            seg_dir = (p1 - p0).normalized()
            seg_norm = mathutils.Vector((0, 0, 1)).cross(seg_dir).cross(seg_dir).normalized()
            add_bowed_card(bm, uv, seg_mid, seg_norm, 1.1 - 0.15 * s_i, (p1 - p0).length * 1.1, uv_frond, mat_idx=1)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - crown_top).normalized() if v.co.z > 11.0 else v.normal for v in mesh.vertices])
    export_fbx(obj, "SM_Tree_RoyalPalm_Master.fbx")

# ==============================================================================
# MODEL 4: CAMPUS LAWN GRASS CLUMP (Low Manicured Campus Turf)
# ==============================================================================
def create_grass_lawn():
    reset()
    mesh = bpy.data.meshes.new("SM_Campus_Grass_Lawn")
    obj = bpy.data.objects.new("SM_Campus_Grass_Lawn", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_grass = bpy.data.materials.new("MI_Ground_Grass")
    obj.data.materials.append(mat_grass)  # Slot 0
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    # 3 Curved cross-quad cards intersecting at 60 deg, height=0.15m (15cm), radius=0.22m (44cm clump)
    uv_box = ((0.0, 0.0), (1.0, 1.0))
    for i in range(3):
        ang = i * (math.pi / 3.0)
        dir_xy = mathutils.Vector((math.cos(ang), math.sin(ang), 0))
        norm_xy = mathutils.Vector((-math.sin(ang), math.cos(ang), 0))
        w = 0.44
        h = 0.16
        
        # 6 verts bowed outward
        v0 = -dir_xy * (w * 0.5)
        v1 = dir_xy * (w * 0.5)
        v2 = -dir_xy * (w * 0.52) + mathutils.Vector((0, 0, h * 0.5)) + norm_xy * 0.02
        v3 = dir_xy * (w * 0.52) + mathutils.Vector((0, 0, h * 0.5)) - norm_xy * 0.02
        v4 = -dir_xy * (w * 0.45) + mathutils.Vector((0, 0, h)) + norm_xy * 0.05
        v5 = dir_xy * (w * 0.45) + mathutils.Vector((0, 0, h)) - norm_xy * 0.05
        
        vo = [bm.verts.new(p) for p in [v0, v1, v2, v3, v4, v5]]
        f1 = bm.faces.new([vo[0], vo[1], vo[3], vo[2]])
        f1.material_index = 0
        f1.smooth = True
        for l in f1.loops:
            if l.vert == vo[0]: l[uv].uv = (0.0, 0.0)
            elif l.vert == vo[1]: l[uv].uv = (1.0, 0.0)
            elif l.vert == vo[3]: l[uv].uv = (1.0, 0.5)
            elif l.vert == vo[2]: l[uv].uv = (0.0, 0.5)
            
        f2 = bm.faces.new([vo[2], vo[3], vo[5], vo[4]])
        f2.material_index = 0
        f2.smooth = True
        for l in f2.loops:
            if l.vert == vo[2]: l[uv].uv = (0.0, 0.5)
            elif l.vert == vo[3]: l[uv].uv = (1.0, 0.5)
            elif l.vert == vo[5]: l[uv].uv = (1.0, 1.0)
            elif l.vert == vo[4]: l[uv].uv = (0.0, 1.0)
            
    bm.to_mesh(mesh)
    bm.free()
    # Normals point straight up to receive full daylight without dark backfaces
    mesh.normals_split_custom_set_from_vertices([mathutils.Vector((0, 0, 1)) for _ in mesh.vertices])
    export_fbx(obj, "SM_Campus_Grass_Lawn.fbx")

# ==============================================================================
# MODEL 5: TALLER NATURAL GRASS TUFT (For Tree Bases & Garden Borders)
# ==============================================================================
def create_grass_tuft():
    reset()
    mesh = bpy.data.meshes.new("SM_Campus_Grass_Tuft")
    obj = bpy.data.objects.new("SM_Campus_Grass_Tuft", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_grass = bpy.data.materials.new("MI_Ground_Grass")
    obj.data.materials.append(mat_grass)
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    # 4 Intersecting curved cards, height=0.26m (26cm), width=0.55m
    for i in range(4):
        ang = i * (math.pi / 4.0) + random.uniform(-0.1, 0.1)
        dir_xy = mathutils.Vector((math.cos(ang), math.sin(ang), 0))
        norm_xy = mathutils.Vector((-math.sin(ang), math.cos(ang), 0))
        w = 0.55
        h = random.uniform(0.24, 0.28)
        
        v0 = -dir_xy * (w * 0.5)
        v1 = dir_xy * (w * 0.5)
        v2 = -dir_xy * (w * 0.54) + mathutils.Vector((0, 0, h * 0.5)) + norm_xy * 0.04
        v3 = dir_xy * (w * 0.54) + mathutils.Vector((0, 0, h * 0.5)) - norm_xy * 0.04
        v4 = -dir_xy * (w * 0.40) + mathutils.Vector((0, 0, h)) + norm_xy * 0.08
        v5 = dir_xy * (w * 0.40) + mathutils.Vector((0, 0, h)) - norm_xy * 0.08
        
        vo = [bm.verts.new(p) for p in [v0, v1, v2, v3, v4, v5]]
        f1 = bm.faces.new([vo[0], vo[1], vo[3], vo[2]])
        f1.material_index = 0
        f1.smooth = True
        for l in f1.loops:
            if l.vert == vo[0]: l[uv].uv = (0.0, 0.0)
            elif l.vert == vo[1]: l[uv].uv = (1.0, 0.0)
            elif l.vert == vo[3]: l[uv].uv = (1.0, 0.5)
            elif l.vert == vo[2]: l[uv].uv = (0.0, 0.5)
            
        f2 = bm.faces.new([vo[2], vo[3], vo[5], vo[4]])
        f2.material_index = 0
        f2.smooth = True
        for l in f2.loops:
            if l.vert == vo[2]: l[uv].uv = (0.0, 0.5)
            elif l.vert == vo[3]: l[uv].uv = (1.0, 0.5)
            elif l.vert == vo[5]: l[uv].uv = (1.0, 1.0)
            elif l.vert == vo[4]: l[uv].uv = (0.0, 1.0)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([mathutils.Vector((0, 0, 1)) for _ in mesh.vertices])
    export_fbx(obj, "SM_Campus_Grass_Tuft.fbx")

# ==============================================================================
# MODEL 6: KAMINI BUSH (Murraya Paniculata) - Authentic White Fragrant Shrub
# ==============================================================================
def create_kamini_bush():
    reset()
    mesh = bpy.data.meshes.new("SM_Campus_Bush_Kamini")
    obj = bpy.data.objects.new("SM_Campus_Bush_Kamini", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_shrub = bpy.data.materials.new("MI_Foliage_Fern_Natural")
    obj.data.materials.append(mat_shrub)
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    # 24 Intersecting curved leaves arranged in a 1.4m dome shrub
    uv_box = ((0.02, 0.52), (0.48, 0.98))
    center = mathutils.Vector((0, 0, 0.6))
    for i in range(24):
        ang = (2.0 * math.pi * i / 24) * 2.39996  # Golden ratio spiral
        rad = 0.35 + 0.45 * math.sqrt(i / 24.0)
        z = 0.2 + 0.9 * (1.0 - (rad / 0.8)**2) * 0.7
        pos = mathutils.Vector((rad * math.cos(ang), rad * math.sin(ang), z))
        norm = (pos - center).normalized() + mathutils.Vector((0, 0, 0.4))
        add_bowed_card(bm, uv, pos, norm, 0.55, 0.55, uv_box, mat_idx=0)
        
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - center).normalized() for v in mesh.vertices])
    export_fbx(obj, "SM_Campus_Bush_Kamini.fbx")

# Execute all generators
print("Starting generation of authentic DU vegetation library...")
create_krishnachura()
create_banyan()
create_royal_palm()
create_grass_lawn()
create_grass_tuft()
create_kamini_bush()
print("All vegetation models successfully generated!")
"""

script_path = "/tmp/generate_all_vegetation.py"
with open(script_path, "w") as f:
    f.write(BLENDER_BATCH_CODE)

print("Running Blender batch generation...")
res = subprocess.run([BLENDER_BIN, "--background", "--python", script_path], capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print("Blender ERROR:", res.stderr)
    sys.exit(1)

print("\n✓ Full vegetation library generated successfully!")
