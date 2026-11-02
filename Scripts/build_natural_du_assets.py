#!/usr/bin/env python3
"""
Comprehensive Natural Dhaka University Asset Generator for Blender 5.2.3 LTS
Builds high-quality organic vegetation, campus heritage gates, authentic Dhaka vehicles,
and modern city skyline towers for SparkVision.

Assets Produced:
1. SM_Tree_Krishnachura_Natural.fbx (Delonix Regia - organic spreading canopy, flaring trunk, blossoms)
2. SM_Tree_Debdaru_Natural.fbx (Polyalthia Longifolia - weeping mast tree, dense pendulous foliage)
3. SM_Tree_Banyan_Natural.fbx (Ficus Benghalensis - buttressed trunk, hanging aerial prop roots, wide crown)
4. SM_Garden_Flowerbed_Circular.fbx (Ornamental brick-bordered circular garden with blooming shrubs)
5. SM_Garden_Flowerbed_Border.fbx (12m x 2.5m promenade flowerbed border with flowers & hedges)
6. SM_Curzon_Heritage_Gate.fbx (Indo-Saracenic brick pillars, arched wrought iron crest, carriage gates)
7. SM_Vehicle_Bus_Dhaka.fbx (Iconic Dhaka city commuter bus)
8. SM_Vehicle_CNG_AutoRickshaw.fbx (Dhaka green CNG 3-wheeler auto-rickshaw with security grill)
9. SM_Vehicle_Car_Sedan.fbx (Modern city sedan car)
10. SM_Vehicle_Cycle_Rickshaw.fbx (Traditional Dhaka cycle rickshaw with folding hood & tin plate)
11. SM_Modern_Tower_Glass.fbx (24-story glass curtain-wall corporate skyscraper)
12. SM_Modern_Building_Commercial.fbx (16-story stepped modern commercial complex)
"""

import bpy
import bmesh
import math
import os
import random

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def export_fbx(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    # Select all mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
    bpy.context.view_layer.objects.active = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )
    print(f"  ✓ Exported: {filename}")

def add_material_to_mesh(obj, mat_name):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    obj.data.materials.append(mat)
    return len(obj.data.materials) - 1

def assign_material_slot_to_faces(obj, slot_index, face_indices=None):
    if face_indices is None:
        face_indices = range(len(obj.data.polygons))
    for f_idx in face_indices:
        obj.data.polygons[f_idx].material_index = slot_index

# =============================================================================
# 1. NATURAL KRISHNACHURA TREE (Delonix Regia)
# =============================================================================
def build_krishnachura_natural():
    print("Building SM_Tree_Krishnachura_Natural...")
    clear_scene()

    # Materials
    mat_wood = bpy.data.materials.new(name="M_Bark_Tree")
    mat_bloom = bpy.data.materials.new(name="M_Foliage_Krishnachura")

    wood_parts = []
    foliage_parts = []

    # 1. Base buttress flaring roots
    root_angles = [0, 65, 130, 200, 270, 330]
    for ang_deg in root_angles:
        rad = math.radians(ang_deg)
        rx = math.cos(rad) * 1.1
        ry = math.sin(rad) * 1.1
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.45, depth=1.6,
            location=(rx * 0.5, ry * 0.5, 0.7)
        )
        r_obj = bpy.context.active_object
        tilt_x = -math.sin(rad) * 0.25
        tilt_y = math.cos(rad) * 0.25
        r_obj.rotation_euler = (tilt_x, tilt_y, rad)
        r_obj.scale = (0.6, 1.2, 1.0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        wood_parts.append(r_obj)

    # 2. Main trunk (organic taper and slight twist)
    trunk_segments = [
        # (z_bottom, z_top, r_bot, r_top, ox, oy)
        (0.0, 1.8, 0.95, 0.75, 0.05, 0.05),
        (1.8, 3.4, 0.75, 0.60, 0.15, -0.08),
        (3.4, 4.8, 0.60, 0.50, 0.10, -0.15),
    ]
    for zb, zt, rb, rt, ox, oy in trunk_segments:
        depth = zt - zb
        cz = zb + depth * 0.5
        bpy.ops.mesh.primitive_cone_add(
            vertices=12, radius1=rb, radius2=rt, depth=depth,
            location=(ox, oy, cz)
        )
        t_seg = bpy.context.active_object
        wood_parts.append(t_seg)

    # 3. Main spreading limbs (characteristic broad umbrella spread of Delonix regia)
    limb_defs = [
        # (start_pos, dir_vector, length, radius_start, radius_end, branch_angle)
        ((0.15, -0.1, 4.4), (2.8, 1.5, 2.2), 3.8, 0.38, 0.20, (0.35, -0.2, 0.6)),
        ((0.10, -0.1, 4.5), (-2.6, 1.8, 2.0), 3.7, 0.36, 0.19, (0.30, 0.35, 2.2)),
        ((0.05, -0.2, 4.3), (-1.2, -2.9, 1.8), 3.5, 0.35, 0.18, (-0.4, 0.15, -1.8)),
        ((0.20, -0.0, 4.6), (2.4, -2.2, 2.1), 3.6, 0.34, 0.17, (-0.35, -0.35, -0.8)),
        ((0.10, -0.05, 4.8), (0.2, 2.8, 2.3), 3.6, 0.32, 0.16, (0.45, 0.05, 1.5)),
        ((0.12, -0.12, 4.9), (-0.5, -0.5, 2.5), 2.8, 0.28, 0.15, (0.05, 0.05, 0.0)),
    ]

    branch_ends = []
    for (sx, sy, sz), (dx, dy, dz), length, r1, r2, (rot_x, rot_y, rot_z) in limb_defs:
        mid_x = sx + dx * 0.5
        mid_y = sy + dy * 0.5
        mid_z = sz + dz * 0.5
        bpy.ops.mesh.primitive_cone_add(
            vertices=8, radius1=r1, radius2=r2, depth=length,
            location=(mid_x, mid_y, mid_z)
        )
        limb = bpy.context.active_object
        limb.rotation_euler = (rot_x, rot_y, rot_z)
        bpy.ops.object.transform_apply(rotation=True)
        wood_parts.append(limb)

        end_pt = (sx + dx, sy + dy, sz + dz)
        branch_ends.append(end_pt)

        # Secondary sub-branch branching further outward
        sub_dx = dx * 0.6 + (random.random() - 0.5) * 1.5
        sub_dy = dy * 0.6 + (random.random() - 0.5) * 1.5
        sub_dz = dz * 0.35 + 0.4
        sub_mid_x = end_pt[0] + sub_dx * 0.5
        sub_mid_y = end_pt[1] + sub_dy * 0.5
        sub_mid_z = end_pt[2] + sub_dz * 0.5
        sub_len = math.sqrt(sub_dx**2 + sub_dy**2 + sub_dz**2)
        bpy.ops.mesh.primitive_cone_add(
            vertices=6, radius1=r2, radius2=0.08, depth=sub_len,
            location=(sub_mid_x, sub_mid_y, sub_mid_z)
        )
        sub_branch = bpy.context.active_object
        sub_branch.rotation_euler = (rot_x * 0.7, rot_y * 0.7, rot_z + 0.4)
        bpy.ops.object.transform_apply(rotation=True)
        wood_parts.append(sub_branch)
        branch_ends.append((end_pt[0] + sub_dx, end_pt[1] + sub_dy, end_pt[2] + sub_dz))

    # 4. Organic Foliage & Blossom Canopy Clusters
    # We create broad, soft billowing clusters centered over the branch ends and canopy dome
    canopy_centers = [
        # (cx, cy, cz, rad_x, rad_y, rad_z)
        (0.0, 0.0, 7.6, 4.2, 4.2, 1.8),
        (3.8, 1.8, 6.8, 3.4, 3.2, 1.6),
        (-3.6, 2.2, 6.9, 3.2, 3.4, 1.5),
        (-1.8, -3.8, 6.6, 3.5, 3.2, 1.5),
        (3.2, -3.0, 6.7, 3.3, 3.1, 1.6),
        (0.5, 3.8, 7.0, 3.2, 3.2, 1.5),
        (-4.4, -1.2, 6.5, 3.0, 2.8, 1.4),
        (4.5, -0.8, 6.6, 3.1, 2.9, 1.5),
        (2.0, 3.2, 7.2, 2.8, 2.8, 1.4),
        (-2.2, 3.0, 7.1, 2.9, 2.7, 1.4),
        (0.0, -2.4, 7.3, 3.0, 2.8, 1.5),
        # Lower outer skirt clusters
        (5.2, 1.0, 5.8, 2.5, 2.5, 1.2),
        (-4.8, 1.4, 5.9, 2.6, 2.4, 1.2),
        (2.0, -4.6, 5.7, 2.6, 2.5, 1.2),
        (-2.4, -4.4, 5.8, 2.5, 2.4, 1.2),
    ]

    for i, (cx, cy, cz, rx, ry, rz) in enumerate(canopy_centers):
        # Create an icosphere with 2 subdivisions for a natural organic rounded clump
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=2, radius=1.0, location=(cx, cy, cz)
        )
        f_obj = bpy.context.active_object
        f_obj.name = f"Krishnachura_Canopy_{i}"
        f_obj.scale = (rx, ry, rz)
        # Random rotation so every cluster has unique face angles
        f_obj.rotation_euler = (
            random.uniform(-0.3, 0.3),
            random.uniform(-0.3, 0.3),
            random.uniform(0, 6.28)
        )
        bpy.ops.object.transform_apply(rotation=True, scale=True)

        # Deform vertices slightly with random jitter for organic natural look
        mesh = f_obj.data
        for v in mesh.vertices:
            jitter = (random.random() - 0.5) * 0.15
            v.co += v.co.normalized() * jitter

        foliage_parts.append(f_obj)

    # 5. Join wood parts together
    bpy.ops.object.select_all(action='DESELECT')
    for p in wood_parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = wood_parts[0]
    bpy.ops.object.join()
    wood_joined = bpy.context.active_object
    wood_joined.name = "Trunk_And_Branches"

    # 6. Join foliage parts together
    bpy.ops.object.select_all(action='DESELECT')
    for fp in foliage_parts:
        fp.select_set(True)
    bpy.context.view_layer.objects.active = foliage_parts[0]
    bpy.ops.object.join()
    foliage_joined = bpy.context.active_object
    foliage_joined.name = "Canopy_Blossoms"

    # Add materials to parts before final join
    wood_mat_idx = add_material_to_mesh(wood_joined, "M_Bark_Tree")
    foliage_mat_idx = add_material_to_mesh(foliage_joined, "M_Foliage_Krishnachura")

    # UV unwrap both parts cleanly
    bpy.ops.object.select_all(action='DESELECT')
    wood_joined.select_set(True)
    bpy.context.view_layer.objects.active = wood_joined
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    foliage_joined.select_set(True)
    bpy.context.view_layer.objects.active = foliage_joined
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Join into single static mesh with 2 distinct material slots
    # Slot 0: M_Bark_Tree, Slot 1: M_Foliage_Krishnachura
    wood_joined.data.materials.append(mat_bloom)
    # Ensure wood faces have slot 0
    assign_material_slot_to_faces(wood_joined, 0)
    # Foliage joined has slot 1
    foliage_joined.data.materials.clear()
    foliage_joined.data.materials.append(mat_wood)
    foliage_joined.data.materials.append(mat_bloom)
    assign_material_slot_to_faces(foliage_joined, 1)

    bpy.ops.object.select_all(action='DESELECT')
    wood_joined.select_set(True)
    foliage_joined.select_set(True)
    bpy.context.view_layer.objects.active = wood_joined
    bpy.ops.object.join()
    final_tree = bpy.context.active_object
    final_tree.name = "SM_Tree_Krishnachura_Natural"

    export_fbx("SM_Tree_Krishnachura_Natural.fbx")

