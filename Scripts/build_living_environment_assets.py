#!/usr/bin/env python3
"""
Living University of Dhaka Environment Asset Generator for Blender 5.2.3 LTS
Creates authentic Bangladeshi botanical & environmental assets:
  1. SM_Tree_Banyan_Mature (Iconic Heritage Banyan with hanging prop roots & vast canopy)
  2. SM_Tree_Raintree_Avenue (Century-old Raintree with symmetrical umbrella canopy)
  3. SM_Tree_Krishnachura_Bloom (Flamboyant with fiery scarlet-red flowering crown)
  4. SM_Tree_Radhachura_Yellow (Yellow Poinciana with golden blossom panicles)
  5. SM_Tree_Jarul_Purple (Pride of India with lilac-purple flowers for pond edges)
  6. SM_Tree_Neem_Delicate (Airy medicinal neem with light fluttering foliage)
  7. SM_Tree_Palm_Coconut (Curved ringed coconut palm with arching fronds)
  8. SM_Tree_Palm_BetelNut (Pencil-straight supari palm with compact upright crown)
  9. SM_Cluster_Bamboo_Thicket (Bengal golden bamboo cluster with arching culms)
  10. SM_Pond_WaterLily_Cluster (Floating Shapla pads & white-lilac blossoms)
  11. SM_Plant_Reeds_Kashful (Wetland reeds & feathery silver-white plumes)
  12. SM_Curzon_Pond_Ghat (Historic stepped red-brick water descent)
  13. SM_Decal_Petal_Scatter (Fallen scarlet blossom ground scatter)

Metric scale: 1 Blender unit = 1 meter = 100 Unreal units.
"""

import bpy
import bmesh
import math
import mathutils
import os

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Environment"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

