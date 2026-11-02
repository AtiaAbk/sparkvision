#!/usr/bin/env python3
"""
Procedural Super-Natural Foliage Model Generator for Blender 5.2.3 LTS
Builds authentic, high-fidelity tree models with organic branches, individual leaf-branch cards,
and sphericalized foliage normals matching Where Winds Meet and user reference imagery:
1. SM_Natural_Raintree_Grand (24m umbrella canopy with compound pinnate leaf cards, Ref 3)
2. SM_Natural_Banyan_Heritage (22m gnarled twisting trunk with prop roots & dense foliage, Ref 2)
3. SM_Natural_Krishnachura_Bloom (16m wuxia flaming scarlet flowering hero tree, Ref 1)
4. SM_Natural_Fern_Cluster (Lush undergrowth fern clump for path and pond borders)

Metric scale: 1 Blender unit = 1 meter = 100 Unreal units.
"""

import bpy
import bmesh
import math
import mathutils
import os
import random

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/NaturalFoliage"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def get_or_create_material(name, color, roughness=0.7):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

def create_curved_leaf_quad(bm, uv_layer, center, size, normal_dir, canopy_center, mat_index):
    """
    Creates a slightly bowed 2-segment leaf card oriented in 3D space,
    with proper UVs (0 to 1) and custom normal oriented toward canopy shell.
    """
    w, h = size
    # Create local coordinate frame
    up = mathutils.Vector((0, 0, 1))
    norm = normal_dir.normalized()
    if abs(norm.dot(up)) > 0.95:
        up = mathutils.Vector((1, 0, 0))
    tangent = norm.cross(up).normalized()
    bitangent = norm.cross(tangent).normalized()

    # 6 vertices: 2 quad segments along height with central bow
    v_bottom_l = center - tangent * (w * 0.5) - bitangent * (h * 0.5)
    v_bottom_r = center + tangent * (w * 0.5) - bitangent * (h * 0.5)
    v_mid_l    = center - tangent * (w * 0.55) + norm * (h * 0.12) # Bow forward
    v_mid_r    = center + tangent * (w * 0.55) + norm * (h * 0.12)
    v_top_l    = center - tangent * (w * 0.45) + bitangent * (h * 0.5)
    v_top_r    = center + tangent * (w * 0.45) + bitangent * (h * 0.5)

    vert_bl = bm.verts.new(v_bottom_l)
    vert_br = bm.verts.new(v_bottom_r)
    vert_ml = bm.verts.new(v_mid_l)
    vert_mr = bm.verts.new(v_mid_r)
    vert_tl = bm.verts.new(v_top_l)
    vert_tr = bm.verts.new(v_top_r)

    # Face 1: lower quad
    f1 = bm.faces.new([vert_bl, vert_br, vert_mr, vert_ml])
    f1.material_index = mat_index
    # Face 2: upper quad
    f2 = bm.faces.new([vert_ml, vert_mr, vert_tr, vert_tl])
    f2.material_index = mat_index

    # UV Mapping: (0,0) bottom-left, (1,1) top-right
    for l in f1.loops:
        if l.vert == vert_bl: l[uv_layer].uv = (0.0, 0.0)
        elif l.vert == vert_br: l[uv_layer].uv = (1.0, 0.0)
        elif l.vert == vert_mr: l[uv_layer].uv = (1.0, 0.5)
        elif l.vert == vert_ml: l[uv_layer].uv = (0.0, 0.5)

    for l in f2.loops:
        if l.vert == vert_ml: l[uv_layer].uv = (0.0, 0.5)
        elif l.vert == vert_mr: l[uv_layer].uv = (1.0, 0.5)
        elif l.vert == vert_tr: l[uv_layer].uv = (1.0, 1.0)
        elif l.vert == vert_tl: l[uv_layer].uv = (0.0, 1.0)

    return [vert_bl, vert_br, vert_ml, vert_mr, vert_tl, vert_tr]

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
    print(f"  ✓ Exported: {filepath} ({os.path.getsize(filepath) / 1024.0:.1f} KB)")