# =============================================================================
# 2. NATURAL WEEPING DEBDARU TREE (Polyalthia Longifolia)
# =============================================================================
def build_debdaru_natural():
    print("Building SM_Tree_Debdaru_Natural...")
    clear_scene()

    mat_wood = bpy.data.materials.new(name="M_Bark_Tree")
    mat_leaves = bpy.data.materials.new(name="M_Foliage_Debdaru_Dark")

    wood_parts = []
    foliage_parts = []

    # 1. Central slender mast trunk (16 meters tall)
    # Tapering from radius 0.40 at base to 0.08 at apex
    trunk_segments = [
        (0.0, 3.0, 0.42, 0.35),
        (3.0, 7.0, 0.35, 0.28),
        (7.0, 11.5, 0.28, 0.20),
        (11.5, 16.0, 0.20, 0.08),
    ]
    for zb, zt, rb, rt in trunk_segments:
        depth = zt - zb
        cz = zb + depth * 0.5
        bpy.ops.mesh.primitive_cone_add(
            vertices=10, radius1=rb, radius2=rt, depth=depth,
            location=(0, 0, cz)
        )
        wood_parts.append(bpy.context.active_object)

    # 2. Weeping pendulous foliage tiers extending down to near-ground level (Z=1.2m)
    # Debdaru has a dense, weeping columnar/spire profile:
    # Starts narrow at bottom (Z=1.2, r=1.4), widens in lower-middle (Z=4.5, r=2.4),
    # then tapers gradually to apex (Z=16.5, r=0.2).
    tier_defs = [
        # (cz, height, radius_x, radius_y)
        (1.8, 1.6, 1.4, 1.3),
        (3.0, 1.8, 1.9, 1.8),
        (4.5, 2.0, 2.3, 2.2),
        (6.0, 2.0, 2.2, 2.1),
        (7.5, 2.0, 2.0, 1.9),
        (9.0, 2.0, 1.8, 1.7),
        (10.5, 1.9, 1.5, 1.4),
        (12.0, 1.8, 1.2, 1.2),
        (13.5, 1.7, 0.9, 0.85),
        (14.8, 1.5, 0.6, 0.55),
        (15.8, 1.4, 0.35, 0.35),
    ]

    for idx, (cz, h, rx, ry) in enumerate(tier_defs):
        # We create 4-6 drooping lobes per tier distributed around the perimeter
        num_lobes = 6 if cz < 10.0 else 4
        for lobe_i in range(num_lobes):
            ang = (lobe_i / num_lobes) * 2 * math.pi + (idx * 0.6)
            dist = (rx + ry) * 0.35
            lx = math.cos(ang) * dist
            ly = math.sin(ang) * dist
            # Drooping elongated weeping cluster
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8, radius=rx * 0.48, depth=h * 1.15,
                location=(lx, ly, cz - h * 0.15)
            )
            lobe = bpy.context.active_object
            lobe.name = f"Debdaru_Lobe_{idx}_{lobe_i}"
            # Tilt outward and downward
            tilt = 0.15 * (1.0 - cz / 17.0)
            lobe.rotation_euler = (-math.sin(ang) * tilt, math.cos(ang) * tilt, ang)
            lobe.scale = (0.9, 1.1, 1.0)
            bpy.ops.object.transform_apply(rotation=True, scale=True)
            foliage_parts.append(lobe)

        # Central dense fill core for each tier
        bpy.ops.mesh.primitive_cone_add(
            vertices=10, radius1=rx * 0.85, radius2=rx * 0.45, depth=h * 1.05,
            location=(0, 0, cz)
        )
        core = bpy.context.active_object
        foliage_parts.append(core)

    # Join wood
    bpy.ops.object.select_all(action='DESELECT')
    for p in wood_parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = wood_parts[0]
    bpy.ops.object.join()
    wood_joined = bpy.context.active_object
    wood_joined.name = "Debdaru_Trunk"

    # Join foliage
    bpy.ops.object.select_all(action='DESELECT')
    for p in foliage_parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = foliage_parts[0]
    bpy.ops.object.join()
    foliage_joined = bpy.context.active_object
    foliage_joined.name = "Debdaru_Foliage"

    # UV Unwrap
    for obj in [wood_joined, foliage_joined]:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

    # Setup materials: Slot 0: Wood, Slot 1: Foliage
    wood_joined.data.materials.append(mat_wood)
    wood_joined.data.materials.append(mat_leaves)
    assign_material_slot_to_faces(wood_joined, 0)

    foliage_joined.data.materials.append(mat_wood)
    foliage_joined.data.materials.append(mat_leaves)
    assign_material_slot_to_faces(foliage_joined, 1)

    bpy.ops.object.select_all(action='DESELECT')
    wood_joined.select_set(True)
    foliage_joined.select_set(True)
    bpy.context.view_layer.objects.active = wood_joined
    bpy.ops.object.join()
    final_tree = bpy.context.active_object
    final_tree.name = "SM_Tree_Debdaru_Natural"

    export_fbx("SM_Tree_Debdaru_Natural.fbx")