def get_or_create_material(name, color, roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat

def assign_material_to_verts(bm, verts, mat_index):
    for f in bm.faces:
        if all(v in verts for v in f.verts):
            f.material_index = mat_index

def assign_material_to_any_verts(bm, verts, mat_index):
    for f in bm.faces:
        if any(v in verts for v in f.verts):
            f.material_index = mat_index

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

# ==============================================================================
# 1. SM_Tree_Banyan_Mature (Height: 24m, Canopy: 36m, 6 Prop Roots)
# ==============================================================================
def build_tree_banyan():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Banyan", (0.24, 0.20, 0.16, 1.0), roughness=0.88)
    mat_leaf = get_or_create_material("M_Foliage_Banyan_Leaf", (0.08, 0.22, 0.06, 1.0), roughness=0.55)

    mesh = bpy.data.meshes.new("SM_Tree_Banyan_Mature")
    obj = bpy.data.objects.new("SM_Tree_Banyan_Mature", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0: Bark
    obj.data.materials.append(mat_leaf) # Slot 1: Foliage

    bm = bmesh.new()

    # Massive Central Buttressed Trunk (Base radius 2.6m, forks at 7.0m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=2.6, radius2=1.8, depth=7.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 3.5), verts=trunk["verts"])

    # 4 Fluted Buttress Roots at Base
    for ang in [0.0, math.pi/2.0, math.pi, 3.0*math.pi/2.0]:
        bx = 2.8 * math.cos(ang)
        by = 2.8 * math.sin(ang)
        bt = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(1.2, 0.6, 3.0), verts=bt["verts"])
        rot = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot, verts=bt["verts"])
        bmesh.ops.translate(bm, vec=(bx, by, 1.5), verts=bt["verts"])

    # 6 Major Spreading Scaffold Limbs (reaching outward 10m - 16m)
    limb_angles = [0.2, 1.1, 2.2, 3.3, 4.4, 5.5]
    for la in limb_angles:
        lx = 6.0 * math.cos(la)
        ly = 6.0 * math.sin(la)
        limb = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=1.1, radius2=0.5, depth=9.0)
        rot_x = mathutils.Matrix.Rotation(math.radians(55.0), 3, 'Y')
        rot_z = mathutils.Matrix.Rotation(la, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_x, verts=limb["verts"])
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_z, verts=limb["verts"])
        bmesh.ops.translate(bm, vec=(lx*0.6, ly*0.6, 9.5), verts=limb["verts"])

        # Hanging Aerial Prop Root descending to the ground!
        px = 10.5 * math.cos(la)
        py = 10.5 * math.sin(la)
        p_root = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.45, radius2=0.35, depth=11.0)
        bmesh.ops.translate(bm, vec=(px, py, 5.5), verts=p_root["verts"])

    # Tiered Sprawling Foliage Canopies (Dark Emerald Leaves, Slot 1)
    # 7 Interlocking Canopy Domes
    canopy_centers = [
        (0.0, 0.0, 18.0, 14.0, 7.5),
        (-9.0, -7.0, 14.5, 11.0, 6.0),
        (9.0, -7.0, 15.0, 11.0, 6.0),
        (-9.0, 8.0, 15.5, 11.5, 6.0),
        (9.0, 8.0, 15.0, 11.0, 6.0),
        (0.0, -12.0, 13.5, 10.5, 5.5),
        (0.0, 12.0, 14.0, 10.5, 5.5),
    ]

    for cx, cy, cz, rw, rh in canopy_centers:
        dome = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=1.0)
        bmesh.ops.scale(bm, vec=(rw, rw, rh), verts=dome["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=dome["verts"])
        assign_material_to_verts(bm, dome["verts"], 1) # Foliage

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Banyan_Mature.fbx")

# ==============================================================================
# 2. SM_Tree_Raintree_Avenue (Height: 28m, Canopy: 32m Umbrella)
# ==============================================================================
def build_tree_raintree():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Raintree", (0.22, 0.17, 0.13, 1.0), roughness=0.85)
    mat_leaf = get_or_create_material("M_Foliage_Raintree_Leaf", (0.11, 0.28, 0.08, 1.0), roughness=0.60)

    mesh = bpy.data.meshes.new("SM_Tree_Raintree_Avenue")
    obj = bpy.data.objects.new("SM_Tree_Raintree_Avenue", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0: Bark
    obj.data.materials.append(mat_leaf) # Slot 1: Leaf

    bm = bmesh.new()

    # Tall Clear Bole Trunk (Base 1.5m, fork at 10m, total height 12m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=1.6, radius2=1.0, depth=11.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 5.5), verts=trunk["verts"])

    # 5 Symmetrical Spreading Branches
    for i in range(5):
        ang = i * (2.0 * math.pi / 5)
        bx = 4.5 * math.cos(ang)
        by = 4.5 * math.sin(ang)
        br = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.8, radius2=0.35, depth=10.0)
        rot_y = mathutils.Matrix.Rotation(math.radians(45.0), 3, 'Y')
        rot_z = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_y, verts=br["verts"])
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_z, verts=br["verts"])
        bmesh.ops.translate(bm, vec=(bx*0.6, by*0.6, 13.5), verts=br["verts"])

    # Classical Vast Symmetrical Umbrella Canopy (Diameter 30m, Height 8m)
    c_umbrella = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=14, radius=1.0)
    bmesh.ops.scale(bm, vec=(15.0, 15.0, 6.5), verts=c_umbrella["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 21.0), verts=c_umbrella["verts"])
    assign_material_to_verts(bm, c_umbrella["verts"], 1)

    # Sub-canopy feather layer for dappled light
    c_lower = bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=1.0)
    bmesh.ops.scale(bm, vec=(12.0, 12.0, 4.0), verts=c_lower["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 17.5), verts=c_lower["verts"])
    assign_material_to_verts(bm, c_lower["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Raintree_Avenue.fbx")

# ==============================================================================
# 3. SM_Tree_Krishnachura_Bloom (Height: 15m, Canopy: 18m Flaming Red)
# ==============================================================================
def build_tree_krishnachura():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Krishnachura", (0.28, 0.24, 0.20, 1.0), roughness=0.75)
    mat_leaf = get_or_create_material("M_Foliage_Krishnachura_Red", (0.82, 0.16, 0.08, 1.0), roughness=0.45) # Scarlet Red!

    mesh = bpy.data.meshes.new("SM_Tree_Krishnachura_Bloom")
    obj = bpy.data.objects.new("SM_Tree_Krishnachura_Bloom", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0: Bark
    obj.data.materials.append(mat_leaf) # Slot 1: Scarlet Bloom

    bm = bmesh.new()

    # Low-Forking Smooth Trunk (Height 4.5m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.9, radius2=0.6, depth=4.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.25), verts=trunk["verts"])

    # 4 Wide-Spreading Angled Branches
    for i in range(4):
        ang = i * (math.pi / 2.0) + 0.35
        bx = 3.0 * math.cos(ang)
        by = 3.0 * math.sin(ang)
        br = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.45, radius2=0.22, depth=6.5)
        rot_y = mathutils.Matrix.Rotation(math.radians(60.0), 3, 'Y')
        rot_z = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_y, verts=br["verts"])
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_z, verts=br["verts"])
        bmesh.ops.translate(bm, vec=(bx*0.6, by*0.6, 5.5), verts=br["verts"])

    # Sprawling Flat-Topped Umbrella of Brilliant Red Flowers (Diameter 18m)
    crowns = [
        (0.0, 0.0, 12.0, 8.5, 4.0),
        (-4.5, -3.5, 10.5, 6.0, 3.2),
        (4.5, -3.5, 10.8, 6.0, 3.2),
        (-3.5, 4.5, 10.6, 6.0, 3.2),
        (4.0, 4.0, 10.5, 6.0, 3.2),
    ]
    for cx, cy, cz, rw, rh in crowns:
        c = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0)
        bmesh.ops.scale(bm, vec=(rw, rw, rh), verts=c["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=c["verts"])
        assign_material_to_verts(bm, c["verts"], 1) # Red Blossom

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Krishnachura_Bloom.fbx")

# ==============================================================================
# 4. SM_Tree_Radhachura_Yellow (Height: 16m, Canopy: 16m Golden Yellow)
# ==============================================================================
def build_tree_radhachura():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Radhachura", (0.25, 0.20, 0.16, 1.0), roughness=0.80)
    mat_leaf = get_or_create_material("M_Foliage_Radhachura_Yellow", (0.86, 0.72, 0.12, 1.0), roughness=0.50) # Golden Yellow!

    mesh = bpy.data.meshes.new("SM_Tree_Radhachura_Yellow")
    obj = bpy.data.objects.new("SM_Tree_Radhachura_Yellow", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.85, radius2=0.55, depth=5.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.75), verts=trunk["verts"])

    # Golden Blossom Canopy
    for cx, cy, cz, rw, rh in [(0, 0, 13.0, 7.5, 4.5), (-3.5, 2.0, 11.5, 5.0, 3.5), (3.5, -2.0, 11.8, 5.0, 3.5)]:
        c = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0)
        bmesh.ops.scale(bm, vec=(rw, rw, rh), verts=c["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=c["verts"])
        assign_material_to_verts(bm, c["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Radhachura_Yellow.fbx")

# ==============================================================================
# 5. SM_Tree_Jarul_Purple (Height: 14m, Canopy: 12m Lilac Purple)
# ==============================================================================
def build_tree_jarul():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Jarul", (0.32, 0.29, 0.26, 1.0), roughness=0.70)
    mat_leaf = get_or_create_material("M_Foliage_Jarul_Lilac", (0.58, 0.28, 0.65, 1.0), roughness=0.50) # Lilac Purple!

    mesh = bpy.data.meshes.new("SM_Tree_Jarul_Purple")
    obj = bpy.data.objects.new("SM_Tree_Jarul_Purple", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.75, radius2=0.48, depth=5.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.5), verts=trunk["verts"])

    # Lilac Flower Panicle Canopy
    for cx, cy, cz, rw, rh in [(0, 0, 11.5, 6.0, 4.2), (-2.5, -2.0, 9.8, 4.5, 3.0), (2.5, 2.0, 10.2, 4.5, 3.0)]:
        c = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0)
        bmesh.ops.scale(bm, vec=(rw, rw, rh), verts=c["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=c["verts"])
        assign_material_to_verts(bm, c["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Jarul_Purple.fbx")

# ==============================================================================
# 6. SM_Tree_Neem_Delicate (Height: 12m, Light Fluttering Canopy)
# ==============================================================================
def build_tree_neem():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Neem", (0.20, 0.16, 0.13, 1.0), roughness=0.85)
    mat_leaf = get_or_create_material("M_Foliage_Neem_Green", (0.16, 0.38, 0.12, 1.0), roughness=0.60)

    mesh = bpy.data.meshes.new("SM_Tree_Neem_Delicate")
    obj = bpy.data.objects.new("SM_Tree_Neem_Delicate", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.55, radius2=0.35, depth=5.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.5), verts=trunk["verts"])

    # Airy Light Canopy
    for cx, cy, cz, rw, rh in [(0, 0, 9.5, 4.8, 3.8), (-1.8, 1.5, 8.2, 3.2, 2.6), (1.8, -1.5, 8.5, 3.2, 2.6)]:
        c = bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=8, radius=1.0)
        bmesh.ops.scale(bm, vec=(rw, rw, rh), verts=c["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=c["verts"])
        assign_material_to_verts(bm, c["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Neem_Delicate.fbx")

# ==============================================================================
# 7. SM_Tree_Palm_Coconut (Height: 20m, Curved Ringed Trunk)
# ==============================================================================
def build_palm_coconut():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_PalmRinged", (0.35, 0.32, 0.28, 1.0), roughness=0.80)
    mat_leaf = get_or_create_material("M_Foliage_PalmFrond", (0.12, 0.32, 0.09, 1.0), roughness=0.50)

    mesh = bpy.data.meshes.new("SM_Tree_Palm_Coconut")
    obj = bpy.data.objects.new("SM_Tree_Palm_Coconut", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()

    # Curved Trunk built from 6 segments leaning outward (classic water-leaning palm!)
    num_seg = 6
    seg_len = 3.2
    cur_x = 0.0
    cur_z = 0.0
    for s in range(num_seg):
        r1 = 0.45 - s * 0.03
        r2 = 0.42 - s * 0.03
        lean_dx = 0.45 * (s / num_seg) ** 1.5
        c = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=r1, radius2=r2, depth=seg_len)
        bmesh.ops.translate(bm, vec=(cur_x + lean_dx/2.0, 0.0, cur_z + seg_len/2.0), verts=c["verts"])
        cur_x += lean_dx
        cur_z += seg_len

    # Crown of 12 Arching Pinnate Fronds at apex
    crown_z = cur_z
    crown_x = cur_x
    for i in range(12):
        ang = i * (2.0 * math.pi / 12)
        fx = 2.4 * math.cos(ang)
        fy = 2.4 * math.sin(ang)
        frond = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.5, radius2=0.08, depth=4.8)
        rot_y = mathutils.Matrix.Rotation(math.radians(65.0), 3, 'Y')
        rot_z = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_y, verts=frond["verts"])
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_z, verts=frond["verts"])
        bmesh.ops.translate(bm, vec=(crown_x + fx*0.5, fy*0.5, crown_z - 0.5), verts=frond["verts"])
        assign_material_to_verts(bm, frond["verts"], 1) # Palm frond

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Palm_Coconut.fbx")

# ==============================================================================
# 8. SM_Tree_Palm_BetelNut (Height: 16m, Pencil-Straight Supari Palm)
# ==============================================================================
def build_palm_betel():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_BetelGreen", (0.28, 0.35, 0.22, 1.0), roughness=0.65)
    mat_leaf = get_or_create_material("M_Foliage_BetelCrown", (0.10, 0.30, 0.08, 1.0), roughness=0.50)

    mesh = bpy.data.meshes.new("SM_Tree_Palm_BetelNut")
    obj = bpy.data.objects.new("SM_Tree_Palm_BetelNut", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()

    # Pencil-Straight Ringed Trunk (Radius 0.22m, height 14m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.25, radius2=0.18, depth=14.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 7.0), verts=trunk["verts"])

    # Compact Upright Crown Fronds
    for i in range(8):
        ang = i * (2.0 * math.pi / 8)
        fr = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.35, radius2=0.06, depth=3.0)
        rot_y = mathutils.Matrix.Rotation(math.radians(35.0), 3, 'Y')
        rot_z = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_y, verts=fr["verts"])
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_z, verts=fr["verts"])
        bmesh.ops.translate(bm, vec=(0.6*math.cos(ang), 0.6*math.sin(ang), 14.8), verts=fr["verts"])
        assign_material_to_verts(bm, fr["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Palm_BetelNut.fbx")

# ==============================================================================
# 9. SM_Cluster_Bamboo_Thicket (Bengal Golden Bamboo Cluster)
# ==============================================================================
def build_bamboo_thicket():
    reset_scene()
    mat_stem = get_or_create_material("M_Stem_BambooGold", (0.75, 0.68, 0.22, 1.0), roughness=0.45) # Golden yellow!
    mat_leaf = get_or_create_material("M_Foliage_BambooLeaf", (0.16, 0.35, 0.10, 1.0), roughness=0.55)

    mesh = bpy.data.meshes.new("SM_Cluster_Bamboo_Thicket")
    obj = bpy.data.objects.new("SM_Cluster_Bamboo_Thicket", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_stem)
    obj.data.materials.append(mat_leaf)

    bm = bmesh.new()

    # Clump of 18 Culms sprouting from root crown ($4.0m cluster diameter)
    num_culms = 18
    for i in range(num_culms):
        ang = i * (2.0 * math.pi / num_culms)
        dist = 0.4 + (i % 3) * 0.65
        cx = dist * math.cos(ang)
        cy = dist * math.sin(ang)
        h = 11.0 + (i % 5) * 0.8
        
        # Culm cylinder
        culm = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.08, radius2=0.04, depth=h)
        # Slight outward bend
        bend_rad = math.radians(6.0 + dist * 4.0)
        rot_y = mathutils.Matrix.Rotation(bend_rad, 3, 'Y')
        rot_z = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_y, verts=culm["verts"])
        bmesh.ops.rotate(bm, cent=(0,0,0), matrix=rot_z, verts=culm["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, h/2.0), verts=culm["verts"])

        # Feathery Leaf Spray atop each culm (Slot 1)
        tip_x = cx + math.sin(bend_rad) * h * math.cos(ang) * 0.5
        tip_y = cy + math.sin(bend_rad) * h * math.sin(ang) * 0.5
        leaf_b = bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=1.0)
        bmesh.ops.scale(bm, vec=(1.6, 1.6, 2.2), verts=leaf_b["verts"])
        bmesh.ops.translate(bm, vec=(tip_x, tip_y, h - 0.5), verts=leaf_b["verts"])
        assign_material_to_verts(bm, leaf_b["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Cluster_Bamboo_Thicket.fbx")

# ==============================================================================
# 10. SM_Pond_WaterLily_Cluster (Floating Shapla Pads & Blossoms)
# ==============================================================================
def build_water_lily_cluster():
    reset_scene()
    mat_pad = get_or_create_material("M_Foliage_LilyPad", (0.08, 0.28, 0.12, 1.0), roughness=0.35)
    mat_flower = get_or_create_material("M_Flower_Shapla", (0.92, 0.90, 0.95, 1.0), roughness=0.30) # White-lilac blossom!

    mesh = bpy.data.meshes.new("SM_Pond_WaterLily_Cluster")
    obj = bpy.data.objects.new("SM_Pond_WaterLily_Cluster", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_pad)
    obj.data.materials.append(mat_flower)

    bm = bmesh.new()

    # 10 Floating Notched Water Lily Pads
    pad_positions = [
        (0.0, 0.0, 0.45),
        (-0.6, 0.4, 0.38),
        (0.7, -0.3, 0.42),
        (-0.4, -0.7, 0.35),
        (0.8, 0.6, 0.40),
        (-0.9, -0.2, 0.36),
        (0.2, 0.9, 0.38),
        (-0.1, -1.0, 0.32),
        (1.1, 0.1, 0.34),
        (-0.8, 0.9, 0.30),
    ]

    for px, py, r_pad in pad_positions:
        # Thin disc resting at Z = 0
        pad = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=r_pad, radius2=r_pad, depth=0.02)
        bmesh.ops.translate(bm, vec=(px, py, 0.01), verts=pad["verts"])

    # 3 Upright Shapla Blossoms
    flower_positions = [(0.0, 0.0), (-0.5, 0.3), (0.6, -0.2)]
    for fx, fy in flower_positions:
        # 8-Petal Star Lotus
        fl = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.18, radius2=0.04, depth=0.15)
        bmesh.ops.translate(bm, vec=(fx, fy, 0.08), verts=fl["verts"])
        assign_material_to_verts(bm, fl["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Pond_WaterLily_Cluster.fbx")

# ==============================================================================
# 11. SM_Plant_Reeds_Kashful (Wetland Reeds & Plumes)
# ==============================================================================
def build_reeds_kashful():
    reset_scene()
    mat_stem = get_or_create_material("M_Stem_ReedGreen", (0.18, 0.32, 0.10, 1.0), roughness=0.60)
    mat_plume = get_or_create_material("M_Foliage_KashfulWhite", (0.94, 0.94, 0.92, 1.0), roughness=0.75) # Silky white plumes!

    mesh = bpy.data.meshes.new("SM_Plant_Reeds_Kashful")
    obj = bpy.data.objects.new("SM_Plant_Reeds_Kashful", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_stem)
    obj.data.materials.append(mat_plume)

    bm = bmesh.new()

    # Clump of 12 reed stalks
    for i in range(12):
        ang = i * (2.0 * math.pi / 12)
        dist = 0.25 + (i % 2) * 0.2
        rx = dist * math.cos(ang)
        ry = dist * math.sin(ang)
        rh = 2.0 + (i % 3) * 0.35

        st = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.03, radius2=0.015, depth=rh)
        bmesh.ops.translate(bm, vec=(rx, ry, rh/2.0), verts=st["verts"])

        # Feathery white plume atop stalk (Slot 1)
        plume = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.10, radius2=0.01, depth=0.65)
        bmesh.ops.translate(bm, vec=(rx, ry, rh + 0.3), verts=plume["verts"])
        assign_material_to_verts(bm, plume["verts"], 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Plant_Reeds_Kashful.fbx")

# ==============================================================================
# 12. SM_Curzon_Pond_Ghat (Historic Stepped Brick Water Descent)
# ==============================================================================
def build_pond_ghat():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.51, 0.17, 0.12, 1.0), roughness=0.82)
    mat_stone = get_or_create_material("M_Curzon_Sandstone", (0.65, 0.48, 0.35, 1.0), roughness=0.75)

    mesh = bpy.data.meshes.new("SM_Curzon_Pond_Ghat")
    obj = bpy.data.objects.new("SM_Curzon_Pond_Ghat", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_brick)
    obj.data.materials.append(mat_stone)

    bm = bmesh.new()
    width = 12.0
    num_steps = 8
    tread = 0.50
    riser = 0.22

    for s in range(num_steps):
        st = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(width, tread, (num_steps - s) * riser), verts=st["verts"])
        bmesh.ops.translate(bm, vec=(0.0, s * tread, ((num_steps - s) * riser) / 2.0), verts=st["verts"])

    # Side retaining brick walls
    for wx in [-width/2.0 - 0.3, width/2.0 + 0.3]:
        wall = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.6, num_steps * tread, num_steps * riser + 0.4), verts=wall["verts"])
        bmesh.ops.translate(bm, vec=(wx, (num_steps * tread) / 2.0, (num_steps * riser + 0.4) / 2.0), verts=wall["verts"])

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Pond_Ghat.fbx")