# ==============================================================================
# 1. SM_Natural_Raintree_Grand (Height: 24m, Spread: 28m Umbrella Canopy, Ref 3)
# ==============================================================================
def build_natural_raintree():
    print("\n[1/4] Building SM_Natural_Raintree_Grand...")
    reset_scene()
    random.seed(42)

    mat_bark = get_or_create_material("M_Bark_Natural_Gnarled", (0.24, 0.18, 0.12, 1.0), roughness=0.85)
    mat_leaf = get_or_create_material("M_Foliage_Natural_Leaf", (0.18, 0.45, 0.10, 1.0), roughness=0.45)

    mesh = bpy.data.meshes.new("SM_Natural_Raintree_Grand")
    obj = bpy.data.objects.new("SM_Natural_Raintree_Grand", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0
    obj.data.materials.append(mat_leaf) # Slot 1

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # A. Buttressed Organic Trunk (Height 9.5m, Base Radius 2.2m with flare, forks at 8.5m)
    trunk_verts = []
    num_rings = 8
    segments = 14
    for r in range(num_rings):
        t = r / float(num_rings - 1)
        z = t * 9.5
        # Base flare
        rad = (2.2 * (1.0 - t * 0.6) + 0.3 * (1.0 - t)**3)
        # Organic wobble
        ox = 0.35 * math.sin(t * 3.0)
        oy = 0.25 * math.cos(t * 2.5)

        ring = []
        for s in range(segments):
            ang = s * (2.0 * math.pi / segments)
            # Buttress flutes at base
            flute = 0.35 * math.cos(ang * 4.0) * (1.0 - t)**2 if t < 0.4 else 0.0
            x = (rad + flute) * math.cos(ang) + ox
            y = (rad + flute) * math.sin(ang) + oy
            vert = bm.verts.new(mathutils.Vector((x, y, z)))
            ring.append(vert)
        trunk_verts.append(ring)

    # Stitch trunk rings
    for r in range(num_rings - 1):
        for s in range(segments):
            s_next = (s + 1) % segments
            v1 = trunk_verts[r][s]
            v2 = trunk_verts[r][s_next]
            v3 = trunk_verts[r+1][s_next]
            v4 = trunk_verts[r+1][s]
            f = bm.faces.new([v1, v2, v3, v4])
            f.material_index = 0
            # Simple cylinder UV
            u0 = s / float(segments)
            u1 = (s + 1) / float(segments)
            v_low = r / float(num_rings)
            v_high = (r + 1) / float(num_rings)
            for l in f.loops:
                if l.vert == v1: l[uv_layer].uv = (u0, v_low)
                elif l.vert == v2: l[uv_layer].uv = (u1, v_low)
                elif l.vert == v3: l[uv_layer].uv = (u1, v_high)
                elif l.vert == v4: l[uv_layer].uv = (u0, v_high)

    # B. 6 Major Spreading Scaffold Branches reaching outward in umbrella formation
    branch_tips = []
    num_limbs = 6
    canopy_center = mathutils.Vector((0.0, 0.0, 18.0))

    for i in range(num_limbs):
        base_ang = i * (2.0 * math.pi / num_limbs) + random.uniform(-0.15, 0.15)
        reach = random.uniform(9.0, 13.0)
        lift = random.uniform(7.0, 10.5)

        start_pt = mathutils.Vector((0.7 * math.cos(base_ang), 0.7 * math.sin(base_ang), 9.0))
        end_pt = start_pt + mathutils.Vector((reach * math.cos(base_ang), reach * math.sin(base_ang), lift))
        mid_pt = (start_pt + end_pt) * 0.5 + mathutils.Vector((0.0, 0.0, -1.2)) # Natural sag

        # Build cylinder along bezier curve
        pts = [start_pt, mid_pt, end_pt]
        b_rings = []
        b_segs = 8
        for b_idx in range(6):
            bt = b_idx / 5.0
            # Quadratic bezier
            pos = (1-bt)**2 * pts[0] + 2*(1-bt)*bt * pts[1] + bt**2 * pts[2]
            rad = 0.85 * (1.0 - bt * 0.65)
            # Tangent
            tan = 2*(1-bt)*(pts[1] - pts[0]) + 2*bt*(pts[2] - pts[1])
            norm = tan.normalized()
            up_vec = mathutils.Vector((0, 0, 1))
            right_vec = norm.cross(up_vec).normalized()
            up_corrected = right_vec.cross(norm).normalized()

            ring = []
            for bs in range(b_segs):
                bang = bs * (2.0 * math.pi / b_segs)
                r_pos = pos + (right_vec * math.cos(bang) + up_corrected * math.sin(bang)) * rad
                ring.append(bm.verts.new(r_pos))
            b_rings.append(ring)

        # Stitch branch
        for br in range(len(b_rings) - 1):
            for bs in range(b_segs):
                bs_next = (bs + 1) % b_segs
                face = bm.faces.new([b_rings[br][bs], b_rings[br][bs_next], b_rings[br+1][bs_next], b_rings[br+1][bs]])
                face.material_index = 0

        # Sub-branches
        for sub_i in range(3):
            sub_ang = base_ang + random.uniform(-0.6, 0.6)
            sub_reach = random.uniform(3.0, 5.5)
            sub_pt = end_pt + mathutils.Vector((sub_reach * math.cos(sub_ang), sub_reach * math.sin(sub_ang), random.uniform(-0.5, 2.5)))
            branch_tips.append(sub_pt)

    # C. Distribute 180+ Leaf Branch Cards in Layered Umbrella Canopy
    leaf_verts_all = []
    print(f"  Generating leaf cards around {len(branch_tips)} branch endpoints...")
    for tip in branch_tips:
        # Generate cluster of 8-12 leaf quads around each tip
        cluster_size = random.randint(8, 12)
        for _ in range(cluster_size):
            offset = mathutils.Vector((
                random.uniform(-2.2, 2.2),
                random.uniform(-2.2, 2.2),
                random.uniform(-1.0, 1.8)
            ))
            card_center = tip + offset
            normal_dir = (card_center - canopy_center).normalized() + mathutils.Vector((
                random.uniform(-0.4, 0.4),
                random.uniform(-0.4, 0.4),
                random.uniform(-0.2, 0.3)
            ))
            card_size = (random.uniform(2.4, 3.4), random.uniform(2.4, 3.4))
            v_list = create_curved_leaf_quad(bm, uv_layer, card_center, card_size, normal_dir, canopy_center, mat_index=1)
            leaf_verts_all.extend(v_list)

    bm.to_mesh(mesh)
    bm.free()

    # D. Sphericalize Canopy Normals for Soft Volumetric Foliage Shading
    # Set custom split normals for the leaf vertices pointing outward from canopy center
    print("  Applying spherical split normals to canopy cards...")
    custom_normals = []
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            v_idx = mesh.loops[loop_idx].vertex_index
            v_pos = mesh.vertices[v_idx].co
            if poly.material_index == 1:
                # Leaf card: normal points outward from canopy dome
                dir_vec = (v_pos - canopy_center).normalized()
                # Blend slightly with upward vector so leaves catch sunlight from above
                final_norm = (dir_vec * 0.75 + mathutils.Vector((0, 0, 0.45))).normalized()
                custom_normals.append(final_norm)
            else:
                # Bark: standard face normal
                custom_normals.append(poly.normal)

    mesh.normals_split_custom_set(custom_normals)
    export_fbx(obj, "SM_Natural_Raintree_Grand.fbx")

# ==============================================================================
# 2. SM_Natural_Banyan_Heritage (Gnarled Twisting Trunk & Prop Roots, Ref 2)
# ==============================================================================
def build_natural_banyan():
    print("\n[2/4] Building SM_Natural_Banyan_Heritage...")
    reset_scene()
    random.seed(55)

    mat_bark = get_or_create_material("M_Bark_Natural_Gnarled", (0.22, 0.17, 0.13, 1.0), roughness=0.88)
    mat_leaf = get_or_create_material("M_Foliage_Banyan_Natural", (0.12, 0.38, 0.08, 1.0), roughness=0.50)

    mesh = bpy.data.meshes.new("SM_Natural_Banyan_Heritage")
    obj = bpy.data.objects.new("SM_Natural_Banyan_Heritage", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0
    obj.data.materials.append(mat_leaf) # Slot 1

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # Twisted, Gnarled Central Trunk (Height 8m, Base Radius 2.5m)
    num_rings = 8
    segments = 12
    trunk_rings = []
    for r in range(num_rings):
        t = r / float(num_rings - 1)
        z = t * 7.5
        rad = 2.4 * (1.0 - t * 0.45)
        # Gnarled spiral twist
        twist_ang = t * 1.2
        ox = 0.5 * math.sin(twist_ang)
        oy = 0.5 * math.cos(twist_ang)

        ring = []
        for s in range(segments):
            ang = s * (2.0 * math.pi / segments)
            x = rad * math.cos(ang) + ox
            y = rad * math.sin(ang) + oy
            ring.append(bm.verts.new(mathutils.Vector((x, y, z))))
        trunk_rings.append(ring)

    for r in range(num_rings - 1):
        for s in range(segments):
            sn = (s + 1) % segments
            f = bm.faces.new([trunk_rings[r][s], trunk_rings[r][sn], trunk_rings[r+1][sn], trunk_rings[r+1][s]])
            f.material_index = 0

    # 4 Aerial Prop Roots descending to ground
    prop_angles = [0.4, 1.9, 3.5, 5.0]
    for pa in prop_angles:
        px = 7.0 * math.cos(pa)
        py = 7.0 * math.sin(pa)
        p_root = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.45, radius2=0.25, depth=8.5)
        bmesh.ops.translate(bm, vec=(px, py, 4.25), verts=p_root["verts"])
        for f in p_root["verts"]:
            pass # material 0 by default

    # Spreading Horizontal Limbs
    branch_tips = []
    canopy_center = mathutils.Vector((0.0, 0.0, 14.0))
    for i, pa in enumerate(prop_angles):
        # Scaffold limb connects trunk to prop root and continues outward
        limb_start = mathutils.Vector((0.0, 0.0, 7.0))
        limb_end = mathutils.Vector((9.5 * math.cos(pa), 9.5 * math.sin(pa), 10.5))
        # Simple limb cylinder
        limb = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.75, radius2=0.35, depth=10.0)
        # Align along vector
        dir_vec = limb_end - limb_start
        mid = (limb_start + limb_end) * 0.5
        rot_q = mathutils.Vector((0, 0, 1)).rotation_difference(dir_vec.normalized())
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_q.to_matrix(), verts=limb["verts"])
        bmesh.ops.translate(bm, vec=mid, verts=limb["verts"])

        # Sub-branch tips
        for sb in range(4):
            sang = pa + random.uniform(-0.5, 0.5)
            tip_pos = limb_end + mathutils.Vector((random.uniform(1.5, 4.0)*math.cos(sang), random.uniform(1.5, 4.0)*math.sin(sang), random.uniform(0.5, 3.0)))
            branch_tips.append(tip_pos)

    # Leaf Cards (Broad glossy banyan leaves)
    for tip in branch_tips:
        for _ in range(random.randint(7, 11)):
            offset = mathutils.Vector((random.uniform(-1.8, 1.8), random.uniform(-1.8, 1.8), random.uniform(-0.8, 1.5)))
            card_center = tip + offset
            norm_dir = (card_center - canopy_center).normalized()
            create_curved_leaf_quad(bm, uv_layer, card_center, (2.6, 2.6), norm_dir, canopy_center, mat_index=1)

    bm.to_mesh(mesh)
    bm.free()

    custom_normals = []
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            v_idx = mesh.loops[loop_idx].vertex_index
            v_pos = mesh.vertices[v_idx].co
            if poly.material_index == 1:
                custom_normals.append((v_pos - canopy_center).normalized())
            else:
                custom_normals.append(poly.normal)
    mesh.normals_split_custom_set(custom_normals)
    export_fbx(obj, "SM_Natural_Banyan_Heritage.fbx")