# =============================================================================
# 3. NATURAL BANYAN TREE (Ficus Benghalensis)
# =============================================================================
def build_banyan_natural():
    print("Building SM_Tree_Banyan_Natural...")
    clear_scene()

    mat_wood = bpy.data.materials.new(name="M_Bark_Tree")
    mat_leaves = bpy.data.materials.new(name="M_Foliage_Banyan_Leaf")

    wood_parts = []
    foliage_parts = []

    # 1. Massive central composite trunk with buttressed root flares
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1.6, depth=3.5, location=(0, 0, 1.75))
    main_trunk = bpy.context.active_object
    wood_parts.append(main_trunk)

    # 4 corner trunk buttresses
    for bx, by in [(1.1, 1.1), (-1.1, 1.1), (1.1, -1.1), (-1.1, -1.1)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.75, depth=2.8, location=(bx, by, 1.4))
        wood_parts.append(bpy.context.active_object)

    # 2. Spreading massive horizontal limbs
    limb_angles = [0, 60, 120, 180, 240, 300]
    outer_points = []
    for ang_deg in limb_angles:
        rad = math.radians(ang_deg)
        dist = 7.5
        lx = math.cos(rad) * dist
        ly = math.sin(rad) * dist
        mid_x = lx * 0.5
        mid_y = ly * 0.5
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.6, depth=dist, location=(mid_x, mid_y, 4.2))
        limb = bpy.context.active_object
        limb.rotation_euler = (0, math.radians(85), rad)
        bpy.ops.object.transform_apply(rotation=True)
        wood_parts.append(limb)
        outer_points.append((lx, ly, 4.5))

        # 3. Aerial Prop Roots dropping to ground from each limb
        # 2 prop roots per limb at different distances
        for r_dist in [3.5, 6.2]:
            px = math.cos(rad) * r_dist + (random.random() - 0.5) * 0.4
            py = math.sin(rad) * r_dist + (random.random() - 0.5) * 0.4
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22, depth=4.5, location=(px, py, 2.25))
            root_col = bpy.context.active_object
            root_col.rotation_euler = (random.uniform(-0.06, 0.06), random.uniform(-0.06, 0.06), 0)
            bpy.ops.object.transform_apply(rotation=True)
            wood_parts.append(root_col)

    # 4. Dense broad umbrella canopy (22m diameter, lush billowing foliage)
    canopy_specs = [
        # (cx, cy, cz, rx, ry, rz)
        (0.0, 0.0, 8.5, 6.5, 6.5, 2.8),
        (5.5, 3.2, 7.5, 5.0, 4.8, 2.4),
        (-5.5, 3.2, 7.5, 4.8, 5.0, 2.4),
        (0.0, 6.5, 7.6, 5.0, 4.5, 2.3),
        (0.0, -6.5, 7.4, 4.8, 4.6, 2.4),
        (5.5, -3.2, 7.3, 4.7, 4.8, 2.3),
        (-5.5, -3.2, 7.4, 4.9, 4.7, 2.3),
        # Outer peripheral lower leaf skirts
        (8.5, 0.0, 6.2, 4.0, 4.0, 1.8),
        (-8.5, 0.0, 6.2, 4.0, 4.0, 1.8),
        (0.0, 8.5, 6.2, 4.0, 4.0, 1.8),
        (0.0, -8.5, 6.0, 4.0, 4.0, 1.8),
    ]

    for cx, cy, cz, rx, ry, rz in canopy_specs:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, location=(cx, cy, cz))
        f_obj = bpy.context.active_object
        f_obj.scale = (rx, ry, rz)
        f_obj.rotation_euler = (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(0, 6.28))
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        foliage_parts.append(f_obj)

    # Join wood
    bpy.ops.object.select_all(action='DESELECT')
    for p in wood_parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = wood_parts[0]
    bpy.ops.object.join()
    wood_joined = bpy.context.active_object

    # Join foliage
    bpy.ops.object.select_all(action='DESELECT')
    for p in foliage_parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = foliage_parts[0]
    bpy.ops.object.join()
    foliage_joined = bpy.context.active_object

    # UV Unwrap
    for obj in [wood_joined, foliage_joined]:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

    wood_joined.data.materials.append(mat_wood)
    wood_joined.data.materials.append(mat_leaves)
    assign_material_slot_to_faces(wood_joined, 0)

    foliage_joined.data.materials.append(mat_wood)
    foliage_joined.data.materials.append(mat_leaves)
    assign_material_slot_to_faces(foliage_joined, 1)

    bpy.ops.object.select_all(action='DESELECT')
    wood_joined.select_set(True)
    foliage_joined.select_set(True)
    bpy.context.view_layer.objects.active = wood_joined
    bpy.ops.object.join()
    final_tree = bpy.context.active_object
    final_tree.name = "SM_Tree_Banyan_Natural"

    export_fbx("SM_Tree_Banyan_Natural.fbx")

