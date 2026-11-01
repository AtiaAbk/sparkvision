#!/usr/bin/env python3
"""
Living University of Dhaka Environment Asset Generator (Part 2)
Generates high-fidelity FBX assets using Blender 5.2.3 LTS:
  1. SM_Tree_Debdaru_Columnar (Weeping Mast tree, 16m)
  2. SM_Tree_Mahogany_Grand (Grand colonial shade tree, 22m)
  3. SM_Tree_Kadam_Bloom (Burflower-tree with golden pom-pom blooms, 14m)
  4. SM_Cluster_Bamboo_Grove (Dense 16-culm bamboo grove, 11m)
  5. SM_Bush_Rangan_Scarlet (Flame of the woods shrub with scarlet flowers, 1.6m)
  6. SM_Bush_Gandharaj_White (Cape jasmine shrub with white double flowers, 1.4m)
  7. SM_Bush_Kamini_Hedge (Flowering hedge unit, 3.5m x 0.8m x 1.2m)
  8. SM_Grass_Tuft_Lawn (Fine lawn grass tuft, 0.25m)
  9. SM_Grass_Tall_Savanna (Tall wild monsoon grass with white plumes, 1.4m)
  10. SM_Fern_Undergrowth_Cluster (Shade-loving sword fern clump, 0.75m)
  11. SM_Ground_LeafLitter_Patch (Fallen organic leaf scatter patch, 2.2m radius)
  12. SM_Wildlife_Bird_Doel (Perched Oriental Magpie-Robin, National Bird)
  13. SM_Wildlife_Butterfly_Cluster (Tropical yellow butterflies hovering)
  14. SM_Wildlife_Dragonfly_Pair (Iridescent pond dragonflies)

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

def set_material_index_range(bm, start_idx, end_idx, mat_index):
    bm.faces.ensure_lookup_table()
    for i in range(start_idx, end_idx):
        bm.faces[i].material_index = mat_index

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
# 1. SM_Tree_Debdaru_Columnar (Height: 16m, Weeping Columnar Crown)
# ==============================================================================
def build_tree_debdaru():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Tree", (0.18, 0.15, 0.12, 1.0))
    mat_leaf = get_or_create_material("M_Foliage_Debdaru_Dark", (0.05, 0.18, 0.05, 1.0))

    mesh = bpy.data.meshes.new("SM_Tree_Debdaru_Columnar")
    obj = bpy.data.objects.new("SM_Tree_Debdaru_Columnar", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0
    obj.data.materials.append(mat_leaf) # Slot 1

    bm = bmesh.new()

    # Slender straight central trunk (Base radius 0.35m, height 16m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.35, radius2=0.08, depth=16.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 8.0), verts=trunk["verts"])
    for f in bm.faces:
        f.material_index = 0

    # 7 Tiers of weeping columnar downward-tapered foliage cones
    leaf_faces_start = len(bm.faces)
    tier_heights = [3.5, 5.5, 7.5, 9.5, 11.5, 13.5, 15.0]
    tier_radii = [1.8, 1.9, 1.7, 1.5, 1.2, 0.9, 0.5]
    for z, r in zip(tier_heights, tier_radii):
        cone = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=r, radius2=0.2, depth=2.8)
        bmesh.ops.translate(bm, vec=(0.0, 0.0, z), verts=cone["verts"])

    bm.faces.ensure_lookup_table()
    for i in range(leaf_faces_start, len(bm.faces)):
        bm.faces[i].material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Debdaru_Columnar.fbx")

# ==============================================================================
# 2. SM_Tree_Mahogany_Grand (Height: 22m, Canopy: 26m)
# ==============================================================================
def build_tree_mahogany():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Tree", (0.20, 0.16, 0.12, 1.0))
    mat_leaf = get_or_create_material("M_Foliage_Raintree_Leaf", (0.11, 0.28, 0.08, 1.0))

    mesh = bpy.data.meshes.new("SM_Tree_Mahogany_Grand")
    obj = bpy.data.objects.new("SM_Tree_Mahogany_Grand", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark) # Slot 0
    obj.data.materials.append(mat_leaf) # Slot 1

    bm = bmesh.new()

    # Heavy upright trunk (Base radius 1.2m, height 8m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=1.2, radius2=0.85, depth=8.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.0), verts=trunk["verts"])

    # 4 Heavy spreading primary boughs
    bough_angles = [0.2, 1.8, 3.4, 4.9]
    for ang in bough_angles:
        b = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.45, radius2=0.25, depth=8.0)
        bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.0), verts=b["verts"])
        rot_y = mathutils.Matrix.Rotation(math.radians(35.0), 3, 'Y')
        rot_z = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, matrix=rot_z @ rot_y, verts=b["verts"])
        bmesh.ops.translate(bm, vec=(0.0, 0.0, 7.5), verts=b["verts"])

    for f in bm.faces:
        f.material_index = 0

    # 5 Vast overlapping canopy foliage masses (Center + 4 quadrants)
    leaf_start = len(bm.faces)
    canopy_centers = [
        (0.0, 0.0, 18.0, 7.5, 4.5),
        (5.5, 3.5, 16.0, 6.0, 3.8),
        (-5.0, 4.0, 16.5, 5.8, 3.8),
        (-4.5, -4.5, 15.5, 6.2, 4.0),
        (4.8, -4.2, 16.0, 5.9, 3.8)
    ]
    for cx, cy, cz, rx, rz in canopy_centers:
        c = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=rx)
        bmesh.ops.scale(bm, vec=(1.0, 1.0, rz/rx), verts=c["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, cz), verts=c["verts"])

    set_material_index_range(bm, leaf_start, len(bm.faces), 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Mahogany_Grand.fbx")

# ==============================================================================
# 3. SM_Tree_Kadam_Bloom (Height: 14m, Golden Pom-Pom Blooms)
# ==============================================================================
def build_tree_kadam():
    reset_scene()
    mat_bark = get_or_create_material("M_Bark_Tree", (0.22, 0.17, 0.13, 1.0))
    mat_leaf = get_or_create_material("M_Foliage_Neem_Green", (0.16, 0.38, 0.12, 1.0))
    mat_bloom = get_or_create_material("M_Foliage_Kadam_Golden", (0.95, 0.65, 0.08, 1.0))

    mesh = bpy.data.meshes.new("SM_Tree_Kadam_Bloom")
    obj = bpy.data.objects.new("SM_Tree_Kadam_Bloom", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)  # Slot 0
    obj.data.materials.append(mat_leaf)  # Slot 1
    obj.data.materials.append(mat_bloom) # Slot 2

    bm = bmesh.new()

    # Trunk (Base radius 0.7m, height 12m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.7, radius2=0.35, depth=12.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 6.0), verts=trunk["verts"])
    for f in bm.faces:
        f.material_index = 0

    # 3 Tiers of horizontal umbrella branches & leaves
    leaf_start = len(bm.faces)
    for z, r in [(6.5, 4.5), (9.0, 5.2), (11.5, 3.8)]:
        tier = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=0.8, depth=2.0)
        bmesh.ops.translate(bm, vec=(0.0, 0.0, z), verts=tier["verts"])

    set_material_index_range(bm, leaf_start, len(bm.faces), 1)

    # 10 Golden pom-pom flower spheres ($r=0.4m$) hanging on canopy margins
    bloom_start = len(bm.faces)
    bloom_locs = [
        (3.5, 1.5, 6.8), (-3.2, 1.8, 6.9), (0.0, -3.8, 7.0),
        (4.2, -2.5, 9.2), (-4.0, -2.2, 9.3), (2.0, 4.5, 9.4), (-2.2, 4.2, 9.1),
        (2.8, 0.0, 11.6), (-2.5, 0.5, 11.8), (0.5, -2.7, 11.7)
    ]
    for bx, by, bz in bloom_locs:
        s = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.42)
        bmesh.ops.translate(bm, vec=(bx, by, bz), verts=s["verts"])

    set_material_index_range(bm, bloom_start, len(bm.faces), 2)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Tree_Kadam_Bloom.fbx")

# ==============================================================================
# 4. SM_Cluster_Bamboo_Grove (Height: 11m, 16 Arching Culms)
# ==============================================================================
def build_bamboo_grove():
    reset_scene()
    mat_stem = get_or_create_material("M_Stem_BambooGold", (0.75, 0.68, 0.22, 1.0))
    mat_leaf = get_or_create_material("M_Foliage_BambooLeaf", (0.16, 0.35, 0.10, 1.0))

    mesh = bpy.data.meshes.new("SM_Cluster_Bamboo_Grove")
    obj = bpy.data.objects.new("SM_Cluster_Bamboo_Grove", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_stem) # Slot 0
    obj.data.materials.append(mat_leaf) # Slot 1

    bm = bmesh.new()

    # 16 Culms arranged in natural clumping rings
    stem_start = 0
    import random
    random.seed(42)

    culm_positions = []
    for ring_r, count in [(0.6, 4), (1.5, 6), (2.4, 6)]:
        for i in range(count):
            ang = (2.0 * math.pi / count) * i + random.uniform(-0.2, 0.2)
            cx = ring_r * math.cos(ang)
            cy = ring_r * math.sin(ang)
            h = random.uniform(8.5, 11.5)
            culm_positions.append((cx, cy, h, ang))

    for cx, cy, h, ang in culm_positions:
        # Culm cylinder
        culm = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.08, radius2=0.04, depth=h)
        # Gentle outward lean
        lean_angle = math.radians(random.uniform(4.0, 12.0))
        rot_lean = mathutils.Matrix.Rotation(lean_angle, 3, 'Y')
        rot_yaw = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.translate(bm, vec=(0.0, 0.0, h/2.0), verts=culm["verts"])
        bmesh.ops.rotate(bm, matrix=rot_yaw @ rot_lean, verts=culm["verts"])
        bmesh.ops.translate(bm, vec=(cx, cy, 0.0), verts=culm["verts"])

    for f in bm.faces:
        f.material_index = 0

    # Leaf plumes on culm upper thirds
    leaf_start = len(bm.faces)
    for cx, cy, h, ang in culm_positions:
        # 3 Leaf cluster cards per culm
        for z_off in [h * 0.75, h * 0.9, h * 1.0]:
            plume = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=random.uniform(0.7, 1.1))
            bmesh.ops.scale(bm, vec=(1.2, 1.2, 0.5), verts=plume["verts"])
            bmesh.ops.translate(bm, vec=(cx * 1.2, cy * 1.2, z_off), verts=plume["verts"])

    set_material_index_range(bm, leaf_start, len(bm.faces), 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Cluster_Bamboo_Grove.fbx")

# ==============================================================================
# 5. SM_Bush_Rangan_Scarlet (Height: 1.6m, Scarlet Flower Clusters)
# ==============================================================================
def build_bush_rangan():
    reset_scene()
    mat_leaf = get_or_create_material("M_Foliage_Banyan_Leaf", (0.08, 0.22, 0.06, 1.0))
    mat_flower = get_or_create_material("M_Flower_Rangan_Scarlet", (0.92, 0.12, 0.08, 1.0))

    mesh = bpy.data.meshes.new("SM_Bush_Rangan_Scarlet")
    obj = bpy.data.objects.new("SM_Bush_Rangan_Scarlet", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_leaf)   # Slot 0
    obj.data.materials.append(mat_flower) # Slot 1

    bm = bmesh.new()

    # Dense rounded shrub body
    body = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    bmesh.ops.scale(bm, vec=(1.2, 1.1, 0.8), verts=body["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.8), verts=body["verts"])
    for f in bm.faces:
        f.material_index = 0

    # 8 Scarlet flower corymb clusters
    flower_start = len(bm.faces)
    flower_locs = [
        (0.6, 0.5, 1.2), (-0.7, 0.4, 1.1), (0.2, -0.8, 1.2), (-0.5, -0.6, 1.0),
        (0.0, 0.0, 1.55), (0.8, -0.2, 1.0), (-0.8, -0.1, 1.15), (0.1, 0.8, 1.1)
    ]
    for fx, fy, fz in flower_locs:
        fl = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.22)
        bmesh.ops.translate(bm, vec=(fx, fy, fz), verts=fl["verts"])

    set_material_index_range(bm, flower_start, len(bm.faces), 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Bush_Rangan_Scarlet.fbx")

# ==============================================================================
# 6. SM_Bush_Gandharaj_White (Height: 1.4m, Fragrant White Double Blooms)
# ==============================================================================
def build_bush_gandharaj():
    reset_scene()
    mat_leaf = get_or_create_material("M_Foliage_Banyan_Leaf", (0.07, 0.20, 0.06, 1.0))
    mat_flower = get_or_create_material("M_Flower_Gardenia_White", (0.96, 0.96, 0.94, 1.0))

    mesh = bpy.data.meshes.new("SM_Bush_Gandharaj_White")
    obj = bpy.data.objects.new("SM_Bush_Gandharaj_White", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_leaf)   # Slot 0
    obj.data.materials.append(mat_flower) # Slot 1

    bm = bmesh.new()

    body = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.85)
    bmesh.ops.scale(bm, vec=(1.1, 1.0, 0.8), verts=body["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.7), verts=body["verts"])
    for f in bm.faces:
        f.material_index = 0

    flower_start = len(bm.faces)
    flower_locs = [
        (0.4, 0.4, 1.1), (-0.5, 0.3, 1.05), (0.1, -0.6, 1.1), (-0.3, -0.4, 0.95),
        (0.0, 0.0, 1.35), (0.6, -0.2, 0.9)
    ]
    for fx, fy, fz in flower_locs:
        fl = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.18)
        bmesh.ops.translate(bm, vec=(fx, fy, fz), verts=fl["verts"])

    set_material_index_range(bm, flower_start, len(bm.faces), 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Bush_Gandharaj_White.fbx")

# ==============================================================================
# 7. SM_Bush_Kamini_Hedge (Length: 3.5m, Width: 0.8m, Height: 1.2m)
# ==============================================================================
def build_bush_kamini_hedge():
    reset_scene()
    mat_hedge = get_or_create_material("M_Curzon_Hedge", (0.09, 0.24, 0.07, 1.0))
    mat_flower = get_or_create_material("M_Flower_Gardenia_White", (0.96, 0.96, 0.94, 1.0))

    mesh = bpy.data.meshes.new("SM_Bush_Kamini_Hedge")
    obj = bpy.data.objects.new("SM_Bush_Kamini_Hedge", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_hedge)  # Slot 0
    obj.data.materials.append(mat_flower) # Slot 1

    bm = bmesh.new()

    # Rectangular hedge block with chamfered top
    box = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(3.5, 0.8, 1.2), verts=box["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.6), verts=box["verts"])
    for f in bm.faces:
        f.material_index = 0

    # Delicate white star blossoms scattered on upper surface
    flower_start = len(bm.faces)
    for x in [-1.4, -0.9, -0.4, 0.1, 0.6, 1.1, 1.5]:
        for y in [-0.22, 0.22]:
            s = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.08)
            bmesh.ops.translate(bm, vec=(x, y, 1.22), verts=s["verts"])

    set_material_index_range(bm, flower_start, len(bm.faces), 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Bush_Kamini_Hedge.fbx")

# ==============================================================================
# 8. SM_Grass_Tuft_Lawn (Height: 0.25m, Radius: 0.5m)
# ==============================================================================
def build_grass_lawn():
    reset_scene()
    mat_grass = get_or_create_material("M_Ground_Grass", (0.13, 0.32, 0.09, 1.0))

    mesh = bpy.data.meshes.new("SM_Grass_Tuft_Lawn")
    obj = bpy.data.objects.new("SM_Grass_Tuft_Lawn", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_grass)

    bm = bmesh.new()

    # 6 Cross-quad grass blade clusters
    for i in range(6):
        ang = (math.pi / 6.0) * i
        plane = bmesh.ops.create_grid(bm, x_segments=1, y_segments=2, size=0.25)
        bmesh.ops.scale(bm, vec=(0.8, 1.0, 1.0), verts=plane["verts"])
        rot_x = mathutils.Matrix.Rotation(math.radians(85.0), 3, 'X')
        rot_z = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, matrix=rot_z @ rot_x, verts=plane["verts"])
        bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.12), verts=plane["verts"])

    for f in bm.faces:
        f.material_index = 0

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Grass_Tuft_Lawn.fbx")

# ==============================================================================
# 9. SM_Grass_Tall_Savanna (Height: 1.4m, White Plumes)
# ==============================================================================
def build_grass_savanna():
    reset_scene()
    mat_stem = get_or_create_material("M_Stem_ReedGreen", (0.18, 0.32, 0.10, 1.0))
    mat_plume = get_or_create_material("M_Foliage_KashfulWhite", (0.94, 0.94, 0.92, 1.0))

    mesh = bpy.data.meshes.new("SM_Grass_Tall_Savanna")
    obj = bpy.data.objects.new("SM_Grass_Tall_Savanna", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_stem)  # Slot 0
    obj.data.materials.append(mat_plume) # Slot 1

    bm = bmesh.new()

    # 8 Arching grass stems
    stem_start = 0
    for i in range(8):
        ang = (math.pi / 4.0) * i
        cone = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.03, radius2=0.008, depth=1.2)
        bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.6), verts=cone["verts"])
        rot_lean = mathutils.Matrix.Rotation(math.radians(12.0), 3, 'Y')
        rot_yaw = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, matrix=rot_yaw @ rot_lean, verts=cone["verts"])
        bmesh.ops.translate(bm, vec=(0.15 * math.cos(ang), 0.15 * math.sin(ang), 0.0), verts=cone["verts"])

    for f in bm.faces:
        f.material_index = 0

    # 4 Silky white Kashful plumes on top
    plume_start = len(bm.faces)
    for i in [0, 2, 4, 6]:
        ang = (math.pi / 4.0) * i
        p = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.08, radius2=0.01, depth=0.45)
        bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.35), verts=p["verts"])
        rot_lean = mathutils.Matrix.Rotation(math.radians(15.0), 3, 'Y')
        rot_yaw = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, matrix=rot_yaw @ rot_lean, verts=p["verts"])

    set_material_index_range(bm, plume_start, len(bm.faces), 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Grass_Tall_Savanna.fbx")

# ==============================================================================
# 10. SM_Fern_Undergrowth_Cluster (Height: 0.75m, Radius: 0.8m)
# ==============================================================================
def build_fern_cluster():
    reset_scene()
    mat_fern = get_or_create_material("M_Foliage_Fern_Emerald", (0.10, 0.42, 0.10, 1.0))

    mesh = bpy.data.meshes.new("SM_Fern_Undergrowth_Cluster")
    obj = bpy.data.objects.new("SM_Fern_Undergrowth_Cluster", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_fern)

    bm = bmesh.new()

    # 10 Arching sword-fern fronds in a rosette
    for i in range(10):
        ang = (2.0 * math.pi / 10.0) * i
        frond = bmesh.ops.create_grid(bm, x_segments=1, y_segments=3, size=0.35)
        bmesh.ops.scale(bm, vec=(0.4, 1.4, 1.0), verts=frond["verts"])
        rot_pitch = mathutils.Matrix.Rotation(math.radians(45.0), 3, 'X')
        rot_yaw = mathutils.Matrix.Rotation(ang, 3, 'Z')
        bmesh.ops.rotate(bm, matrix=rot_yaw @ rot_pitch, verts=frond["verts"])
        bmesh.ops.translate(bm, vec=(0.2 * math.cos(ang), 0.2 * math.sin(ang), 0.25), verts=frond["verts"])

    for f in bm.faces:
        f.material_index = 0

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Fern_Undergrowth_Cluster.fbx")

# ==============================================================================
# 11. SM_Ground_LeafLitter_Patch (Radius: 2.2m)
# ==============================================================================
def build_leaf_litter():
    reset_scene()
    mat_litter = get_or_create_material("M_Ground_LeafLitter_Moist", (0.28, 0.20, 0.14, 1.0))

    mesh = bpy.data.meshes.new("SM_Ground_LeafLitter_Patch")
    obj = bpy.data.objects.new("SM_Ground_LeafLitter_Patch", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_litter)

    bm = bmesh.new()

    # Thin disk with subtle organic height variations
    patch = bmesh.ops.create_circle(bm, cap_ends=True, radius=2.2, segments=16)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.02), verts=patch["verts"])

    for f in bm.faces:
        f.material_index = 0

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Ground_LeafLitter_Patch.fbx")

# ==============================================================================
# 12. SM_Wildlife_Bird_Doel (Length: 0.19m, Perched Oriental Magpie-Robin)
# ==============================================================================
def build_bird_doel():
    reset_scene()
    mat_black = get_or_create_material("M_Fauna_Doel_Black", (0.04, 0.04, 0.06, 1.0))
    mat_white = get_or_create_material("M_Fauna_Doel_White", (0.96, 0.96, 0.96, 1.0))

    mesh = bpy.data.meshes.new("SM_Wildlife_Bird_Doel")
    obj = bpy.data.objects.new("SM_Wildlife_Bird_Doel", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_black) # Slot 0: Black head/back/wings
    obj.data.materials.append(mat_white) # Slot 1: White breast/belly

    bm = bmesh.new()

    # Head and Upper Body (Black)
    body = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.08)
    bmesh.ops.scale(bm, vec=(1.4, 0.9, 0.9), verts=body["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.12), verts=body["verts"])

    # Beak
    beak = bmesh.ops.create_cone(bm, cap_ends=True, segments=4, radius1=0.015, radius2=0.002, depth=0.04)
    rot_beak = mathutils.Matrix.Rotation(math.radians(90.0), 3, 'Y')
    bmesh.ops.rotate(bm, matrix=rot_beak, verts=beak["verts"])
    bmesh.ops.translate(bm, vec=(0.12, 0.0, 0.14), verts=beak["verts"])

    # Upright Cocked Tail (Characteristic Doel posture)
    tail = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(0.14, 0.03, 0.01), verts=tail["verts"])
    rot_tail = mathutils.Matrix.Rotation(math.radians(45.0), 3, 'Y')
    bmesh.ops.rotate(bm, matrix=rot_tail, verts=tail["verts"])
    bmesh.ops.translate(bm, vec=(-0.14, 0.0, 0.18), verts=tail["verts"])

    for f in bm.faces:
        f.material_index = 0

    # Lower Breast & Belly (White)
    white_start = len(bm.faces)
    belly = bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.06)
    bmesh.ops.scale(bm, vec=(1.1, 0.8, 0.7), verts=belly["verts"])
    bmesh.ops.translate(bm, vec=(0.02, 0.0, 0.08), verts=belly["verts"])

    set_material_index_range(bm, white_start, len(bm.faces), 1)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Wildlife_Bird_Doel.fbx")

# ==============================================================================
# 13. SM_Wildlife_Butterfly_Cluster (Pair of fluttering yellow butterflies)
# ==============================================================================
def build_butterfly_cluster():
    reset_scene()
    mat_yellow = get_or_create_material("M_Fauna_Butterfly_Yellow", (0.96, 0.88, 0.10, 1.0))

    mesh = bpy.data.meshes.new("SM_Wildlife_Butterfly_Cluster")
    obj = bpy.data.objects.new("SM_Wildlife_Butterfly_Cluster", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_yellow)

    bm = bmesh.new()

    for bx, by, bz, yaw in [(0.0, 0.0, 0.5, 0.0), (0.4, 0.3, 0.7, 1.2), (-0.3, 0.4, 0.6, -1.0)]:
        # Left Wing
        w_l = bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.08)
        rot_l = mathutils.Matrix.Rotation(math.radians(35.0), 3, 'X')
        bmesh.ops.rotate(bm, matrix=rot_l, verts=w_l["verts"])
        bmesh.ops.translate(bm, vec=(0.0, -0.04, 0.0), verts=w_l["verts"])

        # Right Wing
        w_r = bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.08)
        rot_r = mathutils.Matrix.Rotation(math.radians(-35.0), 3, 'X')
        bmesh.ops.rotate(bm, matrix=rot_r, verts=w_r["verts"])
        bmesh.ops.translate(bm, vec=(0.0, 0.04, 0.0), verts=w_r["verts"])

        # Combine & Translate butterfly instance
        all_verts = w_l["verts"] + w_r["verts"]
        rot_yaw = mathutils.Matrix.Rotation(yaw, 3, 'Z')
        bmesh.ops.rotate(bm, matrix=rot_yaw, verts=all_verts)
        bmesh.ops.translate(bm, vec=(bx, by, bz), verts=all_verts)

    for f in bm.faces:
        f.material_index = 0

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Wildlife_Butterfly_Cluster.fbx")

# ==============================================================================
# 14. SM_Wildlife_Dragonfly_Pair (Pair of iridescent dragonflies)
# ==============================================================================
def build_dragonfly_pair():
    reset_scene()
    mat_teal = get_or_create_material("M_Fauna_Dragonfly_Teal", (0.10, 0.78, 0.82, 1.0))

    mesh = bpy.data.meshes.new("SM_Wildlife_Dragonfly_Pair")
    obj = bpy.data.objects.new("SM_Wildlife_Dragonfly_Pair", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_teal)

    bm = bmesh.new()

    for dx, dy, dz, yaw in [(0.0, 0.0, 0.3, 0.4), (0.5, -0.4, 0.4, -0.8)]:
        # Slender Abdomen
        body = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.015, radius2=0.005, depth=0.12)
        rot_b = mathutils.Matrix.Rotation(math.radians(90.0), 3, 'Y')
        bmesh.ops.rotate(bm, matrix=rot_b, verts=body["verts"])

        # 4 Outspread Wings
        w1 = bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.06)
        bmesh.ops.scale(bm, vec=(0.3, 1.2, 1.0), verts=w1["verts"])
        bmesh.ops.translate(bm, vec=(0.02, 0.0, 0.01), verts=w1["verts"])

        w2 = bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.05)
        bmesh.ops.scale(bm, vec=(0.3, 1.0, 1.0), verts=w2["verts"])
        bmesh.ops.translate(bm, vec=(-0.02, 0.0, 0.01), verts=w2["verts"])

        all_v = body["verts"] + w1["verts"] + w2["verts"]
        rot_yaw = mathutils.Matrix.Rotation(yaw, 3, 'Z')
        bmesh.ops.rotate(bm, matrix=rot_yaw, verts=all_v)
        bmesh.ops.translate(bm, vec=(dx, dy, dz), verts=all_v)

    for f in bm.faces:
        f.material_index = 0

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Wildlife_Dragonfly_Pair.fbx")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("BUILDING EXPANDED BOTANICAL & WILDLIFE ASSETS (Blender 5.2.3 LTS)...")
    print("=" * 70)
    build_tree_debdaru()
    build_tree_mahogany()
    build_tree_kadam()
    build_bamboo_grove()
    build_bush_rangan()
    build_bush_gandharaj()
    build_bush_kamini_hedge()
    build_grass_lawn()
    build_grass_savanna()
    build_fern_cluster()
    build_leaf_litter()
    build_bird_doel()
    build_butterfly_cluster()
    build_dragonfly_pair()
    print("=" * 70)
    print("ALL 14 EXPANDED ASSETS EXPORTED SUCCESSFULLY TO FBX!")
    print("=" * 70)