# ==============================================================================
# 3. SM_Natural_Krishnachura_Bloom (Flaming Scarlet Wuxia Tree, Ref 1)
# ==============================================================================
def build_natural_krishnachura():
    print("\n[3/4] Building SM_Natural_Krishnachura_Bloom...")
    reset_scene()
    random.seed(77)

    mat_bark = get_or_create_material("M_Bark_Natural_Gnarled", (0.28, 0.22, 0.16, 1.0), roughness=0.80)
    mat_leaf = get_or_create_material("M_Foliage_Krishnachura_Natural", (0.85, 0.16, 0.08, 1.0), roughness=0.45)

    mesh = bpy.data.meshes.new("SM_Natural_Krishnachura_Bloom")
    obj = bpy.data.objects.new("SM_Natural_Krishnachura_Bloom", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0
    obj.data.materials.append(mat_leaf) # Slot 1

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # Spreading Vase-Shaped Trunk (Height 6.5m, forks early into 4 main trunks)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=1.4, radius2=0.9, depth=6.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 3.25), verts=trunk["verts"])

    canopy_center = mathutils.Vector((0.0, 0.0, 11.5))
    branch_tips = []
    for ang in [0.2, 1.7, 3.2, 4.8]:
        limb_start = mathutils.Vector((0.4 * math.cos(ang), 0.4 * math.sin(ang), 5.5))
        limb_end = mathutils.Vector((6.5 * math.cos(ang), 6.5 * math.sin(ang), 9.5))
        limb = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.6, radius2=0.25, depth=7.5)
        dir_vec = limb_end - limb_start
        rot_q = mathutils.Vector((0, 0, 1)).rotation_difference(dir_vec.normalized())
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_q.to_matrix(), verts=limb["verts"])
        bmesh.ops.translate(bm, vec=(limb_start + limb_end)*0.5, verts=limb["verts"])

        for sb in range(4):
            tip_pos = limb_end + mathutils.Vector((random.uniform(1.2, 3.2)*math.cos(ang), random.uniform(1.2, 3.2)*math.sin(ang), random.uniform(0.5, 2.5)))
            branch_tips.append(tip_pos)

    # Scarlet Red Flower & Foliage Cards
    for tip in branch_tips:
        for _ in range(random.randint(8, 12)):
            offset = mathutils.Vector((random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), random.uniform(-0.6, 1.4)))
            card_center = tip + offset
            norm_dir = (card_center - canopy_center).normalized()
            create_curved_leaf_quad(bm, uv_layer, card_center, (2.2, 2.2), norm_dir, canopy_center, mat_index=1)

    bm.to_mesh(mesh)
    bm.free()

    custom_normals = []
    for poly in mesh.polygons:
        for loop_idx in poly.loop_indices:
            v_idx = mesh.loops[loop_idx].vertex_index
            v_pos = mesh.vertices[v_idx].co
            if poly.material_index == 1:
                custom_normals.append((v_pos - canopy_center).normalized())
            else:
                custom_normals.append(poly.normal)
    mesh.normals_split_custom_set(custom_normals)
    export_fbx(obj, "SM_Natural_Krishnachura_Bloom.fbx")