# =============================================================================
# 4. FLOWER BEDS / BAGAN PROPS
# =============================================================================
def build_flowerbed_circular():
    print("Building SM_Garden_Flowerbed_Circular...")
    clear_scene()

    mat_brick = bpy.data.materials.new(name="MI_Curzon_Brick")
    mat_soil = bpy.data.materials.new(name="MI_Ground_Grass")
    mat_hedge = bpy.data.materials.new(name="MI_Curzon_Hedge")
    mat_flower = bpy.data.materials.new(name="MI_Flower_Rangan_Scarlet")

    # 1. Circular brick retaining curb (diameter 6m, radius 3m, 0.35m height)
    num_bricks = 36
    brick_parts = []
    for i in range(num_bricks):
        ang = (i / num_bricks) * 2 * math.pi
        bx = math.cos(ang) * 3.0
        by = math.sin(ang) * 3.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, 0.175))
        b = bpy.context.active_object
        b.scale = (0.28, 0.52, 0.35)
        b.rotation_euler = (0, 0, ang + math.pi * 0.5)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        brick_parts.append(b)

    # 2. Rich dark soil mound (curved dome)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=2.95, depth=0.30, location=(0, 0, 0.15))
    soil = bpy.context.active_object
    soil.scale = (1.0, 1.0, 0.9)
    bpy.ops.object.transform_apply(scale=True)

    # 3. Outer ring of manicured green shrubs with flowers (radius 2.3m)
    shrub_parts = []
    flower_parts = []
    for i in range(16):
        ang = (i / 16) * 2 * math.pi
        sx = math.cos(ang) * 2.2
        sy = math.sin(ang) * 2.2
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.45, location=(sx, sy, 0.45))
        shrub = bpy.context.active_object
        shrub.scale = (1.0, 1.0, 0.75)
        bpy.ops.object.transform_apply(scale=True)
        shrub_parts.append(shrub)

        # Flower blossoms on top
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.25, depth=0.08, location=(sx, sy, 0.72))
        fl = bpy.context.active_object
        flower_parts.append(fl)

    # 4. Inner ring of vibrant flowers (radius 1.2m)
    for i in range(8):
        ang = (i / 8) * 2 * math.pi + 0.3
        sx = math.cos(ang) * 1.2
        sy = math.sin(ang) * 1.2
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.40, location=(sx, sy, 0.55))
        shrub = bpy.context.active_object
        shrub.scale = (1.0, 1.0, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        shrub_parts.append(shrub)

        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.28, depth=0.08, location=(sx, sy, 0.85))
        fl = bpy.context.active_object
        flower_parts.append(fl)

    # 5. Center ornamental focal shrub
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.65, location=(0, 0, 0.75))
    center_shrub = bpy.context.active_object
    center_shrub.scale = (1.0, 1.0, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    shrub_parts.append(center_shrub)

    bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.45, depth=0.10, location=(0, 0, 1.35))
    flower_parts.append(bpy.context.active_object)

    # Join each group
    # Bricks
    bpy.ops.object.select_all(action='DESELECT')
    for b in brick_parts:
        b.select_set(True)
    bpy.context.view_layer.objects.active = brick_parts[0]
    bpy.ops.object.join()
    bricks_obj = bpy.context.active_object

    # Shrubs
    bpy.ops.object.select_all(action='DESELECT')
    for s in shrub_parts:
        s.select_set(True)
    bpy.context.view_layer.objects.active = shrub_parts[0]
    bpy.ops.object.join()
    shrubs_obj = bpy.context.active_object

    # Flowers
    bpy.ops.object.select_all(action='DESELECT')
    for f in flower_parts:
        f.select_set(True)
    bpy.context.view_layer.objects.active = flower_parts[0]
    bpy.ops.object.join()
    flowers_obj = bpy.context.active_object

    # Unwrap all
    for obj in [bricks_obj, soil, shrubs_obj, flowers_obj]:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

    # Assign slots: 0: Brick, 1: Soil, 2: Hedge, 3: Flower
    all_objs = [bricks_obj, soil, shrubs_obj, flowers_obj]
    for obj in all_objs:
        obj.data.materials.append(mat_brick)
        obj.data.materials.append(mat_soil)
        obj.data.materials.append(mat_hedge)
        obj.data.materials.append(mat_flower)

    assign_material_slot_to_faces(bricks_obj, 0)
    assign_material_slot_to_faces(soil, 1)
    assign_material_slot_to_faces(shrubs_obj, 2)
    assign_material_slot_to_faces(flowers_obj, 3)

    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = bricks_obj
    bpy.ops.object.join()
    final_bed = bpy.context.active_object
    final_bed.name = "SM_Garden_Flowerbed_Circular"

    export_fbx("SM_Garden_Flowerbed_Circular.fbx")

def build_flowerbed_border():
    print("Building SM_Garden_Flowerbed_Border...")
    clear_scene()

    mat_brick = bpy.data.materials.new(name="MI_Curzon_Brick")
    mat_soil = bpy.data.materials.new(name="MI_Ground_Grass")
    mat_hedge = bpy.data.materials.new(name="MI_Curzon_Hedge")
    mat_flower = bpy.data.materials.new(name="MI_Flower_Rangan_Scarlet")

    # 12m length x 2.4m width rectangular flowerbed with brick curb
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.15))
    curb = bpy.context.active_object
    curb.scale = (12.0, 2.4, 0.30)
    bpy.ops.object.transform_apply(scale=True)

    # Soil fill
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.22))
    soil = bpy.context.active_object
    soil.scale = (11.6, 2.0, 0.25)
    bpy.ops.object.transform_apply(scale=True)

    # Shrub clusters along the length
    shrub_parts = []
    flower_parts = []
    for x in range(-5, 6, 2):
        for y in [-0.5, 0.5]:
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.45, location=(x + random.uniform(-0.15, 0.15), y, 0.45))
            sh = bpy.context.active_object
            shrub_parts.append(sh)

            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.28, depth=0.08, location=(x, y, 0.75))
            fl = bpy.context.active_object
            flower_parts.append(fl)

    # Join shrubs & flowers
    bpy.ops.object.select_all(action='DESELECT')
    for s in shrub_parts:
        s.select_set(True)
    bpy.context.view_layer.objects.active = shrub_parts[0]
    bpy.ops.object.join()
    shrubs_obj = bpy.context.active_object

    bpy.ops.object.select_all(action='DESELECT')
    for f in flower_parts:
        f.select_set(True)
    bpy.context.view_layer.objects.active = flower_parts[0]
    bpy.ops.object.join()
    flowers_obj = bpy.context.active_object

    for obj in [curb, soil, shrubs_obj, flowers_obj]:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

    all_objs = [curb, soil, shrubs_obj, flowers_obj]
    for obj in all_objs:
        obj.data.materials.append(mat_brick)
        obj.data.materials.append(mat_soil)
        obj.data.materials.append(mat_hedge)
        obj.data.materials.append(mat_flower)

    assign_material_slot_to_faces(curb, 0)
    assign_material_slot_to_faces(soil, 1)
    assign_material_slot_to_faces(shrubs_obj, 2)
    assign_material_slot_to_faces(flowers_obj, 3)

    bpy.ops.object.select_all(action='DESELECT')
    for obj in all_objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = curb
    bpy.ops.object.join()
    final_border = bpy.context.active_object
    final_border.name = "SM_Garden_Flowerbed_Border"

    export_fbx("SM_Garden_Flowerbed_Border.fbx")