# ==============================================================================
# 13. SM_Decal_Petal_Scatter (Ground Fallen Blossom Decal Mesh)
# ==============================================================================
def build_petal_scatter():
    reset_scene()
    mat_petal = get_or_create_material("M_Decal_KrishnachuraPetals", (0.85, 0.15, 0.08, 1.0), roughness=0.60)

    mesh = bpy.data.meshes.new("SM_Decal_Petal_Scatter")
    obj = bpy.data.objects.new("SM_Decal_Petal_Scatter", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_petal)

    bm = bmesh.new()
    # Octagonal ground patch (4m x 4m)
    p = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=2.0, radius2=2.0, depth=0.01)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.005), verts=p["verts"])

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Decal_Petal_Scatter.fbx")

# Main Execution Flow
if __name__ == "__main__":
    print("[Environment Rebuild] Generating complete Bangladeshi botanical library...")
    build_tree_banyan()
    build_tree_raintree()
    build_tree_krishnachura()
    build_tree_radhachura()
    build_tree_jarul()
    build_tree_neem()
    build_palm_coconut()
    build_palm_betel()
    build_bamboo_thicket()
    build_water_lily_cluster()
    build_reeds_kashful()
    build_pond_ghat()
    build_petal_scatter()
    print("[Environment Rebuild] Successfully exported all 13 ecological assets to FBX!")
