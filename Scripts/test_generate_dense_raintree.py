import sys
import os
import subprocess

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Vegetation"
BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender"

BLENDER_CODE = """
import bpy
import bmesh
import mathutils
import math
import random
import os

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Vegetation"
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
    print(f"Exported {filename} ({len(obj.data.polygons)} polys, {len(obj.data.vertices)} verts)")

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
            v0 = s / num_segs * 4.0
            v1 = (s + 1) / num_segs * 4.0
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

full_leaf_uvs = [
    ((0.02, 0.02), (0.98, 0.98)),
    ((0.98, 0.02), (0.02, 0.98)),
]

def create_raintree():
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
    
    # 1. Authentic Fluted Trunk (Centimeters)
    profile = [
        (0.0,   75.0, 32.0),
        (35.0,  58.0, 20.0),
        (80.0,  48.0, 12.0),
        (150.0, 42.0, 5.0),
        (230.0, 38.0, 2.0),
        (310.0, 36.0, 1.0),
        (380.0, 35.0, 0.0),
    ]
    rings = []
    for z, r, flare in profile:
        rv = []
        lean_x = math.sin(z * 0.004) * 10.0
        lean_y = math.cos(z * 0.003) * 6.0
        for i in range(16):
            ang = (2.0 * math.pi * i) / 16
            flute = math.cos(5.0 * ang) * flare if flare > 0 else 0.0
            noise = math.sin(ang * 7.0 + z * 0.03) * 2.0
            curr_r = max(12.0, r + flute + noise)
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
        
    fork_pos = mathutils.Vector((0, 0, 380.0))
    canopy_center = mathutils.Vector((0, 0, 750.0))
    
    # 2. Main Spreading Boughs
    boughs = [
        (0.00,  780.0, 720.0, 28.0, 14.0),
        (1.25,  840.0, 760.0, 26.0, 14.0),
        (2.50,  760.0, 710.0, 27.0, 13.0),
        (3.80,  820.0, 750.0, 28.0, 14.0),
        (5.05,  800.0, 730.0, 26.0, 13.0),
    ]
    
    foliage_anchors = []
    
    for b_ang, reach, b_h, r_s, r_e in boughs:
        b_end = mathutils.Vector((reach * math.cos(b_ang), reach * math.sin(b_ang), b_h))
        curl = mathutils.Vector((math.cos(b_ang) * 40.0, math.sin(b_ang) * 40.0, 60.0))
        build_tube(bm, uv, fork_pos, b_end, r_s, r_e, num_segs=6, sides=10, curl=curl)
        
        for t_b in [0.45, 0.70]:
            p_mid = fork_pos.lerp(b_end, t_b) + curl * math.sin(t_b * math.pi)
            foliage_anchors.append((p_mid, (b_end - fork_pos).normalized(), 12))
        
        for s_i in range(3):
            t = 0.50 + s_i * 0.22
            s_start = fork_pos.lerp(b_end, t) + curl * math.sin(t * math.pi)
            s_ang = b_ang + (-0.55 + s_i * 0.55) + random.uniform(-0.15, 0.15)
            s_reach = reach + random.uniform(140.0, 260.0)
            s_z = b_h + random.uniform(-40.0, 80.0)
            s_end = mathutils.Vector((s_reach * math.cos(s_ang), s_reach * math.sin(s_ang), s_z))
            s_curl = mathutils.Vector((0, 0, -25.0 if s_reach > 850.0 else 30.0))
            build_tube(bm, uv, s_start, s_end, r_e * 0.85, 6.0, num_segs=4, sides=7, curl=s_curl)
            
            foliage_anchors.append((s_start.lerp(s_end, 0.5), (s_end - s_start).normalized(), 14))
            foliage_anchors.append((s_end, (s_end - s_start).normalized(), 16))
            
            for tw_i in range(2):
                tw_ang = s_ang + random.uniform(-0.5, 0.5)
                tw_reach = s_reach + random.uniform(80.0, 160.0)
                tw_z = s_z + random.uniform(-50.0, 40.0)
                tw_end = mathutils.Vector((tw_reach * math.cos(tw_ang), tw_reach * math.sin(tw_ang), tw_z))
                build_tube(bm, uv, s_end, tw_end, 4.5, 2.0, num_segs=2, sides=5)
                foliage_anchors.append((tw_end, (tw_end - s_end).normalized(), 14))

    # 3. Intermediate Lower Drooping Boughs (fills 4m to 6.5m)
    lower_boughs = [
        (0.60, 520.0, 500.0, 20.0, 8.0),
        (1.90, 540.0, 520.0, 20.0, 8.0),
        (3.15, 510.0, 490.0, 19.0, 7.5),
        (4.45, 530.0, 510.0, 20.0, 8.0),
    ]
    for lb_ang, reach, lb_h, r_s, r_e in lower_boughs:
        lb_start = mathutils.Vector((0, 0, 360.0))
        lb_end = mathutils.Vector((reach * math.cos(lb_ang), reach * math.sin(lb_ang), lb_h))
        lb_curl = mathutils.Vector((math.cos(lb_ang) * 30.0, math.sin(lb_ang) * 30.0, -40.0))
        build_tube(bm, uv, lb_start, lb_end, r_s, r_e, num_segs=4, sides=7, curl=lb_curl)
        foliage_anchors.append((lb_start.lerp(lb_end, 0.55), (lb_end - lb_start).normalized(), 15))
        foliage_anchors.append((lb_end, (lb_end - lb_start).normalized(), 18))
        for d_i in range(2):
            d_ang = lb_ang + random.uniform(-0.4, 0.4)
            d_end = lb_end + mathutils.Vector((random.uniform(90.0, 160.0)*math.cos(d_ang), random.uniform(90.0, 160.0)*math.sin(d_ang), random.uniform(-60.0, 10.0)))
            build_tube(bm, uv, lb_end, d_end, 5.0, 2.0, num_segs=2, sides=5)
            foliage_anchors.append((d_end, (d_end - lb_end).normalized(), 15))
                
    # 4. Central Domed Crown
    crown_top = mathutils.Vector((0, 0, 1050.0))
    build_tube(bm, uv, fork_pos, crown_top, 24.0, 9.0, num_segs=5, sides=8, curl=mathutils.Vector((15.0, 10.0, 20.0)))
    for cr_i in range(5):
        cr_ang = cr_i * (2.0 * math.pi / 5.0) + 0.2
        cr_reach = random.uniform(280.0, 420.0)
        cr_z = 1050.0 + random.uniform(60.0, 180.0)
        cr_tip = mathutils.Vector((cr_reach * math.cos(cr_ang), cr_reach * math.sin(cr_ang), cr_z))
        build_tube(bm, uv, crown_top, cr_tip, 8.0, 2.5, num_segs=3, sides=6)
        foliage_anchors.append((crown_top.lerp(cr_tip, 0.5), (cr_tip - crown_top).normalized(), 12))
        foliage_anchors.append((cr_tip, (cr_tip - crown_top).normalized(), 16))

    # 5. Generate Lush Layered Foliage Cards
    print(f"Total foliage anchor clusters: {len(foliage_anchors)}")
    total_cards = 0
    for anchor, b_dir, count in foliage_anchors:
        for _ in range(count):
            off = mathutils.Vector((
                random.uniform(-75.0, 75.0),
                random.uniform(-75.0, 75.0),
                random.uniform(-45.0, 45.0)
            ))
            cp = anchor + off
            outward = (cp - canopy_center).normalized()
            norm = (outward * 0.65 + b_dir.normalized() * 0.25 + mathutils.Vector((random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(0.1, 0.5)))).normalized()
            card_w = random.uniform(85.0, 110.0)
            card_h = random.uniform(85.0, 115.0)
            add_bowed_card(bm, uv, cp, norm, card_w, card_h, random.choice(full_leaf_uvs), mat_idx=1)
            total_cards += 1
            
    print(f"Generated {total_cards} foliage cards!")
    bm.to_mesh(mesh)
    bm.free()
    
    mesh.normals_split_custom_set_from_vertices([
        (v.co - canopy_center).normalized() if v.co.z > 360.0 else v.normal
        for v in mesh.vertices
    ])
    export_fbx(obj, "SM_Tree_Raintree_Master.fbx")

create_raintree()
"""

script_path = "/tmp/test_dense_raintree.py"
with open(script_path, "w") as f:
    f.write(BLENDER_CODE)

res = subprocess.run([BLENDER_BIN, "--background", "--python", script_path], capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print("Blender Error:", res.stderr)
    sys.exit(1)