# =============================================================================
# 5. AUTHENTIC CURZON / MIR JUMLA HERITAGE CAMPUS GATE
# =============================================================================
def build_curzon_heritage_gate():
    print("Building SM_Curzon_Heritage_Gate...")
    clear_scene()

    mat_brick = bpy.data.materials.new(name="MI_Curzon_Brick")
    mat_stone = bpy.data.materials.new(name="MI_Curzon_Sandstone")
    mat_iron = bpy.data.materials.new(name="MI_Curzon_CastIron")
    mat_brass = bpy.data.materials.new(name="MI_Curzon_Brass")

    brick_parts = []
    stone_parts = []
    iron_parts = []
    brass_parts = []

    # Main Gateway dimensions:
    # 2 Central Monumental Pillars at X = -5.0m and X = +5.0m (10m central vehicular span)
    # 2 Outer Wicket Pillars at X = -8.5m and X = +8.5m (3m pedestrian span on each side)
    # Total width: 20m, Main pillar height: 8.5m

    pillar_xs = [-5.0, 5.0]
    for px in pillar_xs:
        # Base Stone Plinth (2.4m x 2.4m x 0.8m)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0, 0.4))
        b_plinth = bpy.context.active_object
        b_plinth.scale = (2.4, 2.4, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        stone_parts.append(b_plinth)

        # Red Brick Main Shaft (2.0m x 2.0m x 6.0m)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0, 3.8))
        shaft = bpy.context.active_object
        shaft.scale = (2.0, 2.0, 6.0)
        bpy.ops.object.transform_apply(scale=True)
        brick_parts.append(shaft)

        # Decorative Sandstone Cornice / Cap (2.3m x 2.3m x 0.6m)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0, 7.1))
        cap = bpy.context.active_object
        cap.scale = (2.3, 2.3, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        stone_parts.append(cap)

        # Indo-Saracenic Dome / Chattri Finial (octagonal kalash)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.9, depth=1.0, location=(px, 0, 7.9))
        dome = bpy.context.active_object
        stone_parts.append(dome)

        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.45, radius2=0.05, depth=0.8, location=(px, 0, 8.8))
        finial = bpy.context.active_object
        brass_parts.append(finial)

    # Flanking Wicket Pillars (-8.5m and +8.5m)
    wicket_xs = [-8.5, 8.5]
    for wx in wicket_xs:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, 0, 0.3))
        w_plinth = bpy.context.active_object
        w_plinth.scale = (1.6, 1.6, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        stone_parts.append(w_plinth)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, 0, 2.8))
        w_shaft = bpy.context.active_object
        w_shaft.scale = (1.4, 1.4, 4.4)
        bpy.ops.object.transform_apply(scale=True)
        brick_parts.append(w_shaft)

        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, 0, 5.25))
        w_cap = bpy.context.active_object
        w_cap.scale = (1.6, 1.6, 0.5)
        bpy.ops.object.transform_apply(scale=True)
        stone_parts.append(w_cap)

        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.35, radius2=0.05, depth=0.6, location=(wx, 0, 5.8))
        brass_parts.append(bpy.context.active_object)

    # Low Perimeter Wing Walls with spear railings (-13m to -8.5m and +8.5m to +13m)
    for wx_start, wx_end in [(-13.0, -8.5), (8.5, 13.0)]:
        cx = (wx_start + wx_end) * 0.5
        w_len = abs(wx_end - wx_start)
        # Brick dwarf wall
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, 0, 0.6))
        dwarf = bpy.context.active_object
        dwarf.scale = (w_len, 0.5, 1.2)
        bpy.ops.object.transform_apply(scale=True)
        brick_parts.append(dwarf)

        # Stone wall coping
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, 0, 1.25))
        coping = bpy.context.active_object
        coping.scale = (w_len + 0.1, 0.6, 0.1)
        bpy.ops.object.transform_apply(scale=True)
        stone_parts.append(coping)

        # Iron spear railings atop wall
        num_spears = int(w_len * 4)
        for s_i in range(num_spears):
            sx = wx_start + (s_i + 0.5) * (w_len / num_spears)
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.03, depth=1.2, location=(sx, 0, 1.9))
            iron_parts.append(bpy.context.active_object)
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.06, radius2=0.0, depth=0.18, location=(sx, 0, 2.55))
            brass_parts.append(bpy.context.active_object)

    # Ornate Overhead Wrought Iron Gateway Arch spanning between main pillars (X: -5m to +5m)
    # Curved arch frame
    arch_pts = 16
    for i in range(arch_pts):
        t0 = (i / arch_pts) * math.pi
        t1 = ((i + 1) / arch_pts) * math.pi
        x0 = math.cos(t0) * 5.0
        z0 = 6.8 + math.sin(t0) * 2.6
        x1 = math.cos(t1) * 5.0
        z1 = 6.8 + math.sin(t1) * 2.6
        mid_x = (x0 + x1) * 0.5
        mid_z = (z0 + z1) * 0.5
        seg_len = math.sqrt((x1 - x0)**2 + (z1 - z0)**2)
        ang = math.atan2(z1 - z0, x1 - x0)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mid_x, 0, mid_z))
        arch_seg = bpy.context.active_object
        arch_seg.scale = (seg_len, 0.12, 0.18)
        arch_seg.rotation_euler = (0, -ang, 0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        iron_parts.append(arch_seg)

    # Central University of Dhaka Crest Medallion on overhead arch
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.75, depth=0.15, location=(0, 0, 9.4))
    medallion = bpy.context.active_object
    medallion.rotation_euler = (math.pi * 0.5, 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    brass_parts.append(medallion)

    # Double-Leaf Wrought Iron Carriage Gates (closed/latched across the 10m road)
    # Left leaf: X = -4.9m to -0.05m; Right leaf: X = +0.05m to +4.9m
    for gate_x_min, gate_x_max in [(-4.9, -0.05), (0.05, 4.9)]:
        g_width = gate_x_max - gate_x_min
        g_mid = (gate_x_min + gate_x_max) * 0.5
        # Frame
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(g_mid, 0, 2.0))
        g_frame = bpy.context.active_object
        g_frame.scale = (g_width, 0.08, 3.8)
        bpy.ops.object.transform_apply(scale=True)
        iron_parts.append(g_frame)

        # Vertical iron pickets
        num_pickets = 14
        for p_i in range(num_pickets):
            px = gate_x_min + (p_i + 0.5) * (g_width / num_pickets)
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.035, depth=3.8, location=(px, 0, 2.0))
            iron_parts.append(bpy.context.active_object)
            # Spear finial
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.07, radius2=0.0, depth=0.22, location=(px, 0, 4.0))
            brass_parts.append(bpy.context.active_object)

    # Pedestrian Wicket Gates (-8.4m to -5.1m and +5.1m to +8.4m)
    for wx_min, wx_max in [(-8.4, -5.1), (5.1, 8.4)]:
        w_width = wx_max - wx_min
        w_mid = (wx_min + wx_max) * 0.5
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(w_mid, 0, 1.6))
        w_gate = bpy.context.active_object
        w_gate.scale = (w_width, 0.06, 3.0)
        bpy.ops.object.transform_apply(scale=True)
        iron_parts.append(w_gate)

    # Combine by material groups
    groups = [
        (brick_parts, mat_brick, 0, "Brick_Parts"),
        (stone_parts, mat_stone, 1, "Stone_Parts"),
        (iron_parts, mat_iron, 2, "Iron_Parts"),
        (brass_parts, mat_brass, 3, "Brass_Parts"),
    ]

    joined_objs = []
    for parts_list, mat, slot_idx, g_name in groups:
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts_list:
            p.select_set(True)
        bpy.context.view_layer.objects.active = parts_list[0]
        bpy.ops.object.join()
        g_obj = bpy.context.active_object
        g_obj.name = g_name

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

        joined_objs.append((g_obj, slot_idx))

    # Add all 4 materials to all joined objs and set appropriate slot
    for g_obj, slot_idx in joined_objs:
        g_obj.data.materials.append(mat_brick)
        g_obj.data.materials.append(mat_stone)
        g_obj.data.materials.append(mat_iron)
        g_obj.data.materials.append(mat_brass)
        assign_material_slot_to_faces(g_obj, slot_idx)

    # Join everything into final static mesh
    bpy.ops.object.select_all(action='DESELECT')
    for g_obj, _ in joined_objs:
        g_obj.select_set(True)
    bpy.context.view_layer.objects.active = joined_objs[0][0]
    bpy.ops.object.join()
    final_gate = bpy.context.active_object
    final_gate.name = "SM_Curzon_Heritage_Gate"

    export_fbx("SM_Curzon_Heritage_Gate.fbx")

