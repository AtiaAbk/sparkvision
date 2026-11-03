#!/usr/bin/env python3
"""
Generate Complete Authentic Campus Vegetation Library in Unreal Centimeters (1 unit = 1 cm):
1. SM_Tree_Raintree_Master (12.8m tall, 14m wide umbrella canopy)
2. SM_Tree_Krishnachura_Master (9.5m tall, 12m wide iconic scarlet flowering umbrella)
3. SM_Tree_Banyan_Master (11.2m tall, 14m wide massive trunk + 4 prop roots)
4. SM_Tree_RoyalPalm_Master (13.5m tall, 7.5m wide graceful avenue palm)
5. SM_Campus_Grass_Lawn (16cm high, 45cm wide manicured turf clump)
6. SM_Campus_Grass_Tuft (26cm high, 60cm wide natural clump for tree bases & borders)
7. SM_Campus_Bush_Kamini (120cm high, 160cm wide fragrant flowering shrub)
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
            v0 = s / num_segs * 3.0
            v1 = (s + 1) / num_segs * 3.0
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

atlas_uvs = [
    ((0.02, 0.52), (0.48, 0.98)),
    ((0.52, 0.52), (0.98, 0.98)),
    ((0.02, 0.02), (0.48, 0.48)),
    ((0.52, 0.02), (0.98, 0.48)),
]

# ==============================================================================
# MODEL 1: GRAND RAIN TREE MASTER (All coords in CM!)
# ==============================================================================
def create_raintree_master():
    reset()
    mesh = bpy.data.meshes.new("SM_Tree_Raintree_Master")
    obj = bpy.data.objects.new("SM_Tree_Raintree_Master", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_bark = bpy.data.materials.new("M_Bark_Tree")
    mat_foliage = bpy.data.materials.new("M_Master_NaturalFoliage")
    obj.data.materials.append(mat_bark)     # Slot 0
    obj.data.materials.append(mat_foliage)  # Slot 1
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    # Trunk profile in cm: height to fork = 420 cm
    profile = [
        (0.0, 70.0, 25.0),
        (40.0, 55.0, 15.0),
        (90.0, 48.0, 8.0),
        (160.0, 42.0, 3.0),
        (250.0, 38.0, 2.0),
        (340.0, 35.0, 2.0),
        (420.0, 34.0, 2.0),
    ]
    rings = []
    for z, r, flare in profile:
        rv = []
        lean_x = math.sin(z * 0.004) * 12.0
        lean_y = math.cos(z * 0.003) * 8.0
        for i in range(16):
            ang = (2.0 * math.pi * i) / 16
            flute = math.cos(5.0 * ang) * flare if flare > 0 else 0.0
            noise = math.sin(ang * 7.0 + z * 0.03) * 2.0
            curr_r = max(10.0, r + flute + noise)
            vx = lean_x + curr_r * math.cos(ang)
            vy = lean_y + curr_r * math.sin(ang)
            rv.append(bm.verts.new((vx, vy, z)))
        rings.append(rv)
        
    for r_i in range(len(rings) - 1):
        for i in range(16):
            ni = (i + 1) % 16
            f = bm.faces.new([rings[r_i][i], rings[r_i][ni], rings[r_i+1][ni], rings[r_i+1][i]])
            f.material_index = 0
            f.smooth = True
            
    bc = bm.verts.new((0, 0, 0))
    for i in range(16):
        f = bm.faces.new([bc, rings[0][(i+1)%16], rings[0][i]])
        f.material_index = 0
        f.smooth = True
        
    fork_pos = mathutils.Vector((0, 0, 420.0))
    canopy_center = mathutils.Vector((0, 0, 850.0))
    
    boughs = [
        (0.00,  620.0, 880.0, 28.0, 16.0),
        (1.25,  680.0, 920.0, 26.0, 15.0),
        (2.50,  600.0, 850.0, 27.0, 15.0),
        (3.80,  660.0, 900.0, 28.0, 16.0),
        (5.05,  640.0, 870.0, 26.0, 15.0),
    ]
    foliage_anchors = []
    for b_ang, reach, b_h, r_s, r_e in boughs:
        b_end = mathutils.Vector((reach * math.cos(b_ang), reach * math.sin(b_ang), b_h))
        curl = mathutils.Vector((math.cos(b_ang) * 60.0, math.sin(b_ang) * 60.0, 80.0))
        build_tube(bm, uv, fork_pos, b_end, r_s, r_e, num_segs=6, sides=10, curl=curl)
        for s_i in range(3):
            t = 0.45 + s_i * 0.25
            s_start = fork_pos.lerp(b_end, t) + curl * math.sin(t * math.pi)
            s_ang = b_ang + random.uniform(-0.65, 0.65)
            s_reach = reach + random.uniform(120.0, 240.0)
            s_z = b_h + random.uniform(60.0, 180.0)
            s_end = mathutils.Vector((s_reach * math.cos(s_ang), s_reach * math.sin(s_ang), s_z))
            s_curl = mathutils.Vector((0, 0, random.uniform(20.0, 50.0)))
            build_tube(bm, uv, s_start, s_end, r_e * 0.85, 8.0, num_segs=4, sides=8, curl=s_curl)
            foliage_anchors.append((s_start.lerp(s_end, 0.6), s_end - s_start))
            for tw_i in range(3):
                tw_ang = s_ang + random.uniform(-0.5, 0.5)
                tw_reach = s_reach + random.uniform(80.0, 160.0)
                tw_z = s_z + random.uniform(-40.0, 90.0)
                tw_end = mathutils.Vector((tw_reach * math.cos(tw_ang), tw_reach * math.sin(tw_ang), tw_z))
                tw_start = s_end.lerp(s_start, 0.2 * tw_i)
                build_tube(bm, uv, tw_start, tw_end, 6.0, 2.5, num_segs=2, sides=6)
                foliage_anchors.append((tw_end, (tw_end - tw_start).normalized()))
                
    # Central crown
    crown_end = mathutils.Vector((0, 0, 1120.0))
    build_tube(bm, uv, fork_pos, crown_end, 25.0, 8.0, num_segs=5, sides=8, curl=mathutils.Vector((20.0, 10.0, 30.0)))
    for cr_i in range(4):
        cr_ang = cr_i * (math.pi * 0.5) + 0.3
        cr_tip = crown_end + mathutils.Vector((220.0 * math.cos(cr_ang), 220.0 * math.sin(cr_ang), random.uniform(30.0, 90.0)))
        build_tube(bm, uv, crown_end, cr_tip, 7.0, 2.5, num_segs=2, sides=6)
        foliage_anchors.append((cr_tip, (cr_tip - crown_end).normalized()))
        
    for anchor, b_dir in foliage_anchors:
        for _ in range(random.randint(10, 15)):
            off = mathutils.Vector((random.uniform(-85.0, 85.0), random.uniform(-85.0, 85.0), random.uniform(-55.0, 65.0)))
            cp = anchor + off
            outward = (cp - canopy_center).normalized()
            norm = (outward * 0.6 + b_dir.normalized() * 0.3 + mathutils.Vector((random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), random.uniform(0.2, 0.7)))).normalized()
            add_bowed_card(bm, uv, cp, norm, random.uniform(65.0, 85.0), random.uniform(65.0, 85.0), random.choice(atlas_uvs), mat_idx=1)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - canopy_center).normalized() if v.co.z > 420.0 else v.normal for v in mesh.vertices])
    export_fbx(obj, "SM_Tree_Raintree_Master.fbx")

# ==============================================================================
# MODEL 2: KRISHNACHURA MASTER (All coords in CM!)
# ==============================================================================
def create_krishnachura_master():
    reset()
    mesh = bpy.data.meshes.new("SM_Tree_Krishnachura_Master")
    obj = bpy.data.objects.new("SM_Tree_Krishnachura_Master", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_bark = bpy.data.materials.new("M_Bark_Tree")
    mat_flower = bpy.data.materials.new("MI_Foliage_Krishnachura_Natural")
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_flower)
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    profile = [(0.0, 60.0, 20.0), (40.0, 45.0, 10.0), (120.0, 38.0, 4.0), (220.0, 34.0, 2.0), (320.0, 32.0, 0.0)]
    rings = []
    for z, r, fl in profile:
        rv = []
        lean = mathutils.Vector((math.sin(z * 0.005) * 22.0, math.cos(z * 0.004) * 15.0, z))
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
    bc = bm.verts.new((0, 0, 0))
    for i in range(14):
        f = bm.faces.new([bc, rings[0][(i+1)%14], rings[0][i]])
        f.material_index = 0
        f.smooth = True
        
    fork_pos = mathutils.Vector((math.sin(320.0 * 0.005) * 22.0, math.cos(320.0 * 0.004) * 15.0, 320.0))
    canopy_center = fork_pos + mathutils.Vector((0, 0, 380.0))
    
    boughs = [
        (0.00, 550.0, 620.0, 24.0, 12.0),
        (1.05, 580.0, 650.0, 22.0, 11.0),
        (2.10, 520.0, 600.0, 23.0, 12.0),
        (3.14, 560.0, 640.0, 24.0, 11.0),
        (4.20, 540.0, 610.0, 22.0, 12.0),
        (5.25, 570.0, 630.0, 23.0, 11.0),
    ]
    foliage_anchors = []
    for ang, reach, b_z, r_s, r_e in boughs:
        b_end = mathutils.Vector((reach * math.cos(ang), reach * math.sin(ang), b_z))
        curl = mathutils.Vector((math.cos(ang) * 80.0, math.sin(ang) * 80.0, 40.0))
        build_tube(bm, uv, fork_pos, b_end, r_s, r_e, num_segs=5, sides=8, curl=curl)
        for sub_i in range(3):
            t = 0.5 + sub_i * 0.22
            s_start = fork_pos.lerp(b_end, t) + curl * math.sin(t * math.pi)
            s_ang = ang + random.uniform(-0.5, 0.5)
            s_reach = reach + random.uniform(100.0, 200.0)
            s_end = mathutils.Vector((s_reach * math.cos(s_ang), s_reach * math.sin(s_ang), b_z + random.uniform(-30.0, 60.0)))
            build_tube(bm, uv, s_start, s_end, r_e * 0.8, 5.0, num_segs=3, sides=6)
            foliage_anchors.append((s_end, (s_end - s_start).normalized()))
            for tw_i in range(2):
                tw_ang = s_ang + random.uniform(-0.4, 0.4)
                tw_end = s_end + mathutils.Vector((random.uniform(60.0, 120.0) * math.cos(tw_ang), random.uniform(60.0, 120.0) * math.sin(tw_ang), random.uniform(-20.0, 30.0)))
                build_tube(bm, uv, s_end, tw_end, 4.0, 2.0, num_segs=2, sides=5)
                foliage_anchors.append((tw_end, (tw_end - s_end).normalized()))
                
    for anchor, b_dir in foliage_anchors:
        for _ in range(random.randint(9, 14)):
            off = mathutils.Vector((random.uniform(-75.0, 75.0), random.uniform(-75.0, 75.0), random.uniform(-30.0, 35.0)))
            cp = anchor + off
            norm = (cp - canopy_center).normalized() + mathutils.Vector((0, 0, 0.6))
            add_bowed_card(bm, uv, cp, norm, random.uniform(60.0, 80.0), random.uniform(60.0, 80.0), random.choice(atlas_uvs), mat_idx=1)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - canopy_center).normalized() if v.co.z > 300.0 else v.normal for v in mesh.vertices])
    export_fbx(obj, "SM_Tree_Krishnachura_Master.fbx")

# ==============================================================================
# MODEL 3: BANYAN MASTER (All coords in CM!)
# ==============================================================================
def create_banyan_master():
    reset()
    mesh = bpy.data.meshes.new("SM_Tree_Banyan_Master")
    obj = bpy.data.objects.new("SM_Tree_Banyan_Master", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_bark = bpy.data.materials.new("M_Bark_Tree")
    mat_leaves = bpy.data.materials.new("MI_Foliage_Banyan_Natural")
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaves)
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    profile = [(0.0, 95.0, 30.0), (50.0, 75.0, 18.0), (150.0, 62.0, 10.0), (280.0, 55.0, 5.0), (380.0, 52.0, 0.0)]
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
    bc = bm.verts.new((0, 0, 0))
    for i in range(16):
        f = bm.faces.new([bc, rings[0][(i+1)%16], rings[0][i]])
        f.material_index = 0
        f.smooth = True
        
    prop_root_coords = [(180.0, 40.0), (-160.0, 60.0), (50.0, -170.0), (-80.0, -150.0)]
    fork_pos = mathutils.Vector((0, 0, 380.0))
    for px, py in prop_root_coords:
        top_p = mathutils.Vector((px * 0.7, py * 0.7, 360.0))
        bot_p = mathutils.Vector((px, py, 0.0))
        curl_p = mathutils.Vector((random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0), 0.0))
        build_tube(bm, uv, top_p, bot_p, 14.0, 20.0, num_segs=5, sides=7, curl=curl_p)
        
    canopy_center = mathutils.Vector((0, 0, 750.0))
    boughs = [
        (0.40, 620.0, 780.0, 32.0, 18.0),
        (1.70, 600.0, 750.0, 30.0, 17.0),
        (2.95, 650.0, 800.0, 33.0, 18.0),
        (4.20, 580.0, 740.0, 29.0, 16.0),
        (5.50, 630.0, 790.0, 31.0, 17.0),
    ]
    foliage_anchors = []
    for ang, reach, b_z, r_s, r_e in boughs:
        b_end = mathutils.Vector((reach * math.cos(ang), reach * math.sin(ang), b_z))
        curl = mathutils.Vector((math.cos(ang) * 50.0, math.sin(ang) * 50.0, 70.0))
        build_tube(bm, uv, fork_pos, b_end, r_s, r_e, num_segs=5, sides=9, curl=curl)
        for s_i in range(3):
            t = 0.45 + s_i * 0.24
            s_start = fork_pos.lerp(b_end, t) + curl * math.sin(t * math.pi)
            s_ang = ang + random.uniform(-0.6, 0.6)
            s_reach = reach + random.uniform(100.0, 220.0)
            s_end = mathutils.Vector((s_reach * math.cos(s_ang), s_reach * math.sin(s_ang), b_z + random.uniform(-40.0, 80.0)))
            build_tube(bm, uv, s_start, s_end, r_e * 0.85, 7.0, num_segs=3, sides=6)
            foliage_anchors.append((s_end, (s_end - s_start).normalized()))
            
    for anchor, b_dir in foliage_anchors:
        for _ in range(random.randint(10, 16)):
            off = mathutils.Vector((random.uniform(-80.0, 80.0), random.uniform(-80.0, 80.0), random.uniform(-50.0, 50.0)))
            cp = anchor + off
            norm = (cp - canopy_center).normalized() + mathutils.Vector((0, 0, 0.5))
            add_bowed_card(bm, uv, cp, norm, random.uniform(65.0, 88.0), random.uniform(65.0, 88.0), random.choice(atlas_uvs), mat_idx=1)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - canopy_center).normalized() if v.co.z > 300.0 else v.normal for v in mesh.vertices])
    export_fbx(obj, "SM_Tree_Banyan_Master.fbx")

# ==============================================================================
# MODEL 4: ROYAL PALM MASTER (All coords in CM!)
# ==============================================================================
def create_royal_palm_master():
    reset()
    mesh = bpy.data.meshes.new("SM_Tree_RoyalPalm_Master")
    obj = bpy.data.objects.new("SM_Tree_RoyalPalm_Master", mesh)
    bpy.context.collection.objects.link(obj)
    
    mat_trunk = bpy.data.materials.new("M_Bark_Tree")
    mat_frond = bpy.data.materials.new("MI_Foliage_PalmFrond")
    obj.data.materials.append(mat_trunk)
    obj.data.materials.append(mat_frond)
    
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    palm_profile = [
        (0.0,    34.0),
        (50.0,   38.0),
        (200.0,  27.0),
        (500.0,  25.0),
        (800.0,  28.0),
        (1000.0, 24.0),
        (1120.0, 21.0),
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
    bc = bm.verts.new((0, 0, 0))
    for i in range(12):
        f = bm.faces.new([bc, rings[0][(i+1)%12], rings[0][i]])
        f.material_index = 0
        f.smooth = True
        
    crown_profile = [(1120.0, 21.0), (1180.0, 20.0), (1240.0, 18.0)]
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
            
    crown_top = mathutils.Vector((0, 0, 1240.0))
    num_fronds = 14
    for f_idx in range(num_fronds):
        ang = (2.0 * math.pi * f_idx / num_fronds) + (f_idx * 0.15)
        droop_tier = f_idx % 3
        reach = 360.0 if droop_tier != 0 else 420.0
        droop_z = -120.0 if droop_tier == 2 else (-40.0 if droop_tier == 1 else 40.0)
        
        spine_pts = []
        for s_i in range(5):
            t = s_i / 4.0
            p_reach = reach * t
            p_z = crown_top.z + (120.0 * math.sin(t * math.pi * 0.6) + droop_z * t * t)
            pt = mathutils.Vector((p_reach * math.cos(ang), p_reach * math.sin(ang), p_z))
            spine_pts.append(pt)
            
        uv_frond = ((0.02, 0.52), (0.48, 0.98))
        for s_i in range(len(spine_pts) - 1):
            p0 = spine_pts[s_i]
            p1 = spine_pts[s_i + 1]
            seg_mid = (p0 + p1) * 0.5
            seg_dir = (p1 - p0).normalized()
            seg_norm = mathutils.Vector((0, 0, 1)).cross(seg_dir).cross(seg_dir).normalized()
            add_bowed_card(bm, uv, seg_mid, seg_norm, 110.0 - 15.0 * s_i, (p1 - p0).length * 1.1, uv_frond, mat_idx=1)
            
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - crown_top).normalized() if v.co.z > 1100.0 else v.normal for v in mesh.vertices])
    export_fbx(obj, "SM_Tree_RoyalPalm_Master.fbx")

# ==============================================================================
# MODEL 5: GRASS LAWN MASTER (All coords in CM!)
# ==============================================================================
def create_grass_lawn_master():
    reset()
    mesh = bpy.data.meshes.new("SM_Campus_Grass_Lawn")
    obj = bpy.data.objects.new("SM_Campus_Grass_Lawn", mesh)
    bpy.context.collection.objects.link(obj)
    mat_grass = bpy.data.materials.new("MI_Ground_Grass")
    obj.data.materials.append(mat_grass)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    for i in range(3):
        ang = i * (math.pi / 3.0)
        dir_xy = mathutils.Vector((math.cos(ang), math.sin(ang), 0))
        norm_xy = mathutils.Vector((-math.sin(ang), math.cos(ang), 0))
        w = 44.0
        h = 16.0
        v0 = -dir_xy * (w * 0.5)
        v1 = dir_xy * (w * 0.5)
        v2 = -dir_xy * (w * 0.52) + mathutils.Vector((0, 0, h * 0.5)) + norm_xy * 2.0
        v3 = dir_xy * (w * 0.52) + mathutils.Vector((0, 0, h * 0.5)) - norm_xy * 2.0
        v4 = -dir_xy * (w * 0.45) + mathutils.Vector((0, 0, h)) + norm_xy * 5.0
        v5 = dir_xy * (w * 0.45) + mathutils.Vector((0, 0, h)) - norm_xy * 5.0
        vo = [bm.verts.new(p) for p in [v0, v1, v2, v3, v4, v5]]
        f1 = bm.faces.new([vo[0], vo[1], vo[3], vo[2]])
        f1.smooth = True
        for l in f1.loops:
            if l.vert == vo[0]: l[uv].uv = (0.0, 0.0)
            elif l.vert == vo[1]: l[uv].uv = (1.0, 0.0)
            elif l.vert == vo[3]: l[uv].uv = (1.0, 0.5)
            elif l.vert == vo[2]: l[uv].uv = (0.0, 0.5)
        f2 = bm.faces.new([vo[2], vo[3], vo[5], vo[4]])
        f2.smooth = True
        for l in f2.loops:
            if l.vert == vo[2]: l[uv].uv = (0.0, 0.5)
            elif l.vert == vo[3]: l[uv].uv = (1.0, 0.5)
            elif l.vert == vo[5]: l[uv].uv = (1.0, 1.0)
            elif l.vert == vo[4]: l[uv].uv = (0.0, 1.0)
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([mathutils.Vector((0, 0, 1)) for _ in mesh.vertices])
    export_fbx(obj, "SM_Campus_Grass_Lawn.fbx")

# ==============================================================================
# MODEL 6: GRASS TUFT MASTER (All coords in CM!)
# ==============================================================================
def create_grass_tuft_master():
    reset()
    mesh = bpy.data.meshes.new("SM_Campus_Grass_Tuft")
    obj = bpy.data.objects.new("SM_Campus_Grass_Tuft", mesh)
    bpy.context.collection.objects.link(obj)
    mat_grass = bpy.data.materials.new("MI_Ground_Grass")
    obj.data.materials.append(mat_grass)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    for i in range(4):
        ang = i * (math.pi / 4.0) + random.uniform(-0.1, 0.1)
        dir_xy = mathutils.Vector((math.cos(ang), math.sin(ang), 0))
        norm_xy = mathutils.Vector((-math.sin(ang), math.cos(ang), 0))
        w = 58.0
        h = random.uniform(24.0, 28.0)
        v0 = -dir_xy * (w * 0.5)
        v1 = dir_xy * (w * 0.5)
        v2 = -dir_xy * (w * 0.54) + mathutils.Vector((0, 0, h * 0.5)) + norm_xy * 4.0
        v3 = dir_xy * (w * 0.54) + mathutils.Vector((0, 0, h * 0.5)) - norm_xy * 4.0
        v4 = -dir_xy * (w * 0.40) + mathutils.Vector((0, 0, h)) + norm_xy * 8.0
        v5 = dir_xy * (w * 0.40) + mathutils.Vector((0, 0, h)) - norm_xy * 8.0
        vo = [bm.verts.new(p) for p in [v0, v1, v2, v3, v4, v5]]
        f1 = bm.faces.new([vo[0], vo[1], vo[3], vo[2]])
        f1.smooth = True
        for l in f1.loops:
            if l.vert == vo[0]: l[uv].uv = (0.0, 0.0)
            elif l.vert == vo[1]: l[uv].uv = (1.0, 0.0)
            elif l.vert == vo[3]: l[uv].uv = (1.0, 0.5)
            elif l.vert == vo[2]: l[uv].uv = (0.0, 0.5)
        f2 = bm.faces.new([vo[2], vo[3], vo[5], vo[4]])
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
# MODEL 7: KAMINI BUSH MASTER (All coords in CM!)
# ==============================================================================
def create_kamini_bush_master():
    reset()
    mesh = bpy.data.meshes.new("SM_Campus_Bush_Kamini")
    obj = bpy.data.objects.new("SM_Campus_Bush_Kamini", mesh)
    bpy.context.collection.objects.link(obj)
    mat_shrub = bpy.data.materials.new("MI_Foliage_Fern_Natural")
    obj.data.materials.append(mat_shrub)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    
    uv_box = ((0.02, 0.52), (0.48, 0.98))
    center = mathutils.Vector((0, 0, 60.0))
    for i in range(24):
        ang = (2.0 * math.pi * i / 24) * 2.39996
        rad = 35.0 + 45.0 * math.sqrt(i / 24.0)
        z = 20.0 + 90.0 * (1.0 - (rad / 80.0)**2) * 0.7
        pos = mathutils.Vector((rad * math.cos(ang), rad * math.sin(ang), z))
        norm = (pos - center).normalized() + mathutils.Vector((0, 0, 0.4))
        add_bowed_card(bm, uv, pos, norm, 55.0, 55.0, uv_box, mat_idx=0)
    bm.to_mesh(mesh)
    bm.free()
    mesh.normals_split_custom_set_from_vertices([(v.co - center).normalized() for v in mesh.vertices])
    export_fbx(obj, "SM_Campus_Bush_Kamini.fbx")

print("Generating all authentic vegetation models in Unreal Centimeters...")
create_raintree_master()
create_krishnachura_master()
create_banyan_master()
create_royal_palm_master()
create_grass_lawn_master()
create_grass_tuft_master()
create_kamini_bush_master()
print("All vegetation models successfully generated in Centimeters!")
"""

script_path = "/tmp/generate_all_vegetation_cm.py"
with open(script_path, "w") as f:
    f.write(BLENDER_BATCH_CODE)

print("Running Blender batch generation in Centimeters...")
res = subprocess.run([BLENDER_BIN, "--background", "--python", script_path], capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print("Blender ERROR:", res.stderr)
    sys.exit(1)

print("\n✓ Full vegetation library in Unreal Centimeters generated successfully!")
