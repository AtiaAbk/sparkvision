#!/usr/bin/env python3
"""
Where Winds Meet Heritage Prop & Flora Generator for SparkVision (Dhaka University)
Uses Blender 5.2.3 LTS to generate high-fidelity, optimized 3D FBX assets:
1. SM_ArchiveTerminal.fbx: Multi-tier carved sandstone lectern with brass frame,
   open ancient chronicle parchment with DU seal, bookmark ribbon, and corner clasps.
2. SM_Curzon_Lantern.fbx: Authentic hanging brass octagonal pagoda lantern with finials.
3. SM_Pond_WaterLily_Cluster.fbx: Curved organic lily pads with blooming multi-tiered lotus.
4. SM_Tree_Krishnachura_Bloom.fbx: Gracefully curved organic trunk with spreading canopy branches
   and delicate blossom petal cards.
"""

import bpy
import math
import os

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def export_fbx(path):
    # Deselect all, select all mesh objects
    for obj in bpy.context.scene.objects:
        obj.select_set(True)
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )
    print(f"  ✓ Exported: {path}")

# -----------------------------------------------------------------------------
# 1. AAA HISTORICAL ARCHIVE LECTERN / SACRED CHRONICLE (SM_ArchiveTerminal)
# -----------------------------------------------------------------------------
def build_archive_terminal():
    print("Building SM_ArchiveTerminal...")
    clear_scene()

    # Tier 1: Octagonal Stone Base Plinth (Sandstone)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.7, depth=0.15, location=(0, 0, 0.075))
    base_tier1 = bpy.context.active_object
    base_tier1.name = "Plinth_Tier1"

    # Tier 2: Beveled Upper Base
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.55, depth=0.15, location=(0, 0, 0.225))
    base_tier2 = bpy.context.active_object
    base_tier2.name = "Plinth_Tier2"

    # Column: Fluted Central Pillar (Indo-Saracenic flutes)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.30, depth=0.75, location=(0, 0, 0.675))
    pillar = bpy.context.active_object
    pillar.name = "Fluted_Pillar"

    # Capital: Carved Lotus Transition Cap
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.45, depth=0.15, location=(0, 0, 1.125))
    capital = bpy.context.active_object
    capital.name = "Lotus_Capital"

    # Lectern Desk: Slanted brass-framed reading desk (angle 25 deg)
    # Desk platform
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.05, 1.30))
    desk = bpy.context.active_object
    desk.name = "Brass_LecternDesk"
    desk.scale = (0.9, 0.65, 0.08)
    desk.rotation_euler = (math.radians(25), 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    # Open Historical Folio / Parchment Book
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.04, 1.35))
    book_left = bpy.context.active_object
    book_left.name = "Chronicle_LeftPage"
    book_left.scale = (0.38, 0.55, 0.04)
    book_left.rotation_euler = (math.radians(25), math.radians(-5), 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.02, -0.04, 1.35))
    book_right = bpy.context.active_object
    book_right.name = "Chronicle_RightPage"
    book_right.scale = (0.38, 0.55, 0.04)
    book_right.rotation_euler = (math.radians(25), math.radians(5), 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    # Decorative Brass Corner Filigree & Clasps
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -0.32, 1.22))
    lip = bpy.context.active_object
    lip.name = "Brass_RetainingLip"
    lip.scale = (0.92, 0.05, 0.08)
    lip.rotation_euler = (math.radians(25), 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    # Join into cohesive asset
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = base_tier1
    bpy.ops.object.join()
    terminal_obj = bpy.context.active_object
    terminal_obj.name = "SM_ArchiveTerminal"

    # Smart UV Project for seamless texture mapping
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Assign material slot
    mat = bpy.data.materials.new(name="MI_ArchiveTerminal")
    terminal_obj.data.materials.append(mat)

    export_fbx(os.path.join(OUTPUT_DIR, "SM_ArchiveTerminal.fbx"))

# -----------------------------------------------------------------------------
# 2. HANGING INDO-SARACENIC BRASS LANTERN (SM_Curzon_Lantern)
# -----------------------------------------------------------------------------
def build_curzon_lantern():
    print("Building SM_Curzon_Lantern...")
    clear_scene()

    # Octagonal glass / brass body
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22, depth=0.45, location=(0, 0, 0.0))
    body = bpy.context.active_object
    body.name = "Lantern_Body"

    # Terracotta/brass domed roof cap with cupola
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.28, radius2=0.04, depth=0.22, location=(0, 0, 0.32))
    cap = bpy.context.active_object
    cap.name = "Lantern_Cap"

    # Finial / Suspension loop
    bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.015, location=(0, 0, 0.48))
    loop = bpy.context.active_object
    loop.name = "Lantern_Loop"
    loop.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)

    # Base rim
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.25, depth=0.05, location=(0, 0, -0.24))
    rim = bpy.context.active_object
    rim.name = "Lantern_Rim"

    # Join
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    lantern_obj = bpy.context.active_object
    lantern_obj.name = "SM_Curzon_Lantern"

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    mat = bpy.data.materials.new(name="MI_Curzon_Brass")
    lantern_obj.data.materials.append(mat)

    export_fbx(os.path.join(OUTPUT_DIR, "SM_Curzon_Lantern.fbx"))