# =============================================================================
# 6. DHAKA CITY TRANSIT VEHICLES (Outer Highway)
# =============================================================================
def build_vehicle_bus_dhaka():
    print("Building SM_Vehicle_Bus_Dhaka...")
    clear_scene()

    mat_paint = bpy.data.materials.new(name="MI_Curzon_Sandstone")   # Colorful body
    mat_glass = bpy.data.materials.new(name="MI_Curzon_Glass")       # Windows
    mat_metal = bpy.data.materials.new(name="MI_Curzon_Brass")       # Trim & Bumpers
    mat_rubber = bpy.data.materials.new(name="MI_Curzon_CastIron")   # Tires

    paint_parts = []
    glass_parts = []
    metal_parts = []
    rubber_parts = []

    # Bus Dimensions: Length 10.5m, Width 2.6m, Height 3.2m
    # 1. Main Chassis & Lower Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.2))
    body_lower = bpy.context.active_object
    body_lower.scale = (10.5, 2.6, 1.4)
    bpy.ops.object.transform_apply(scale=True)
    paint_parts.append(body_lower)

    # 2. Upper Roof & Cab
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 2.8))
    roof = bpy.context.active_object
    roof.scale = (10.4, 2.55, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    paint_parts.append(roof)

    # 3. Windshield (Front & Rear)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(5.15, 0, 2.1))
    front_windshield = bpy.context.active_object
    front_windshield.scale = (0.2, 2.3, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    glass_parts.append(front_windshield)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-5.15, 0, 2.1))
    rear_glass = bpy.context.active_object
    rear_glass.scale = (0.2, 2.3, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    glass_parts.append(rear_glass)

    # 4. Side Passenger Windows (5 per side)
    for side_y in [-1.31, 1.31]:
        for win_x in [-3.8, -2.0, -0.2, 1.6, 3.4]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(win_x, side_y, 2.1))
            win = bpy.context.active_object
            win.scale = (1.4, 0.08, 0.9)
            bpy.ops.object.transform_apply(scale=True)
            glass_parts.append(win)

    # 5. Roof Luggage Rack (iconic Dhaka bus rack)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 3.15))
    rack = bpy.context.active_object
    rack.scale = (8.0, 2.2, 0.25)
    bpy.ops.object.transform_apply(scale=True)
    metal_parts.append(rack)

    # 6. Heavy Bumpers & Front Grill
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(5.35, 0, 0.6))
    front_bumper = bpy.context.active_object
    front_bumper.scale = (0.35, 2.7, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    metal_parts.append(front_bumper)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-5.35, 0, 0.6))
    rear_bumper = bpy.context.active_object
    rear_bumper.scale = (0.35, 2.7, 0.4)
    bpy.ops.object.transform_apply(scale=True)
    metal_parts.append(rear_bumper)

    # 7. Wheels & Tires (4 wheel positions: front pair at X=3.2m, rear duals at X=-3.0m)
    for wx in [3.2, -3.0]:
        for wy in [-1.25, 1.25]:
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.55, depth=0.35, location=(wx, wy, 0.55))
            tire = bpy.context.active_object
            tire.rotation_euler = (math.pi * 0.5, 0, 0)
            bpy.ops.object.transform_apply(rotation=True)
            rubber_parts.append(tire)

    # Join and assign materials
    groups = [
        (paint_parts, mat_paint, 0),
        (glass_parts, mat_glass, 1),
        (metal_parts, mat_metal, 2),
        (rubber_parts, mat_rubber, 3),
    ]

    joined_list = []
    for parts, mat, slot_idx in groups:
        if not parts:
            continue
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            p.select_set(True)
        bpy.context.view_layer.objects.active = parts[0]
        if len(parts) > 1:
            bpy.ops.object.join()
        g_obj = bpy.context.active_object

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

        joined_list.append((g_obj, slot_idx))

    for g_obj, slot_idx in joined_list:
        g_obj.data.materials.append(mat_paint)
        g_obj.data.materials.append(mat_glass)
        g_obj.data.materials.append(mat_metal)
        g_obj.data.materials.append(mat_rubber)
        assign_material_slot_to_faces(g_obj, slot_idx)

    bpy.ops.object.select_all(action='DESELECT')
    for g_obj, _ in joined_list:
        g_obj.select_set(True)
    bpy.context.view_layer.objects.active = joined_list[0][0]
    bpy.ops.object.join()
    final_bus = bpy.context.active_object
    final_bus.name = "SM_Vehicle_Bus_Dhaka"

    export_fbx("SM_Vehicle_Bus_Dhaka.fbx")