# ==============================================================================
# 4. SM_Natural_Fern_Cluster (Undergrowth Fern, Ref 1 Foreground)
# ==============================================================================
def build_natural_fern():
    print("\n[4/4] Building SM_Natural_Fern_Cluster...")
    reset_scene()
    random.seed(88)

    mat_fern = get_or_create_material("M_Foliage_Fern_Natural", (0.14, 0.48, 0.08, 1.0), roughness=0.40)

    mesh = bpy.data.meshes.new("SM_Natural_Fern_Cluster")
    obj = bpy.data.objects.new("SM_Natural_Fern_Cluster", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_fern)

    bm = bmesh.new()
    uv_layer = bm.loops.layers.uv.new("UVMap")

    # 10 radiating curved fern fronds
    num_fronds = 10
    for f_idx in range(num_fronds):
        ang = f_idx * (2.0 * math.pi / num_fronds) + random.uniform(-0.15, 0.15)
        reach = random.uniform(1.2, 1.8)
        height = random.uniform(0.8, 1.2)

        center = mathutils.Vector((reach * 0.5 * math.cos(ang), reach * 0.5 * math.sin(ang), height * 0.5))
        norm_dir = mathutils.Vector((math.cos(ang), math.sin(ang), 0.6)).normalized()
        create_curved_leaf_quad(bm, uv_layer, center, (1.2, 1.6), norm_dir, mathutils.Vector((0, 0, 0)), mat_index=0)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Natural_Fern_Cluster.fbx")

    print("\n✓ ALL 4 SUPER-NATURAL FOLIAGE MODELS SUCCESSFULLY BUILT!")

if __name__ == "__main__":
    build_natural_raintree()
    build_natural_banyan()
    build_natural_krishnachura()
    build_natural_fern()