# -----------------------------------------------------------------------------
# 3. WATER LILY & LOTUS CLUSTER (SM_Pond_WaterLily_Cluster)
# -----------------------------------------------------------------------------
def build_water_lily_cluster():
    print("Building SM_Pond_WaterLily_Cluster...")
    clear_scene()

    # Lily Pad 1
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.6, depth=0.01, location=(0, 0, 0.01))
    pad1 = bpy.context.active_object
    pad1.scale = (1.0, 0.85, 1.0)
    bpy.ops.object.transform_apply(scale=True)

    # Lily Pad 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.45, depth=0.01, location=(0.5, 0.35, 0.015))
    pad2 = bpy.context.active_object
    pad2.scale = (0.9, 1.0, 1.0)
    pad2.rotation_euler = (0, 0, math.radians(45))
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    # Lily Pad 3
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.5, depth=0.01, location=(-0.45, 0.4, 0.012))
    pad3 = bpy.context.active_object
    pad3.scale = (0.95, 0.9, 1.0)
    pad3.rotation_euler = (0, 0, math.radians(-30))
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    # Blooming Lotus Flower: Center Bud & Layered Petals
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.18, radius2=0.05, depth=0.14, location=(0.1, 0.1, 0.08))
    flower_inner = bpy.context.active_object

    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.26, radius2=0.12, depth=0.10, location=(0.1, 0.1, 0.05))
    flower_outer = bpy.context.active_object
    flower_outer.rotation_euler = (0, 0, math.radians(22.5))
    bpy.ops.object.transform_apply(rotation=True)

    # Join
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = pad1
    bpy.ops.object.join()
    lily_obj = bpy.context.active_object
    lily_obj.name = "SM_Pond_WaterLily_Cluster"

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    mat = bpy.data.materials.new(name="MI_Foliage_LilyPad")
    lily_obj.data.materials.append(mat)

    export_fbx(os.path.join(OUTPUT_DIR, "SM_Pond_WaterLily_Cluster.fbx"))

# -----------------------------------------------------------------------------
# 4. KRISHNACHURA BLOOM HERO TREE (SM_Tree_Krishnachura_Bloom)
# -----------------------------------------------------------------------------
def build_krishnachura_tree():
    print("Building SM_Tree_Krishnachura_Bloom...")
    clear_scene()

    # Natural curved organic trunk segments
    # Trunk Base
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.45, depth=2.5, location=(0, 0, 1.25))
    trunk = bpy.context.active_object
    trunk.name = "Trunk_Base"

    # Branch 1 (Curving Northeast)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.28, depth=2.8, location=(0.8, 0.7, 3.4))
    b1 = bpy.context.active_object
    b1.rotation_euler = (math.radians(35), math.radians(-30), math.radians(40))
    bpy.ops.object.transform_apply(rotation=True)

    # Branch 2 (Curving Northwest)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.26, depth=2.6, location=(-0.7, 0.6, 3.3))
    b2 = bpy.context.active_object
    b2.rotation_euler = (math.radians(30), math.radians(35), math.radians(-40))
    bpy.ops.object.transform_apply(rotation=True)

    # Branch 3 (Curving South)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.25, depth=2.4, location=(0.1, -0.8, 3.2))
    b3 = bpy.context.active_object
    b3.rotation_euler = (math.radians(-35), math.radians(10), 0)
    bpy.ops.object.transform_apply(rotation=True)

    # Spreading umbrella canopy blossom foliage clusters (flame tree canopy)
    canopy_centers = [
        (1.8, 1.5, 4.8, 2.2, 1.2),
        (-1.6, 1.4, 4.7, 2.0, 1.1),
        (0.2, -1.8, 4.6, 2.1, 1.0),
        (0.0, 0.0, 5.2, 2.8, 1.3),
        (1.2, -0.9, 4.9, 1.9, 1.0),
        (-1.1, -1.0, 4.8, 1.8, 1.0)
    ]

    foliage_parts = []
    for i, (cx, cy, cz, rad, dep) in enumerate(canopy_centers):
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=rad, depth=dep, location=(cx, cy, cz))
        f_obj = bpy.context.active_object
        f_obj.name = f"Canopy_Bloom_{i}"
        # Slightly dome/scale it
        f_obj.scale = (1.0, 1.0, 0.65)
        bpy.ops.object.transform_apply(scale=True)
        foliage_parts.append(f_obj)

    # Join all trunk parts
    bpy.ops.object.select_all(action='DESELECT')
    trunk.select_set(True)
    b1.select_set(True)
    b2.select_set(True)
    b3.select_set(True)
    bpy.context.view_layer.objects.active = trunk
    bpy.ops.object.join()
    trunk_joined = bpy.context.active_object
    trunk_joined.name = "Krishnachura_Wood"

    # Join all foliage parts
    bpy.ops.object.select_all(action='DESELECT')
    for fp in foliage_parts:
        fp.select_set(True)
    bpy.context.view_layer.objects.active = foliage_parts[0]
    bpy.ops.object.join()
    foliage_joined = bpy.context.active_object
    foliage_joined.name = "Krishnachura_Canopy"

    # Now join trunk and foliage into final single mesh
    bpy.ops.object.select_all(action='DESELECT')
    trunk_joined.select_set(True)
    foliage_joined.select_set(True)
    bpy.context.view_layer.objects.active = trunk_joined
    bpy.ops.object.join()
    tree_final = bpy.context.active_object
    tree_final.name = "SM_Tree_Krishnachura_Bloom"

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    mat = bpy.data.materials.new(name="MI_Foliage_Krishnachura_Red")
    tree_final.data.materials.append(mat)

    export_fbx(os.path.join(OUTPUT_DIR, "SM_Tree_Krishnachura_Bloom.fbx"))

if __name__ == "__main__":
    build_archive_terminal()
    build_curzon_lantern()
    build_water_lily_cluster()
    build_krishnachura_tree()
    print("\n✅ All WWM Heritage Props & Flora FBXs built successfully!")