def build_vehicle_cng():
    print("Building SM_Vehicle_CNG_AutoRickshaw...")
    clear_scene()

    mat_green = bpy.data.materials.new(name="MI_Curzon_Hedge")         # Green CNG paint
    mat_yellow = bpy.data.materials.new(name="MI_Curzon_Sandstone")    # Yellow canvas roof
    mat_cage = bpy.data.materials.new(name="MI_Curzon_CastIron")       # Black security mesh cage
    mat_wheel = bpy.data.materials.new(name="MI_Curzon_WoodDark")      # Tires & interior

    green_parts = []
    yellow_parts = []
    cage_parts = []
    wheel_parts = []

    # CNG Dimensions: Length 2.7m, Width 1.35m, Height 1.75m
    # 1. Lower body tub (painted green)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.45))
    tub = bpy.context.active_object
    tub.scale = (2.6, 1.35, 0.6)
    bpy.ops.object.transform_apply(scale=True)
    green_parts.append(tub)

    # Front curved nose / cowl
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.65, depth=0.6, location=(1.05, 0, 0.45))
    nose = bpy.context.active_object
    nose.scale = (0.8, 1.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    green_parts.append(nose)

    # 2. Tubular roll-cage frame & security mesh (black iron)
    # Side protective wire mesh grills
    for side_y in [-0.68, 0.68]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.1, side_y, 1.1))
        cage = bpy.context.active_object
        cage.scale = (1.5, 0.05, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        cage_parts.append(cage)

    # Front windshield frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.85, 0, 1.15))
    ws_frame = bpy.context.active_object
    ws_frame.scale = (0.08, 1.25, 0.7)
    bpy.ops.object.transform_apply(scale=True)
    cage_parts.append(ws_frame)

    # 3. Yellow arched canopy roof
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.05, 0, 1.62))
    roof = bpy.context.active_object
    roof.scale = (2.4, 1.38, 0.22)
    bpy.ops.object.transform_apply(scale=True)
    yellow_parts.append(roof)

    # 4. Three Wheels (1 front center, 2 rear sides)
    # Front wheel
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.25, depth=0.15, location=(1.1, 0, 0.25))
    fw = bpy.context.active_object
    fw.rotation_euler = (math.pi * 0.5, 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    wheel_parts.append(fw)

    # Rear wheels
    for ry in [-0.62, 0.62]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.28, depth=0.18, location=(-0.85, ry, 0.28))
        rw = bpy.context.active_object
        rw.rotation_euler = (math.pi * 0.5, 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        wheel_parts.append(rw)

    # Combine & UV
    groups = [
        (green_parts, mat_green, 0),
        (yellow_parts, mat_yellow, 1),
        (cage_parts, mat_cage, 2),
        (wheel_parts, mat_wheel, 3),
    ]

    joined_list = []
    for parts, mat, slot_idx in groups:
        if not parts:
            continue
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            p.select_set(True)
        bpy.context.view_layer.objects.active = parts[0]
        if len(parts) > 1:
            bpy.ops.object.join()
        g_obj = bpy.context.active_object

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

        joined_list.append((g_obj, slot_idx))

    for g_obj, slot_idx in joined_list:
        g_obj.data.materials.append(mat_green)
        g_obj.data.materials.append(mat_yellow)
        g_obj.data.materials.append(mat_cage)
        g_obj.data.materials.append(mat_wheel)
        assign_material_slot_to_faces(g_obj, slot_idx)

    bpy.ops.object.select_all(action='DESELECT')
    for g_obj, _ in joined_list:
        g_obj.select_set(True)
    bpy.context.view_layer.objects.active = joined_list[0][0]
    bpy.ops.object.join()
    final_cng = bpy.context.active_object
    final_cng.name = "SM_Vehicle_CNG_AutoRickshaw"

    export_fbx("SM_Vehicle_CNG_AutoRickshaw.fbx")

def build_vehicle_sedan():
    print("Building SM_Vehicle_Car_Sedan...")
    clear_scene()

    mat_body = bpy.data.materials.new(name="MI_Hero_Modern")        # Metallic white/silver body
    mat_glass = bpy.data.materials.new(name="MI_Curzon_Glass")       # Tinted windows
    mat_trim = bpy.data.materials.new(name="MI_Curzon_CastIron")     # Black trim/grille
    mat_wheel = bpy.data.materials.new(name="MI_Curzon_WoodDark")    # Wheels

    body_parts = []
    glass_parts = []
    trim_parts = []
    wheel_parts = []

    # Sedan: Length 4.6m, Width 1.8m, Height 1.45m
    # Lower chassis
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.45))
    chassis = bpy.context.active_object
    chassis.scale = (4.6, 1.8, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    body_parts.append(chassis)

    # Cabin Greenhouse (roof and pillars)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.15, 0, 1.05))
    cabin = bpy.context.active_object
    cabin.scale = (2.3, 1.5, 0.65)
    bpy.ops.object.transform_apply(scale=True)
    glass_parts.append(cabin)

    # Roof cap
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.15, 0, 1.4))
    roof = bpy.context.active_object
    roof.scale = (2.1, 1.45, 0.1)
    bpy.ops.object.transform_apply(scale=True)
    body_parts.append(roof)

    # Front Grille & Lights
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(2.32, 0, 0.45))
    grille = bpy.context.active_object
    grille.scale = (0.1, 1.4, 0.35)
    bpy.ops.object.transform_apply(scale=True)
    trim_parts.append(grille)

    # 4 Wheels
    for wx in [1.4, -1.4]:
        for wy in [-0.85, 0.85]:
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.33, depth=0.22, location=(wx, wy, 0.33))
            w = bpy.context.active_object
            w.rotation_euler = (math.pi * 0.5, 0, 0)
            bpy.ops.object.transform_apply(rotation=True)
            wheel_parts.append(w)

    groups = [
        (body_parts, mat_body, 0),
        (glass_parts, mat_glass, 1),
        (trim_parts, mat_trim, 2),
        (wheel_parts, mat_wheel, 3),
    ]

    joined_list = []
    for parts, mat, slot_idx in groups:
        if not parts:
            continue
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            p.select_set(True)
        bpy.context.view_layer.objects.active = parts[0]
        if len(parts) > 1:
            bpy.ops.object.join()
        g_obj = bpy.context.active_object

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

        joined_list.append((g_obj, slot_idx))

    for g_obj, slot_idx in joined_list:
        g_obj.data.materials.append(mat_body)
        g_obj.data.materials.append(mat_glass)
        g_obj.data.materials.append(mat_trim)
        g_obj.data.materials.append(mat_wheel)
        assign_material_slot_to_faces(g_obj, slot_idx)

    bpy.ops.object.select_all(action='DESELECT')
    for g_obj, _ in joined_list:
        g_obj.select_set(True)
    bpy.context.view_layer.objects.active = joined_list[0][0]
    bpy.ops.object.join()
    final_car = bpy.context.active_object
    final_car.name = "SM_Vehicle_Car_Sedan"

    export_fbx("SM_Vehicle_Car_Sedan.fbx")

def build_vehicle_rickshaw():
    print("Building SM_Vehicle_Cycle_Rickshaw...")
    clear_scene()

    mat_tin = bpy.data.materials.new(name="MI_Flower_Rangan_Scarlet")  # Painted tin plate & frame
    mat_hood = bpy.data.materials.new(name="MI_Curzon_Sandstone")       # Rickshaw hood canvas
    mat_chrome = bpy.data.materials.new(name="MI_Curzon_Brass")         # Chrome spokes / handlebars
    mat_tires = bpy.data.materials.new(name="MI_Curzon_CastIron")       # Rubber wheels

    tin_parts = []
    hood_parts = []
    chrome_parts = []
    tire_parts = []

    # Rickshaw: Length 2.4m, Width 1.1m, Height 1.75m
    # 1. Front bicycle frame & fork (chrome)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.03, depth=1.2, location=(0.7, 0, 0.7))
    stem = bpy.context.active_object
    stem.rotation_euler = (0, math.radians(-25), 0)
    bpy.ops.object.transform_apply(rotation=True)
    chrome_parts.append(stem)

    # Handlebars
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.025, depth=0.65, location=(0.6, 0, 1.15))
    h_bar = bpy.context.active_object
    h_bar.rotation_euler = (math.pi * 0.5, 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    chrome_parts.append(h_bar)

    # 2. Passenger Carriage Box (painted tin)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.35, 0, 0.65))
    p_box = bpy.context.active_object
    p_box.scale = (1.1, 0.9, 0.45)
    bpy.ops.object.transform_apply(scale=True)
    tin_parts.append(p_box)

    # Back rest tin plate (iconic Dhaka rickshaw art plate)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.85, 0, 0.95))
    art_plate = bpy.context.active_object
    art_plate.scale = (0.05, 0.85, 0.55)
    bpy.ops.object.transform_apply(scale=True)
    tin_parts.append(art_plate)

    # 3. Folding Carriage Hood (hooded canopy)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.55, depth=0.88, location=(-0.45, 0, 1.35))
    hood = bpy.context.active_object
    hood.scale = (1.0, 1.0, 0.7)
    hood.rotation_euler = (math.pi * 0.5, 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    hood_parts.append(hood)

    # 4. Spoked Wheels (1 front, 2 rear)
    # Front wheel
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.35, depth=0.08, location=(1.1, 0, 0.35))
    fw = bpy.context.active_object
    fw.rotation_euler = (math.pi * 0.5, 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    tire_parts.append(fw)

    # Rear wheels
    for ry in [-0.52, 0.52]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.38, depth=0.08, location=(-0.35, ry, 0.38))
        rw = bpy.context.active_object
        rw.rotation_euler = (math.pi * 0.5, 0, 0)
        bpy.ops.object.transform_apply(rotation=True)
        tire_parts.append(rw)

    groups = [
        (tin_parts, mat_tin, 0),
        (hood_parts, mat_hood, 1),
        (chrome_parts, mat_chrome, 2),
        (tire_parts, mat_tires, 3),
    ]

    joined_list = []
    for parts, mat, slot_idx in groups:
        if not parts:
            continue
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            p.select_set(True)
        bpy.context.view_layer.objects.active = parts[0]
        if len(parts) > 1:
            bpy.ops.object.join()
        g_obj = bpy.context.active_object

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

        joined_list.append((g_obj, slot_idx))

    for g_obj, slot_idx in joined_list:
        g_obj.data.materials.append(mat_tin)
        g_obj.data.materials.append(mat_hood)
        g_obj.data.materials.append(mat_chrome)
        g_obj.data.materials.append(mat_tires)
        assign_material_slot_to_faces(g_obj, slot_idx)

    bpy.ops.object.select_all(action='DESELECT')
    for g_obj, _ in joined_list:
        g_obj.select_set(True)
    bpy.context.view_layer.objects.active = joined_list[0][0]
    bpy.ops.object.join()
    final_rickshaw = bpy.context.active_object
    final_rickshaw.name = "SM_Vehicle_Cycle_Rickshaw"

    export_fbx("SM_Vehicle_Cycle_Rickshaw.fbx")

# =============================================================================
# 7. MODERN DHAKA CITY SKYLINE TOWERS
# =============================================================================
def build_modern_tower_glass():
    print("Building SM_Modern_Tower_Glass...")
    clear_scene()

    mat_glass = bpy.data.materials.new(name="MI_Modern_RibbonWindow")
    mat_fins = bpy.data.materials.new(name="MI_Modern_ConcreteFin")

    glass_parts = []
    fin_parts = []

    # 24-Story Glass Skyscraper (32m x 32m x 95m tall)
    # 1. Main Glass Core
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 45.0))
    core = bpy.context.active_object
    core.scale = (32.0, 32.0, 90.0)
    bpy.ops.object.transform_apply(scale=True)
    glass_parts.append(core)

    # 2. Vertical Architectural Mullions / Fins
    for i in range(-14, 15, 4):
        # East/West facade fins
        for fy in [-16.2, 16.2]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(i, fy, 45.0))
            fin = bpy.context.active_object
            fin.scale = (0.4, 0.4, 90.0)
            bpy.ops.object.transform_apply(scale=True)
            fin_parts.append(fin)

        # North/South facade fins
        for fx in [-16.2, 16.2]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(fx, i, 45.0))
            fin = bpy.context.active_object
            fin.scale = (0.4, 0.4, 90.0)
            bpy.ops.object.transform_apply(scale=True)
            fin_parts.append(fin)

    # 3. Rooftop Penthouse & Mechanical Crown (Z=90m to Z=102m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 94.0))
    penthouse = bpy.context.active_object
    penthouse.scale = (24.0, 24.0, 8.0)
    bpy.ops.object.transform_apply(scale=True)
    fin_parts.append(penthouse)

    # Rooftop antenna spire
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.5, depth=14.0, location=(0, 0, 105.0))
    spire = bpy.context.active_object
    fin_parts.append(spire)

    # 4. Ground Floor Grand Colonnade (Z=0m to Z=7m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 3.5))
    lobby = bpy.context.active_object
    lobby.scale = (34.0, 34.0, 7.0)
    bpy.ops.object.transform_apply(scale=True)
    glass_parts.append(lobby)

    # Join and map
    groups = [
        (glass_parts, mat_glass, 0),
        (fin_parts, mat_fins, 1),
    ]

    joined_list = []
    for parts, mat, slot_idx in groups:
        if not parts:
            continue
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            p.select_set(True)
        bpy.context.view_layer.objects.active = parts[0]
        if len(parts) > 1:
            bpy.ops.object.join()
        g_obj = bpy.context.active_object

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

        joined_list.append((g_obj, slot_idx))

    for g_obj, slot_idx in joined_list:
        g_obj.data.materials.append(mat_glass)
        g_obj.data.materials.append(mat_fins)
        assign_material_slot_to_faces(g_obj, slot_idx)

    bpy.ops.object.select_all(action='DESELECT')
    for g_obj, _ in joined_list:
        g_obj.select_set(True)
    bpy.context.view_layer.objects.active = joined_list[0][0]
    bpy.ops.object.join()
    final_tower = bpy.context.active_object
    final_tower.name = "SM_Modern_Tower_Glass"

    export_fbx("SM_Modern_Tower_Glass.fbx")

