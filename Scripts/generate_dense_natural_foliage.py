#!/usr/bin/env python3
"""
High-Density Super-Natural Foliage & Canopy Generator for Blender 5.2.3 LTS
Upgrades tree models and leaf cards to match Reference Images 1, 2, and 3:
1. Rich, multi-tiered compound leaf branch textures (dense pinnate leaflets, deep emerald gradients).
2. Volumetric canopy architecture: 450-650 leaf cards per tree distributed across inner core, mid-tier, and outer crown.
3. Natural branching skeleton: organic curved boughs, secondary twigs, and fine branch tips.
4. Tiled bark UVs for crisp high-resolution wood grain.
5. Sphericalized canopy normals for lush volumetric PBR lighting.
"""

import os
import sys
import math
import random
import numpy as np

# Output directories
TEXTURE_DIR = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_NaturalFoliage"
MODEL_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/NaturalFoliage"
os.makedirs(TEXTURE_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# ==============================================================================
# PART 1: ULTRA-DENSE HIGH-FIDELITY PBR TEXTURES
# ==============================================================================
def generate_enhanced_textures():
    import bpy
    res = 1024
    print("Synthesizing Enhanced High-Density Leaf Textures...")

    u = np.linspace(0.0, 1.0, res, endpoint=False)
    v = np.linspace(0.0, 1.0, res, endpoint=False)
    gx, gy = np.meshgrid(u, v)

    def save_rgba(name, rgba):
        path = os.path.join(TEXTURE_DIR, f"{name}.png")
        img = bpy.data.images.new(name, width=res, height=res, alpha=True, float_buffer=False)
        img.pixels.foreach_set(np.flipud(rgba).ravel())
        img.filepath_raw = path
        img.file_format = 'PNG'
        img.save()
        print(f"  ✓ Updated {name}.png ({os.path.getsize(path)/1024.0:.1f} KB)")

    def calc_normal(h, strength=4.5):
        dzdx = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) * strength
        dzdy = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) * strength
        nz = np.ones((res, res), dtype=np.float32)
        inv = 1.0 / np.sqrt(dzdx**2 + dzdy**2 + nz**2 + 1e-6)
        return np.clip(np.stack([(-dzdx*inv)*0.5+0.5, (-dzdy*inv)*0.5+0.5, (nz*inv)*0.5+0.5, np.ones((res,res))], axis=-1), 0.0, 1.0).astype(np.float32)

    # 1. Raintree Compound Leaf Card (Ref 3: Rain Tree / Gulmohar / Acacia)
    # Dense multi-branching compound frond with 24 pairs of overlapping leaflets
    mask = np.zeros((res, res), dtype=np.float32)
    height = np.zeros((res, res), dtype=np.float32)
    col_r = np.zeros((res, res), dtype=np.float32)
    col_g = np.zeros((res, res), dtype=np.float32)
    col_b = np.zeros((res, res), dtype=np.float32)

    # Main central woody twig
    stem_x = 0.50 + 0.03 * np.sin(gy * 4.0)
    stem_w = 0.012 * (gy * 0.8 + 0.2)
    is_stem = (np.abs(gx - stem_x) < stem_w) & (gy >= 0.08) & (gy <= 0.95)

    np.random.seed(42)
    num_pairs = 20
    for p in range(num_pairs):
        t = p / float(num_pairs - 1)
        py = 0.14 + t * 0.76
        # Leaf length arches: longest in the middle
        p_len = 0.24 * np.sin(t * np.pi * 0.85 + 0.2)
        p_w = 0.052

        for side in [-1.0, 1.0]:
            p_ang = side * (0.42 + 0.20 * (1.0 - t))
            px = stem_x[int(py * res), int(0.5 * res)]
            dx = gx - px
            dy = gy - py
            lx = (dx * np.cos(p_ang) + dy * np.sin(p_ang)) * side
            ly = -dx * np.sin(p_ang) + dy * np.cos(p_ang)

            in_l = (lx >= 0.0) & (lx <= p_len) & ((ly / p_w)**2 <= (1.0 - (lx / p_len - 0.45)**2 * 3.2))
            if np.any(in_l):
                d_c = np.clip(1.0 - np.sqrt((lx/p_len - 0.45)**2 * 3.0 + (ly/p_w)**2), 0.0, 1.0)
                mask[in_l] = 1.0
                height[in_l] = np.maximum(height[in_l], d_c[in_l] * 0.85)

                # Vibrant Natural Foliage: Rich Forest Green with Lime Sunlit Highlights (Ref 1 & 3)
                leaf_t = (1.0 - py) # Higher leaves on twig are fresher/lighter
                base_g = 0.48 + leaf_t * 0.18 + np.random.uniform(-0.03, 0.04)
                base_r = 0.14 + leaf_t * 0.14 + np.random.uniform(-0.02, 0.02)
                base_b = 0.07 + leaf_t * 0.04

                col_r[in_l] = base_r
                col_g[in_l] = base_g
                col_b[in_l] = base_b

    # Add stem
    mask[is_stem] = 1.0
    height[is_stem] = 0.75
    col_r[is_stem] = 0.26
    col_g[is_stem] = 0.22
    col_b[is_stem] = 0.14

    save_rgba("T_Leaf_Raintree_D", np.stack([col_r, col_g, col_b, mask], axis=-1).astype(np.float32))
    save_rgba("T_Leaf_Raintree_N", calc_normal(height, strength=4.5))

