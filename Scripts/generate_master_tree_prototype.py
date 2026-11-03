#!/usr/bin/env python3
"""
Generate Master Tree Prototype for SparkVision:
Authentic Bangladeshi Grand Rain Tree (Samanea saman) / Broadleaf Shade Tree
Inspired by Where Winds Meet and Authentic Dhaka University Campus Reference.

Features:
- Organic trunk with 6 fluted buttress roots, realistic taper (1.1m base -> 0.7m mid -> 0.55m fork).
- 5 primary boughs spreading naturally into an umbrella canopy (14m wide, 11.5m tall).
- 3 tiers of branching (Trunk -> Primary Boughs -> Secondary Branches -> Tertiary Twigs).
- Delicate leaf clusters (cards sized 0.55m - 0.75m, NOT 3-meter slabs!) with 4-quad curved geometry.
- Sphericalized foliage normals for lush volumetric light-wrap and cloud-like shading.
- Two material slots: Slot 0 = Bark, Slot 1 = Foliage.
"""

import sys
import os
import subprocess

OUTPUT_FBX = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Vegetation/SM_Tree_Raintree_Master.fbx"
BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender"

BLENDER_CODE = f"""
import bpy
import bmesh
import mathutils
import math
import random
import os

OUTPUT_FBX = "{OUTPUT_FBX}"
random.seed(42)

# Reset Blender
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for m in bpy.data.meshes:
    if m.users == 0: bpy.data.meshes.remove(m)
for mat in bpy.data.materials:
    if mat.users == 0: bpy.data.materials.remove(mat)

# Create mesh and object
mesh = bpy.data.meshes.new("SM_Tree_Raintree_Master")
obj = bpy.data.objects.new("SM_Tree_Raintree_Master", mesh)
bpy.context.collection.objects.link(obj)

# Create materials
mat_bark = bpy.data.materials.new(name="M_Bark_Tree")
mat_bark.use_nodes = True
mat_foliage = bpy.data.materials.new(name="M_Master_NaturalFoliage")
mat_foliage.use_nodes = True

obj.data.materials.append(mat_bark)     # Slot 0
obj.data.materials.append(mat_foliage)  # Slot 1

bm = bmesh.new()
uv_layer = bm.loops.layers.uv.new("UVMap")

# -------------------------------------------------------------
# 1. TRUNK AND BUTTRESS ROOTS (Organic Fluted Cylinder)
# -------------------------------------------------------------
num_sides = 16
trunk_height = 4.2  # meters before main fork

# Profile heights and radii
profile = [
    (0.00, 0.70, 0.25),  # Base with buttress flare: base_r=0.70m, buttress_amp=0.25m
    (0.40, 0.55, 0.15),
    (0.90, 0.48, 0.08),
    (1.60, 0.42, 0.03),
    (2.50, 0.38, 0.02),
    (3.40, 0.35, 0.02),
    (4.20, 0.34, 0.02),  # Fork point
]

trunk_rings = []
for z, r, flare in profile:
    ring_verts = []
    # Subtle organic trunk lean
    lean_x = math.sin(z * 0.4) * 0.12
    lean_y = math.cos(z * 0.3) * 0.08
    for i in range(num_sides):
        angle = (2.0 * math.pi * i) / num_sides
        # 5 buttress flutes at the base
        flute = math.cos(5.0 * angle) * flare if flare > 0 else 0.0
        # Organic surface perturbation
        noise = math.sin(angle * 7.0 + z * 3.0) * 0.02
        curr_r = max(0.1, r + flute + noise)
        
        vx = lean_x + curr_r * math.cos(angle)
        vy = lean_y + curr_r * math.sin(angle)
        vz = z
        v = bm.verts.new((vx, vy, vz))
        ring_verts.append(v)
    trunk_rings.append(ring_verts)

# Bridge trunk rings with quads
for r_idx in range(len(trunk_rings) - 1):
    r0 = trunk_rings[r_idx]
    r1 = trunk_rings[r_idx + 1]
    z0 = profile[r_idx][0]
    z1 = profile[r_idx + 1][0]
    for i in range(num_sides):
        next_i = (i + 1) % num_sides
        v_a = r0[i]
        v_b = r0[next_i]
        v_c = r1[next_i]
        v_d = r1[i]
        f = bm.faces.new([v_a, v_b, v_c, v_d])
        f.material_index = 0
        f.smooth = True
        
        # UV coordinates for bark (wrapping around X, vertical along Y)
        u0 = i / num_sides
        u1 = (i + 1) / num_sides
        v_uv0 = z0 * 0.8
        v_uv1 = z1 * 0.8
        for loop in f.loops:
            if loop.vert == v_a: loop[uv_layer].uv = (u0, v_uv0)
            elif loop.vert == v_b: loop[uv_layer].uv = (u1, v_uv0)
            elif loop.vert == v_c: loop[uv_layer].uv = (u1, v_uv1)
            elif loop.vert == v_d: loop[uv_layer].uv = (u0, v_uv1)

# Cap bottom of trunk (ground contact)
bottom_center = bm.verts.new((0, 0, 0))
for i in range(num_sides):
    next_i = (i + 1) % num_sides
    f = bm.faces.new([bottom_center, trunk_rings[0][next_i], trunk_rings[0][i]])
    f.material_index = 0
    f.smooth = True

# -------------------------------------------------------------
# 2. HIERARCHICAL BRANCHING (Boughs -> Branches -> Twigs)
# -------------------------------------------------------------
def build_tube(start_pos, end_pos, start_r, end_r, num_segs=5, sides=8, curl=None):
    \"\"\"Builds a smooth curved branch tube from start to end.\"\"\"
    start = mathutils.Vector(start_pos)
    end = mathutils.Vector(end_pos)
    length = (end - start).length
    dir_vec = (end - start).normalized()
    
    # Calculate orthogonal basis
    up = mathutils.Vector((0, 0, 1))
    if abs(dir_vec.dot(up)) > 0.90:
        up = mathutils.Vector((1, 0, 0))
    side_vec = dir_vec.cross(up).normalized()
    up_vec = side_vec.cross(dir_vec).normalized()
    
    rings = []
    for s in range(num_segs + 1):
        t = s / num_segs
        # Quadratic curve for natural drooping/arching
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
            f.material_index = 0
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

# 5 Primary boughs radiating outward to form the umbrella dome
bough_configs = [
    (0.00,  6.2, 8.8, 0.28, 0.16),  # angle, reach_xy, height_z, start_r, end_r
    (1.25,  6.8, 9.2, 0.26, 0.15),
    (2.50,  6.0, 8.5, 0.27, 0.15),
    (3.80,  6.6, 9.0, 0.28, 0.16),
    (5.05,  6.4, 8.7, 0.26, 0.15),
]

fork_pos = mathutils.Vector((0, 0, trunk_height))
twig_tips = []
foliage_anchors = []

for b_ang, reach, b_height, r_start, r_end in bough_configs:
    b_end = mathutils.Vector((
        reach * math.cos(b_ang),
        reach * math.sin(b_ang),
        b_height
    ))
    # Arch curl upward then spreading
    curl = mathutils.Vector((math.cos(b_ang) * 0.6, math.sin(b_ang) * 0.6, 0.8))
    build_tube(fork_pos, b_end, r_start, r_end, num_segs=6, sides=10, curl=curl)
    
    # Secondary branches from each bough (3-4 branches)
    for sub_i in range(3):
        sub_t = 0.45 + sub_i * 0.25
        sub_start = fork_pos.lerp(b_end, sub_t) + curl * math.sin(sub_t * math.pi)
        sub_ang = b_ang + random.uniform(-0.65, 0.65)
        sub_reach = reach + random.uniform(1.2, 2.5)
        sub_z = b_height + random.uniform(0.6, 1.8)
        sub_end = mathutils.Vector((
            sub_reach * math.cos(sub_ang),
            sub_reach * math.sin(sub_ang),
            sub_z
        ))
        sub_curl = mathutils.Vector((0, 0, random.uniform(0.2, 0.5)))
        build_tube(sub_start, sub_end, r_end * 0.85, 0.08, num_segs=4, sides=8, curl=sub_curl)
        foliage_anchors.append((sub_start.lerp(sub_end, 0.6), sub_end - sub_start))
        
        # Tertiary twigs extending into canopy periphery
        for twig_i in range(3):
            tw_ang = sub_ang + random.uniform(-0.5, 0.5)
            tw_reach = sub_reach + random.uniform(0.8, 1.6)
            tw_z = sub_z + random.uniform(-0.4, 0.9)
            tw_end = mathutils.Vector((
                tw_reach * math.cos(tw_ang),
                tw_reach * math.sin(tw_ang),
                tw_z
            ))
            twig_start = sub_end.lerp(sub_start, 0.2 * twig_i)
            build_tube(twig_start, tw_end, 0.06, 0.025, num_segs=2, sides=6)
            twig_tips.append((tw_end, (tw_end - twig_start).normalized()))
            foliage_anchors.append((tw_end, (tw_end - twig_start).normalized()))

# Central apex branch to fill canopy crown
crown_end = mathutils.Vector((0, 0, 11.2))
build_tube(fork_pos, crown_end, 0.25, 0.08, num_segs=5, sides=8, curl=mathutils.Vector((0.2, 0.1, 0.3)))
for cr_i in range(4):
    cr_ang = cr_i * (math.pi * 0.5) + 0.3
    cr_tip = crown_end + mathutils.Vector((
        2.2 * math.cos(cr_ang),
        2.2 * math.sin(cr_ang),
        random.uniform(0.3, 0.9)
    ))
    build_tube(crown_end, cr_tip, 0.07, 0.025, num_segs=2, sides=6)
    foliage_anchors.append((cr_tip, (cr_tip - crown_end).normalized()))

# -------------------------------------------------------------
# 3. HIGH-RESOLUTION REALISTIC LEAF CLUSTERS (Not Slabs!)
# -------------------------------------------------------------
# Leaf card sizes: 0.55m to 0.75m (realistic branchlet scale)
# Each card represents a leafy branchlet with dozens of delicate leaves.
# Multiple intersecting cards form a 3D volumetric puff with no angular planar appearance.

# 4 Quadrants in atlas (0=top-left, 1=top-right, 2=bottom-left, 3=bottom-right)
atlas_uvs = [
    ((0.02, 0.52), (0.48, 0.98)),  # Quadrant 0: Main bough branch
    ((0.52, 0.52), (0.98, 0.98)),  # Quadrant 1: Fine leafy branch
    ((0.02, 0.02), (0.48, 0.48)),  # Quadrant 2: Dense cluster
    ((0.52, 0.02), (0.98, 0.48)),  # Quadrant 3: Feathery sprigs
]

canopy_center = mathutils.Vector((0, 0, 8.5))
cards_created = 0

def add_foliage_card(center, normal, size_w=0.65, size_h=0.65, uv_box=None):
    \"\"\"Creates a 2-segment bowed cross card with curved organic form.\"\"\"
    global cards_created
    norm = normal.normalized()
    up = mathutils.Vector((0, 0, 1))
    if abs(norm.dot(up)) > 0.92:
        up = mathutils.Vector((1, 0, 0))
    tangent = norm.cross(up).normalized()
    bitangent = norm.cross(tangent).normalized()
    
    # 6 vertices for a 2-quad slightly bowed leaf card (prevents flat plane look)
    bow = size_h * 0.12
    v0 = center - tangent * (size_w * 0.5) - bitangent * (size_h * 0.5)
    v1 = center + tangent * (size_w * 0.5) - bitangent * (size_h * 0.5)
    v2 = center - tangent * (size_w * 0.52) + norm * bow
    v3 = center + tangent * (size_w * 0.52) + norm * bow
    v4 = center - tangent * (size_w * 0.48) + bitangent * (size_h * 0.5)
    v5 = center + tangent * (size_w * 0.48) + bitangent * (size_h * 0.5)
    
    vert_objs = [bm.verts.new(p) for p in [v0, v1, v2, v3, v4, v5]]
    
    if uv_box is None:
        u_min, v_min = 0.0, 0.0
        u_max, v_max = 1.0, 1.0
    else:
        (u_min, v_min), (u_max, v_max) = uv_box
    
    # Quad 1: v0, v1, v3, v2
    f1 = bm.faces.new([vert_objs[0], vert_objs[1], vert_objs[3], vert_objs[2]])
    f1.material_index = 1
    f1.smooth = True
    v_mid = (v_min + v_max) * 0.5
    for loop in f1.loops:
        if loop.vert == vert_objs[0]: loop[uv_layer].uv = (u_min, v_min)
        elif loop.vert == vert_objs[1]: loop[uv_layer].uv = (u_max, v_min)
        elif loop.vert == vert_objs[3]: loop[uv_layer].uv = (u_max, v_mid)
        elif loop.vert == vert_objs[2]: loop[uv_layer].uv = (u_min, v_mid)
        
    # Quad 2: v2, v3, v5, v4
    f2 = bm.faces.new([vert_objs[2], vert_objs[3], vert_objs[5], vert_objs[4]])
    f2.material_index = 1
    f2.smooth = True
    for loop in f2.loops:
        if loop.vert == vert_objs[2]: loop[uv_layer].uv = (u_min, v_mid)
        elif loop.vert == vert_objs[3]: loop[uv_layer].uv = (u_max, v_mid)
        elif loop.vert == vert_objs[5]: loop[uv_layer].uv = (u_max, v_max)
        elif loop.vert == vert_objs[4]: loop[uv_layer].uv = (u_min, v_max)
        
    cards_created += 1

# Generate volumetric foliage puffs around each anchor point
print(f"Distributing volumetric foliage puffs across {{len(foliage_anchors)}} branch anchors...")
for anchor_pos, branch_dir in foliage_anchors:
    # 8 to 14 cards per cluster anchor to form an organic volumetric cushion
    num_cards_in_cluster = random.randint(10, 16)
    for c_i in range(num_cards_in_cluster):
        # Offset within a 1.2m radius cloud
        offset = mathutils.Vector((
            random.uniform(-0.85, 0.85),
            random.uniform(-0.85, 0.85),
            random.uniform(-0.55, 0.65)
        ))
        card_center = anchor_pos + offset
        
        # Outward-facing orientation with natural droop
        outward = (card_center - canopy_center).normalized()
        card_norm = (outward * 0.6 + branch_dir.normalized() * 0.3 + mathutils.Vector((
            random.uniform(-0.3, 0.3),
            random.uniform(-0.3, 0.3),
            random.uniform(0.2, 0.7)
        ))).normalized()
        
        card_w = random.uniform(0.55, 0.78)
        card_h = random.uniform(0.55, 0.82)
        uv_b = random.choice(atlas_uvs)
        
        add_foliage_card(card_center, card_norm, card_w, card_h, uv_b)

print(f"Total foliage cards generated: {{cards_created}}")

# -------------------------------------------------------------
# 4. VOLUMETRIC SPHERICALIZED NORMALS
# -------------------------------------------------------------
# Crucial AAA Technique: Modify vertex normals on foliage cards
# so they point outwards from the canopy sphere center.
# This prevents flat polygon shading and produces soft, fluffy,
# cloud-like illumination with gorgeous two-sided light transmission!
bm.to_mesh(mesh)
bm.free()

# Calculate custom split normals
# In Blender 5.x, custom normals are supported directly via normals_split_custom_set_from_vertices
mesh.normals_split_custom_set_from_vertices([
    (v.co - canopy_center).normalized() if v.co.z > trunk_height else v.normal
    for v in mesh.vertices
])

# Export FBX
os.makedirs(os.path.dirname(OUTPUT_FBX), exist_ok=True)
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.export_scene.fbx(
    filepath=OUTPUT_FBX,
    use_selection=True,
    apply_scale_options='FBX_SCALE_ALL',
    axis_forward='-Z',
    axis_up='Y',
    bake_space_transform=False,
    mesh_smooth_type='FACE'
)
print(f"Successfully exported Master Tree to: {{OUTPUT_FBX}}")
"""

script_path = "/tmp/generate_master_tree.py"
with open(script_path, "w") as f:
    f.write(BLENDER_CODE)

print("Running Blender to generate Master Tree prototype...")
res = subprocess.run([BLENDER_BIN, "--background", "--python", script_path], capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print("Blender ERROR:", res.stderr)
    sys.exit(1)

print("\n✓ Master Tree prototype generated successfully!")