def build_modern_building_commercial():
    print("Building SM_Modern_Building_Commercial...")
    clear_scene()

    mat_concrete = bpy.data.materials.new(name="MI_Hero_Modern")
    mat_ribbon = bpy.data.materials.new(name="MI_Modern_RibbonWindow")
    mat_louvers = bpy.data.materials.new(name="MI_Curzon_CastIron")

    conc_parts = []
    ribbon_parts = []
    louver_parts = []

    # 16-story stepped building (48m x 26m x 68m tall)
    # Tier 1 (Podium: Z=0 to Z=25m, 48m x 26m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 12.5))
    podium = bpy.context.active_object
    podium.scale = (48.0, 26.0, 25.0)
    bpy.ops.object.transform_apply(scale=True)
    conc_parts.append(podium)

    # Ribbon windows on podium
    for floor_z in [4.5, 9.5, 14.5, 19.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, floor_z))
        rib = bpy.context.active_object
        rib.scale = (48.4, 26.4, 1.8)
        bpy.ops.object.transform_apply(scale=True)
        ribbon_parts.append(rib)

    # Tier 2 (Tower setback: Z=25m to Z=52m, 36m x 22m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-3.0, 0, 38.5))
    t2 = bpy.context.active_object
    t2.scale = (36.0, 22.0, 27.0)
    bpy.ops.object.transform_apply(scale=True)
    conc_parts.append(t2)

    for floor_z in [28.0, 34.0, 40.0, 46.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-3.0, 0, floor_z))
        rib = bpy.context.active_object
        rib.scale = (36.4, 22.4, 1.8)
        bpy.ops.object.transform_apply(scale=True)
        ribbon_parts.append(rib)

    # Tier 3 (Rooftop Crown: Z=52m to Z=66m, 24m x 18m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-6.0, 0, 59.0))
    t3 = bpy.context.active_object
    t3.scale = (24.0, 18.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    conc_parts.append(t3)

    # Louver sunshades across facade
    for lz in range(6, 60, 4):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 13.3, lz))
        louv = bpy.context.active_object
        louv.scale = (30.0, 0.4, 0.25)
        bpy.ops.object.transform_apply(scale=True)
        louver_parts.append(louv)

    groups = [
        (conc_parts, mat_concrete, 0),
        (ribbon_parts, mat_ribbon, 1),
        (louver_parts, mat_louvers, 2),
    ]

    joined_list = []
    for parts, mat, slot_idx in groups:
        if not parts:
            continue
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            p.select_set(True)
        bpy.context.view_layer.objects.active = parts[0]
        if len(parts) > 1:
            bpy.ops.object.join()
        g_obj = bpy.context.active_object

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.01)
        bpy.ops.object.mode_set(mode='OBJECT')

        joined_list.append((g_obj, slot_idx))

    for g_obj, slot_idx in joined_list:
        g_obj.data.materials.append(mat_concrete)
        g_obj.data.materials.append(mat_ribbon)
        g_obj.data.materials.append(mat_louvers)
        assign_material_slot_to_faces(g_obj, slot_idx)

    bpy.ops.object.select_all(action='DESELECT')
    for g_obj, _ in joined_list:
        g_obj.select_set(True)
    bpy.context.view_layer.objects.active = joined_list[0][0]
    bpy.ops.object.join()
    final_comm = bpy.context.active_object
    final_comm.name = "SM_Modern_Building_Commercial"

    export_fbx("SM_Modern_Building_Commercial.fbx")

# =============================================================================
# MAIN ORCHESTRATION
# =============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("STARTING BLENDER NATURAL ASSET GENERATION")
    print("=" * 60)
    build_krishnachura_natural()
    build_debdaru_natural()
    build_banyan_natural()
    build_flowerbed_circular()
    build_flowerbed_border()
    build_curzon_heritage_gate()
    build_vehicle_bus_dhaka()
    build_vehicle_cng()
    build_vehicle_sedan()
    build_vehicle_rickshaw()
    build_modern_tower_glass()
    build_modern_building_commercial()
    print("=" * 60)
    print("✅ ALL 12 NATURAL & URBAN ASSETS GENERATED SUCCESSFULLY!")
    print("=" * 60)