# ==============================================================================
# PART 2: DENSE NATURAL 3D CANOPY GENERATION (Blender)
# ==============================================================================
def generate_dense_trees():
    import bpy
    import bmesh
    import mathutils

    def reset():
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        for b in bpy.data.meshes:
            if b.users == 0: bpy.data.meshes.remove(b)

    def get_mat(name, color, roughness=0.7):
        mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = roughness
        return mat

    def export(obj, filename):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        path = os.path.join(MODEL_DIR, filename)
        bpy.ops.export_scene.fbx(
            filepath=path,
            use_selection=True,
            global_scale=1.0,
            apply_unit_scale=True,
            bake_space_transform=True,
            object_types={'MESH'},
            mesh_smooth_type='FACE'
        )
        print(f"  ✓ Exported: {filename} ({os.path.getsize(path)/1024.0:.1f} KB)")

    def add_curved_leaf_quad(bm, uv_layer, center, size, norm_dir, canopy_c, mat_idx=1):
        w, h = size
        norm = norm_dir.normalized()
        up = mathutils.Vector((0, 0, 1))
        if abs(norm.dot(up)) > 0.92:
            up = mathutils.Vector((1, 0, 0))
        tang = norm.cross(up).normalized()
        bitang = norm.cross(tang).normalized()

        # Bowed quad (2 segments)
        v_bl = center - tang*(w*0.5) - bitang*(h*0.5)
        v_br = center + tang*(w*0.5) - bitang*(h*0.5)
        v_ml = center - tang*(w*0.55) + norm*(h*0.14)
        v_mr = center + tang*(w*0.55) + norm*(h*0.14)
        v_tl = center - tang*(w*0.45) + bitang*(h*0.5)
        v_tr = center + tang*(w*0.45) + bitang*(h*0.5)

        v1 = bm.verts.new(v_bl)
        v2 = bm.verts.new(v_br)
        v3 = bm.verts.new(v_mr)
        v4 = bm.verts.new(v_ml)
        v5 = bm.verts.new(v_tl)
        v6 = bm.verts.new(v_tr)

        f1 = bm.faces.new([v1, v2, v3, v4])
        f1.material_index = mat_idx
        f2 = bm.faces.new([v4, v3, v6, v5])
        f2.material_index = mat_idx

        for l in f1.loops:
            if l.vert == v1: l[uv_layer].uv = (0.0, 0.0)
            elif l.vert == v2: l[uv_layer].uv = (1.0, 0.0)
            elif l.vert == v3: l[uv_layer].uv = (1.0, 0.5)
            elif l.vert == v4: l[uv_layer].uv = (0.0, 0.5)

        for l in f2.loops:
            if l.vert == v4: l[uv_layer].uv = (0.0, 0.5)
            elif l.vert == v3: l[uv_layer].uv = (1.0, 0.5)
            elif l.vert == v6: l[uv_layer].uv = (1.0, 1.0)
            elif l.vert == v5: l[uv_layer].uv = (0.0, 1.0)

    # -------------------------------------------------------------
    # 1. SM_Natural_Raintree_Grand (Ref 3: Vast Umbrella Canopy)
    # -------------------------------------------------------------
    print("\nBuilding High-Density SM_Natural_Raintree_Grand...")
    reset()
    random.seed(101)

    mat_bark = get_mat("M_Bark_Natural_Gnarled", (0.24, 0.18, 0.12, 1.0), roughness=0.85)
    mat_leaf = get_mat("M_Foliage_Natural_Leaf", (0.18, 0.48, 0.10, 1.0), roughness=0.45)

    mesh = bpy.data.meshes.new("SM_Natural_Raintree_Grand")
    obj = bpy.data.objects.new("SM_Natural_Raintree_Grand", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0
    obj.data.materials.append(mat_leaf) # Slot 1

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # Trunk: Fluted buttressed base, height 10m, forks at 8m
    num_rings = 10
    segments = 16
    trunk_rings = []
    for r in range(num_rings):
        t = r / float(num_rings - 1)
        z = t * 10.0
        rad = 2.4 * (1.0 - t * 0.55) + 0.4 * (1.0 - t)**3
        ox = 0.3 * math.sin(t * 2.5)
        oy = 0.2 * math.cos(t * 2.0)

        ring = []
        for s in range(segments):
            ang = s * (2.0 * math.pi / segments)
            flute = 0.4 * math.cos(ang * 4.0) * (1.0 - t)**2 if t < 0.35 else 0.0
            x = (rad + flute) * math.cos(ang) + ox
            y = (rad + flute) * math.sin(ang) + oy
            ring.append(bm.verts.new(mathutils.Vector((x, y, z))))
        trunk_rings.append(ring)

    for r in range(num_rings - 1):
        for s in range(segments):
            sn = (s + 1) % segments
            f = bm.faces.new([trunk_rings[r][s], trunk_rings[r][sn], trunk_rings[r+1][sn], trunk_rings[r+1][s]])
            f.material_index = 0
            u0 = (s / float(segments)) * 3.0 # Repeat bark horizontally 3x
            u1 = ((s + 1) / float(segments)) * 3.0
            v0 = (r / float(num_rings)) * 6.0 # Repeat vertically 6x
            v1 = ((r + 1) / float(num_rings)) * 6.0
            for l in f.loops:
                if l.vert == trunk_rings[r][s]: l[uv_layer].uv = (u0, v0)
                elif l.vert == trunk_rings[r][sn]: l[uv_layer].uv = (u1, v0)
                elif l.vert == trunk_rings[r+1][sn]: l[uv_layer].uv = (u1, v1)
                elif l.vert == trunk_rings[r+1][s]: l[uv_layer].uv = (u0, v1)

    # 8 Major Spreading Scaffold Boughs (Ref 3 umbrella structure)
    canopy_center = mathutils.Vector((0.0, 0.0, 18.0))
    canopy_points = []
    num_boughs = 8

    for i in range(num_boughs):
        ang = i * (2.0 * math.pi / num_boughs) + random.uniform(-0.1, 0.1)
        reach = random.uniform(10.0, 14.5)
        lift = random.uniform(6.5, 9.5)

        start = mathutils.Vector((0.8*math.cos(ang), 0.8*math.sin(ang), 9.0))
        end = start + mathutils.Vector((reach*math.cos(ang), reach*math.sin(ang), lift))
        mid = (start + end)*0.5 + mathutils.Vector((0, 0, -1.0))

        # Build bough
        pts = [start, mid, end]
        b_rings = []
        b_segs = 8
        for bi in range(6):
            bt = bi / 5.0
            pos = (1-bt)**2 * pts[0] + 2*(1-bt)*bt * pts[1] + bt**2 * pts[2]
            rad = 0.9 * (1.0 - bt * 0.6)
            tan = (2*(1-bt)*(pts[1]-pts[0]) + 2*bt*(pts[2]-pts[1])).normalized()
            up_v = mathutils.Vector((0,0,1))
            rt_v = tan.cross(up_v).normalized()
            up_c = rt_v.cross(tan).normalized()

            ring = []
            for bs in range(b_segs):
                ba = bs * (2.0 * math.pi / b_segs)
                r_pos = pos + (rt_v*math.cos(ba) + up_c*math.sin(ba)) * rad
                ring.append(bm.verts.new(r_pos))
            b_rings.append(ring)

            # Record branch points for leaf placement!
            if bi >= 2:
                canopy_points.append(pos)

        for br in range(len(b_rings) - 1):
            for bs in range(b_segs):
                bsn = (bs + 1) % b_segs
                face = bm.faces.new([b_rings[br][bs], b_rings[br][bsn], b_rings[br+1][bsn], b_rings[br+1][bs]])
                face.material_index = 0

        # 4 Secondary twigs per bough
        for si in range(4):
            st = 0.35 + si * 0.2
            twig_root = (1-st)**2 * pts[0] + 2*(1-st)*st * pts[1] + st**2 * pts[2]
            s_ang = ang + random.uniform(-0.6, 0.6)
            s_reach = random.uniform(3.0, 6.0)
            twig_tip = twig_root + mathutils.Vector((s_reach*math.cos(s_ang), s_reach*math.sin(s_ang), random.uniform(0.5, 3.5)))
            canopy_points.append(twig_tip)
            canopy_points.append((twig_root + twig_tip) * 0.5)

    # C. Distribute 480+ Interlocking Leaf Cards to create a dense, lush umbrella dome!
    print(f"  Distributing 480+ leaf cards across canopy volume...")
    # 1. Outer canopy shell cards
    for cp in canopy_points:
        # Place 4-6 cards around each branch node
        for _ in range(random.randint(4, 7)):
            offset = mathutils.Vector((random.uniform(-1.8, 1.8), random.uniform(-1.8, 1.8), random.uniform(-1.0, 1.6)))
            c_pos = cp + offset
            norm_d = (c_pos - canopy_center).normalized() + mathutils.Vector((random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), random.uniform(0.1, 0.4)))
            add_curved_leaf_quad(bm, uv_layer, c_pos, (2.6, 2.6), norm_d, canopy_center, mat_idx=1)

    # 2. Fill the central umbrella crest (top crown)
    print("  Generating central umbrella crest and crown layers...")
    for _ in range(120):
        c_ang = random.uniform(0.0, 2.0 * math.pi)
        c_rad = random.uniform(0.0, 12.0)
        # Umbrella dome formula: z = 23.5 - 0.05 * rad^2
        cz = 23.5 - 0.045 * (c_rad**2) + random.uniform(-0.8, 1.2)
        cx = c_rad * math.cos(c_ang)
        cy = c_rad * math.sin(c_ang)
        card_pt = mathutils.Vector((cx, cy, cz))
        norm_d = mathutils.Vector((cx*0.06, cy*0.06, 1.0)).normalized()
        add_curved_leaf_quad(bm, uv_layer, card_pt, (2.8, 2.8), norm_d, canopy_center, mat_idx=1)

    bm.to_mesh(mesh)
    bm.free()

    # Apply Spherical Normals
    print("  Calculating sphericalized split normals for lush shading...")
    custom_norms = []
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            v_idx = mesh.loops[loop_idx].vertex_index
            v_pos = mesh.vertices[v_idx].co
            if poly.material_index == 1:
                dir_v = (v_pos - canopy_center).normalized()
                # 80% radial + 20% upward so top leaves catch direct sunlight
                custom_norms.append((dir_v * 0.80 + mathutils.Vector((0, 0, 0.55))).normalized())
            else:
                custom_norms.append(poly.normal)
    mesh.normals_split_custom_set(custom_norms)
    export(obj, "SM_Natural_Raintree_Grand.fbx")

    # -------------------------------------------------------------
    # 2. SM_Natural_Banyan_Heritage (Ref 2: Gnarled Trunks & Dense Clumps)
    # -------------------------------------------------------------
    print("\nBuilding High-Density SM_Natural_Banyan_Heritage...")
    reset()
    random.seed(202)

    mat_bark = get_mat("M_Bark_Natural_Gnarled", (0.24, 0.18, 0.12, 1.0), roughness=0.88)
    mat_leaf = get_mat("M_Foliage_Banyan_Natural", (0.12, 0.40, 0.08, 1.0), roughness=0.50)

    mesh = bpy.data.meshes.new("SM_Natural_Banyan_Heritage")
    obj = bpy.data.objects.new("SM_Natural_Banyan_Heritage", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # Gnarled twisting trunk with root buttresses
    num_rings = 10
    segments = 14
    trunk_rings = []
    for r in range(num_rings):
        t = r / float(num_rings - 1)
        z = t * 8.0
        rad = 2.6 * (1.0 - t * 0.42)
        twist = t * 1.5
        ox = 0.6 * math.sin(twist)
        oy = 0.6 * math.cos(twist)
        ring = []
        for s in range(segments):
            ang = s * (2.0 * math.pi / segments)
            ring.append(bm.verts.new(mathutils.Vector((rad*math.cos(ang) + ox, rad*math.sin(ang) + oy, z))))
        trunk_rings.append(ring)

    for r in range(num_rings - 1):
        for s in range(segments):
            sn = (s + 1) % segments
            f = bm.faces.new([trunk_rings[r][s], trunk_rings[r][sn], trunk_rings[r+1][sn], trunk_rings[r+1][s]])
            f.material_index = 0
            u0 = (s / float(segments)) * 3.0
            u1 = ((s + 1) / float(segments)) * 3.0
            v0 = (r / float(num_rings)) * 5.0
            v1 = ((r + 1) / float(num_rings)) * 5.0
            for l in f.loops:
                if l.vert == trunk_rings[r][s]: l[uv_layer].uv = (u0, v0)
                elif l.vert == trunk_rings[r][sn]: l[uv_layer].uv = (u1, v0)
                elif l.vert == trunk_rings[r+1][sn]: l[uv_layer].uv = (u1, v1)
                elif l.vert == trunk_rings[r+1][s]: l[uv_layer].uv = (u0, v1)

    # 4 Hanging prop roots & horizontal limbs
    canopy_center = mathutils.Vector((0.0, 0.0, 15.0))
    banyan_points = []
    prop_angles = [0.3, 1.8, 3.4, 4.9]
    for pa in prop_angles:
        px = 7.5 * math.cos(pa)
        py = 7.5 * math.sin(pa)
        p_root = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.45, radius2=0.25, depth=9.0)
        bmesh.ops.translate(bm, vec=(px, py, 4.5), verts=p_root["verts"])

        # Horizontal limb
        limb = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.8, radius2=0.35, depth=11.0)
        limb_start = mathutils.Vector((0, 0, 7.5))
        limb_end = mathutils.Vector((px*1.3, py*1.3, 11.5))
        mid = (limb_start + limb_end) * 0.5
        dir_v = (limb_end - limb_start).normalized()
        rot_q = mathutils.Vector((0, 0, 1)).rotation_difference(dir_v)
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_q.to_matrix(), verts=limb["verts"])
        bmesh.ops.translate(bm, vec=mid, verts=limb["verts"])

        for k in range(5):
            kt = k / 4.0
            pos = limb_start + (limb_end - limb_start)*kt
            banyan_points.append(pos)
            for _ in range(3):
                banyan_points.append(pos + mathutils.Vector((random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(0.5, 3.0))))

    # Distribute 380+ broad glossy leaf cards
    for bp in banyan_points:
        for _ in range(random.randint(3, 6)):
            c_pos = bp + mathutils.Vector((random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), random.uniform(-0.8, 1.4)))
            norm_d = (c_pos - canopy_center).normalized()
            add_curved_leaf_quad(bm, uv_layer, c_pos, (2.5, 2.5), norm_d, canopy_center, mat_idx=1)

    bm.to_mesh(mesh)
    bm.free()

    custom_norms = []
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            v_idx = mesh.loops[loop_idx].vertex_index
            v_pos = mesh.vertices[v_idx].co
            if poly.material_index == 1:
                custom_norms.append((v_pos - canopy_center).normalized())
            else:
                custom_norms.append(poly.normal)
    mesh.normals_split_custom_set(custom_norms)
    export(obj, "SM_Natural_Banyan_Heritage.fbx")

    # -------------------------------------------------------------
    # 3. SM_Natural_Krishnachura_Bloom (Ref 1: Scarlet Wuxia Bloom)
    # -------------------------------------------------------------
    print("\nBuilding High-Density SM_Natural_Krishnachura_Bloom...")
    reset()
    random.seed(303)

    mat_bark = get_mat("M_Bark_Natural_Gnarled", (0.26, 0.20, 0.14, 1.0), roughness=0.80)
    mat_leaf = get_mat("M_Foliage_Krishnachura_Natural", (0.88, 0.18, 0.08, 1.0), roughness=0.45)

    mesh = bpy.data.meshes.new("SM_Natural_Krishnachura_Bloom")
    obj = bpy.data.objects.new("SM_Natural_Krishnachura_Bloom", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # Vase-shaped multi-forked trunk
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=1.5, radius2=1.0, depth=6.5)
    bmesh.ops.translate(bm, vec=(0, 0, 3.25), verts=trunk["verts"])

    canopy_center = mathutils.Vector((0, 0, 12.0))
    k_points = []
    for ang in [0.2, 1.4, 2.6, 3.8, 5.0]:
        limb = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.65, radius2=0.28, depth=8.5)
        l_start = mathutils.Vector((0.4*math.cos(ang), 0.4*math.sin(ang), 5.5))
        l_end = mathutils.Vector((7.5*math.cos(ang), 7.5*math.sin(ang), 10.5))
        mid = (l_start + l_end)*0.5
        dir_v = (l_end - l_start).normalized()
        rot_q = mathutils.Vector((0,0,1)).rotation_difference(dir_v)
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_q.to_matrix(), verts=limb["verts"])
        bmesh.ops.translate(bm, vec=mid, verts=limb["verts"])

        for ki in range(5):
            kt = ki / 4.0
            kp = l_start + (l_end - l_start)*kt
            k_points.append(kp)
            for _ in range(4):
                k_points.append(kp + mathutils.Vector((random.uniform(-1.8, 1.8), random.uniform(-1.8, 1.8), random.uniform(0.4, 2.8))))

    # 420+ Flaming Scarlet blossom cards
    for kp in k_points:
        for _ in range(random.randint(3, 6)):
            c_pos = kp + mathutils.Vector((random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2), random.uniform(-0.6, 1.4)))
            norm_d = (c_pos - canopy_center).normalized()
            add_curved_leaf_quad(bm, uv_layer, c_pos, (2.4, 2.4), norm_d, canopy_center, mat_idx=1)

    bm.to_mesh(mesh)
    bm.free()

    custom_norms = []
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            v_idx = mesh.loops[loop_idx].vertex_index
            v_pos = mesh.vertices[v_idx].co
            if poly.material_index == 1:
                custom_norms.append((v_pos - canopy_center).normalized())
            else:
                custom_norms.append(poly.normal)
    mesh.normals_split_custom_set(custom_norms)
    export(obj, "SM_Natural_Krishnachura_Bloom.fbx")

    print("\n✓ ALL HIGH-DENSITY NATURAL TREE MODELS BUILT SUCCESSFULLY!")

if __name__ == "__main__":
    generate_enhanced_textures()
    generate_dense_trees()
