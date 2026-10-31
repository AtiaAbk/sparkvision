#!/usr/bin/env python3
"""
Phase 3 Environment Asset Generator for Blender 5.2.3 LTS
Creates custom 3D architectural landmarks and environment foliage for University of Dhaka:
  1. SM_DoyelMonument (National Bird Roundabout Fountain & Stylized Sculptures)
  2. SM_ShaheedMinar_Monument (Authentic 1952 Language Movement Memorial with upright Sun Disc)
  3. SM_NazrulMausoleum (Poet Kazi Nazrul Islam Open Marble Cenotaph)
  4. SM_Campus_Tree_Hero (Mature Banyan / Raintree Shade Canopy with fluted roots)
  5. SM_CentralLibrary (Muzharul Islam 1953 Tropical Modernist Library on pilotis with brise-soleil)
  6. SM_AparajeyoBangla (Syed Abdullah Khalid 1979 Freedom Fighters Trio on stepped plinth)
Metric scale: 1 Blender unit = 1 meter = 100 Unreal units.
"""

import bpy
import bmesh
import math
import mathutils
import os

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

def get_or_create_material(name, color, roughness=0.7, metallic=0.0, emission=None):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = roughness
            bsdf.inputs["Metallic"].default_value = metallic
            if emission and "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission
                if "Emission Strength" in bsdf.inputs:
                    bsdf.inputs["Emission Strength"].default_value = 1.0
    return mat

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
    print(f"Exported {filepath}")

# 1. Doyel Chattar Magpie Robin Monument (14m diameter fountain & bird sculptures)
def build_doyel_monument():
    reset_scene()
    mat_stone = get_or_create_material("M_Hero_Modern", (0.88, 0.88, 0.90, 1.0), roughness=0.45)
    mat_water = get_or_create_material("M_Water_Pond", (0.05, 0.30, 0.40, 1.0), roughness=0.1)
    mat_bronze = get_or_create_material("M_Curzon_Accent", (0.22, 0.18, 0.14, 1.0), roughness=0.35, metallic=0.85)

    mesh = bpy.data.meshes.new("SM_DoyelMonument")
    obj = bpy.data.objects.new("SM_DoyelMonument", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_stone)   # Slot 0: Basin & Pedestal
    obj.data.materials.append(mat_water)   # Slot 1: Fountain Water
    obj.data.materials.append(mat_bronze)  # Slot 2: Bronze Birds

    bm = bmesh.new()

    # Outer Octagonal Fountain Basin (14m diameter, 1.2m wall)
    basin = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=7.0, radius2=7.0, depth=1.2)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.6), verts=basin["verts"])

    # Water Surface (Slot 1)
    water = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=6.4, radius2=6.4, depth=0.1)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.0), verts=water["verts"])
    for f in [f for f in bm.faces if any(v in water["verts"] for v in f.verts)]:
        f.material_index = 1

    # Tier 1 Stepped Plinth
    plinth1 = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=4.0, radius2=3.4, depth=1.6)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.8), verts=plinth1["verts"])

    # Tier 2 Pedestal
    plinth2 = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=2.6, radius2=2.0, depth=1.8)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 3.5), verts=plinth2["verts"])

    # Top Sculpture Perch Dais
    dais = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(3.6, 2.4, 0.5), verts=dais["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.65), verts=dais["verts"])

    # Two Stylized Doyel (Oriental Magpie-Robin) Sculptures perched proudly (Slot 2)
    # They sit back-to-back, facing outward with high cocked tails
    for idx, (sign, ang_deg) in enumerate([(-1.0, -25.0), (1.0, 25.0)]):
        bird_verts = []
        # Bird Lower Breast / Belly
        belly = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.75, radius2=0.45, depth=2.0)
        rot_body = mathutils.Matrix.Rotation(math.radians(-sign * 30.0), 3, 'Y')
        bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_body, verts=belly["verts"])
        bmesh.ops.translate(bm, vec=(sign * 0.9, 0.0, 5.7), verts=belly["verts"])
        bird_verts.extend(belly["verts"])

        # Upper Torso and Head
        head = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=0.45, radius2=0.15, depth=1.1)
        rot_head = mathutils.Matrix.Rotation(math.radians(-sign * 50.0), 3, 'Y')
        bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_head, verts=head["verts"])
        bmesh.ops.translate(bm, vec=(sign * 1.5, 0.0, 6.7), verts=head["verts"])
        bird_verts.extend(head["verts"])

        # Iconic Cocked Tail Feathers (Fanned upright at ~60 degrees)
        tail = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.25, 0.9, 3.0), verts=tail["verts"])
        rot_tail = mathutils.Matrix.Rotation(math.radians(sign * 55.0), 3, 'Y')
        bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_tail, verts=tail["verts"])
        bmesh.ops.translate(bm, vec=(sign * 0.2, 0.0, 7.3), verts=tail["verts"])
        bird_verts.extend(tail["verts"])

        # Wing planes flanking each bird
        for wing_side in [-1.0, 1.0]:
            wing = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(1.4, 0.15, 0.8), verts=wing["verts"])
            rot_wing = mathutils.Matrix.Rotation(math.radians(-sign * 20.0), 3, 'Y')
            bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_wing, verts=wing["verts"])
            bmesh.ops.translate(bm, vec=(sign * 0.9, wing_side * 0.55, 6.0), verts=wing["verts"])
            bird_verts.extend(wing["verts"])

        for f in bm.faces:
            if any(v in bird_verts for v in f.verts):
                f.material_index = 2

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_DoyelMonument.fbx")

# 2. Central Shaheed Minar Monument (Authentic 1952 Language Movement Memorial)
def build_shaheed_minar():
    reset_scene()
    mat_marble = get_or_create_material("M_Shaheed_Marble", (0.96, 0.96, 0.97, 1.0), roughness=0.25)
    mat_sun = get_or_create_material(
        "M_Shaheed_Sun",
        (0.92, 0.03, 0.03, 1.0),
        roughness=0.35,
        emission=(0.85, 0.02, 0.02, 1.0)
    )
    mat_steps = get_or_create_material("M_Curzon_StonePaving", (0.32, 0.32, 0.35, 1.0), roughness=0.6)

    mesh = bpy.data.meshes.new("SM_ShaheedMinar_Monument")
    obj = bpy.data.objects.new("SM_ShaheedMinar_Monument", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_marble) # Slot 0: White Marble Pillars
    obj.data.materials.append(mat_sun)    # Slot 1: Crimson Sun Disc
    obj.data.materials.append(mat_steps)  # Slot 2: Basalt Steps

    bm = bmesh.new()

    # Elevated Altar Podium (24m wide x 16m deep x 1.2m high)
    podium = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(24.0, 16.0, 1.2), verts=podium["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.6), verts=podium["verts"])
    for f in [f for f in bm.faces if any(v in podium["verts"] for v in f.verts)]:
        f.material_index = 2

    # Stepped Approach Base (Slot 0)
    base = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(18.0, 10.0, 0.4), verts=base["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.4), verts=base["verts"])

    # Central Mother Pillar (14m tall, vertical lower trunk, slanted forward 15° canopy)
    # Left vertical shaft
    m_left = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.2, 0.8, 10.0), verts=m_left["verts"])
    bmesh.ops.translate(bm, vec=(-2.2, -1.0, 6.6), verts=m_left["verts"])

    # Right vertical shaft
    m_right = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.2, 0.8, 10.0), verts=m_right["verts"])
    bmesh.ops.translate(bm, vec=(2.2, -1.0, 6.6), verts=m_right["verts"])

    # Cross connecting horizontal lintel beam
    beam = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(5.6, 0.8, 0.8), verts=beam["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -1.0, 11.2), verts=beam["verts"])

    # Slanted Forward Canopy (Mother protecting children, 15° pitch forward towards -Y)
    canopy = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(6.0, 3.5, 1.2), verts=canopy["verts"])
    # Tilt forward: in Blender, rotation around +X tilts +Z towards -Y
    rot_canopy = mathutils.Matrix.Rotation(math.radians(15.0), 3, 'X')
    bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_canopy, verts=canopy["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -1.8, 12.3), verts=canopy["verts"])

    # Brilliant Crimson Sun Disc (6.4m diameter disc centered behind mother column, Slot 1)
    # Cylinder with solid end caps rotated 90 degrees around X so circular faces stand vertically in X-Z plane!
    sun = bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=3.2, radius2=3.2, depth=0.35)
    rot_sun = mathutils.Matrix.Rotation(math.radians(90.0), 3, 'X')
    bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_sun, verts=sun["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.8, 7.5), verts=sun["verts"])
    for f in [f for f in bm.faces if any(v in sun["verts"] for v in f.verts)]:
        f.material_index = 1

    # Flanking Child Columns (Outer Left & Right)
    # Inner Left (10m tall)
    c_il = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.0, 0.7, 9.0), verts=c_il["verts"])
    bmesh.ops.translate(bm, vec=(-5.2, -0.6, 5.9), verts=c_il["verts"])

    # Inner Right (10m tall)
    c_ir = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.0, 0.7, 9.0), verts=c_ir["verts"])
    bmesh.ops.translate(bm, vec=(5.2, -0.6, 5.9), verts=c_ir["verts"])

    # Outer Left (7m tall)
    c_ol = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(0.9, 0.6, 6.5), verts=c_ol["verts"])
    bmesh.ops.translate(bm, vec=(-7.8, -0.3, 4.65), verts=c_ol["verts"])

    # Outer Right (7m tall)
    c_or = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(0.9, 0.6, 6.5), verts=c_or["verts"])
    bmesh.ops.translate(bm, vec=(7.8, -0.3, 4.65), verts=c_or["verts"])

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_ShaheedMinar_Monument.fbx")

# 3. Kazi Nazrul Islam Mausoleum (Open Marble Cenotaph)
def build_nazrul_mausoleum():
    reset_scene()
    mat_marble = get_or_create_material("M_Shaheed_Marble", (0.95, 0.95, 0.96, 1.0), roughness=0.3)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.88, 0.86, 0.82, 1.0), roughness=0.5)

    mesh = bpy.data.meshes.new("SM_NazrulMausoleum")
    obj = bpy.data.objects.new("SM_NazrulMausoleum", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_marble) # Slot 0: Cenotaph & Plinth
    obj.data.materials.append(mat_trim)   # Slot 1: Jali Railing

    bm = bmesh.new()

    # Elevated Plinth (10m x 8m x 0.6m)
    p = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(10.0, 8.0, 0.6), verts=p["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.3), verts=p["verts"])

    # Inner Stepped Dais
    d = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(5.0, 3.2, 0.4), verts=d["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.8), verts=d["verts"])

    # Marble Sarcophagus Cenotaph
    c = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(3.2, 1.6, 0.9), verts=c["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.45), verts=c["verts"])

    # Perimeter Jali Balustrade Screen (Slot 1)
    for sx, sy, w, d_dim in [(-4.8, 0.0, 0.3, 7.6), (4.8, 0.0, 0.3, 7.6), (0.0, -3.8, 9.6, 0.3), (0.0, 3.8, 9.6, 0.3)]:
        scr = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(w, d_dim, 0.8), verts=scr["verts"])
        bmesh.ops.translate(bm, vec=(sx, sy, 1.0), verts=scr["verts"])
        for f in [f for f in bm.faces if any(v in scr["verts"] for v in f.verts)]:
            f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_NazrulMausoleum.fbx")

# 4. Hero Campus Shade Tree (Mature Banyan / Raintree Canopy)
def build_campus_tree():
    reset_scene()
    mat_bark = get_or_create_material("M_Curzon_Accent", (0.18, 0.14, 0.11, 1.0), roughness=0.85)
    mat_leaves = get_or_create_material("M_Ground_Grass", (0.12, 0.32, 0.10, 1.0), roughness=0.6)

    mesh = bpy.data.meshes.new("SM_Campus_Tree_Hero")
    obj = bpy.data.objects.new("SM_Campus_Tree_Hero", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_bark)   # Slot 0: Trunk & Branches
    obj.data.materials.append(mat_leaves) # Slot 1: Leaf Canopy

    bm = bmesh.new()

    # Fluted Trunk (diameter 1.8m at base, 1.2m at fork, height 6m)
    trunk = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=1.4, radius2=0.9, depth=6.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 3.0), verts=trunk["verts"])

    # 4 Buttress Roots at base
    for ang in [0.0, math.pi/2.0, math.pi, 3.0*math.pi/2.0]:
        rx = 1.6 * math.cos(ang)
        ry = 1.6 * math.sin(ang)
        r = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.5, 0.5, 2.0), verts=r["verts"])
        bmesh.ops.translate(bm, vec=(rx, ry, 1.0), verts=r["verts"])

    # 4 Spreading Main Branches
    for ang in [0.0, math.pi/2.0, math.pi, 3.0*math.pi/2.0]:
        bx = 2.2 * math.cos(ang)
        by = 2.2 * math.sin(ang)
        b = bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.5, radius2=0.25, depth=4.0)
        bmesh.ops.translate(bm, vec=(bx, by, 7.5), verts=b["verts"])

    # Spreading Multi-tier Foliage Canopy (16m wide umbrella crown, Slot 1)
    # Lower canopy tier
    fol1 = bmesh.ops.create_cone(bm, cap_ends=True, segments=14, radius1=8.0, radius2=4.0, depth=4.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 9.5), verts=fol1["verts"])
    for f in [f for f in bm.faces if any(v in fol1["verts"] for v in f.verts)]:
        f.material_index = 1

    # Upper canopy tier
    fol2 = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=5.5, radius2=1.5, depth=3.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 12.5), verts=fol2["verts"])
    for f in [f for f in bm.faces if any(v in fol2["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Campus_Tree_Hero.fbx")

# 5. Dhaka University Central Library (Muzharul Islam 1953 Modernist Masterpiece)
def build_central_library():
    reset_scene()
    mat_concrete = get_or_create_material("M_Supporting_Building", (0.80, 0.80, 0.82, 1.0), roughness=0.6)
    mat_louvers = get_or_create_material("M_Hero_Modern", (0.92, 0.92, 0.94, 1.0), roughness=0.4)
    mat_glass = get_or_create_material("M_Water_Pond", (0.1, 0.15, 0.20, 1.0), roughness=0.1)

    mesh = bpy.data.meshes.new("SM_CentralLibrary")
    obj = bpy.data.objects.new("SM_CentralLibrary", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_concrete) # Slot 0: Structural Frame & Pilotis
    obj.data.materials.append(mat_louvers)  # Slot 1: Brise-Soleil Concrete Louvers
    obj.data.materials.append(mat_glass)    # Slot 2: Recessed Windows

    bm = bmesh.new()

    # Elevated Main Volume (54m wide x 30m deep x 16m high)
    main_vol = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(54.0, 30.0, 12.0), verts=main_vol["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 10.0), verts=main_vol["verts"])

    # Ground Floor Pilotis (Open colonnade stilts raising building above ground)
    for px in [-24.0, -16.0, -8.0, 0.0, 8.0, 16.0, 24.0]:
        for py in [-12.0, 0.0, 12.0]:
            piloti = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(0.9, 0.9, 4.0), verts=piloti["verts"])
            bmesh.ops.translate(bm, vec=(px, py, 2.0), verts=piloti["verts"])

    # Exterior Brise-Soleil Concrete Sun Louvers on South and North facades (Slot 1)
    for face_y in [-15.2, 15.2]:
        for lx in range(-25, 26, 2):
            louver = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(0.2, 0.8, 11.5), verts=louver["verts"])
            bmesh.ops.translate(bm, vec=(float(lx), face_y, 10.0), verts=louver["verts"])
            for f in [f for f in bm.faces if any(v in louver["verts"] for v in f.verts)]:
                f.material_index = 1

    # Entrance Ramp & Lobby Pavilions
    ramp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(12.0, 8.0, 1.5), verts=ramp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -18.0, 0.75), verts=ramp["verts"])

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_CentralLibrary.fbx")

# 6. Aparajeyo Bangla (Syed Abdullah Khalid 1979 Freedom Fighters Trio)
def build_aparajeyo_bangla():
    reset_scene()
    mat_plinth = get_or_create_material("M_Curzon_StonePaving", (0.35, 0.35, 0.38, 1.0), roughness=0.6)
    mat_sculpt = get_or_create_material("M_Hero_Modern", (0.82, 0.80, 0.76, 1.0), roughness=0.55)

    mesh = bpy.data.meshes.new("SM_AparajeyoBangla")
    obj = bpy.data.objects.new("SM_AparajeyoBangla", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_plinth)  # Slot 0: Stepped Concrete Plinth
    obj.data.materials.append(mat_sculpt)  # Slot 1: Cast Concrete Hero Statues

    bm = bmesh.new()

    # Stepped Concrete Base
    base1 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(8.0, 6.0, 1.2), verts=base1["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.6), verts=base1["verts"])

    base2 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(6.5, 4.5, 1.8), verts=base2["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.1), verts=base2["verts"])

    # 3 Heroic Figures standing resolute:
    # 1. Central Figure: Peasant freedom fighter holding rifle (taller, central leader)
    # 2. Left Figure: Female freedom fighter / nurse (Hasina Khan)
    # 3. Right Figure: Youth student freedom fighter
    trio = [
        # (X offset, Y offset, height, width, role)
        (0.0, 0.3, 5.5, 1.6, "Center_FarmerLeader"),
        (-1.8, -0.2, 4.8, 1.3, "Left_FemaleNurse"),
        (1.8, -0.2, 5.1, 1.4, "Right_Student")
    ]

    for ox, oy, h, w, role in trio:
        body = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(w, 1.1, h), verts=body["verts"])
        bmesh.ops.translate(bm, vec=(ox, oy, 3.0 + h/2.0), verts=body["verts"])
        for f in [f for f in bm.faces if any(v in body["verts"] for v in f.verts)]:
            f.material_index = 1

        # Head / Face
        head = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.45, radius2=0.35, depth=0.8)
        bmesh.ops.translate(bm, vec=(ox, oy + 0.1, 3.0 + h + 0.4), verts=head["verts"])
        for f in [f for f in bm.faces if any(v in head["verts"] for v in f.verts)]:
            f.material_index = 1

    # Central Figure Rifle
    rifle = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(0.15, 0.15, 4.2), verts=rifle["verts"])
    rot_rifle = mathutils.Matrix.Rotation(math.radians(15.0), 3, 'Y')
    bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_rifle, verts=rifle["verts"])
    bmesh.ops.translate(bm, vec=(0.8, 0.6, 6.0), verts=rifle["verts"])
    for f in [f for f in bm.faces if any(v in rifle["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_AparajeyoBangla.fbx")

# 7. Sontrash Birodhi Raju Sharok Bhaskorjyo (Anti-Terrorism Raju Memorial Sculpture at TSC Mor)
def build_raju_sculpture():
    reset_scene()
    mat_plinth = get_or_create_material("M_Curzon_StonePaving", (0.32, 0.32, 0.35, 1.0), roughness=0.65)
    mat_bronze = get_or_create_material("M_Hero_Modern", (0.85, 0.82, 0.78, 1.0), roughness=0.45)

    mesh = bpy.data.meshes.new("SM_RajuSculpture")
    obj = bpy.data.objects.new("SM_RajuSculpture", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_plinth)  # Slot 0: Stepped Granite Plinth
    obj.data.materials.append(mat_bronze)  # Slot 1: Linked Hero Figures

    bm = bmesh.new()

    # Tier 1 Circular Pedestal Base (14m diameter, 0.7m height)
    base1 = bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=7.0, radius2=7.0, depth=0.7)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.35), verts=base1["verts"])

    # Tier 2 Concentric Plinth (11m diameter, 0.6m height)
    base2 = bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=5.5, radius2=5.5, depth=0.6)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.0), verts=base2["verts"])

    # Tier 3 Central Pedestal Platform (8m diameter, 0.8m height)
    base3 = bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=4.0, radius2=3.8, depth=0.8)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.7), verts=base3["verts"])

    # Ring of 8 Interconnected Hero Figures (Solidarity ring holding hands in defiance of terrorism)
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    radius_ring = 3.2
    for i, deg in enumerate(angles):
        rad = math.radians(deg)
        fx = radius_ring * math.cos(rad)
        fy = radius_ring * math.sin(rad)
        rot_z = mathutils.Matrix.Rotation(rad, 3, 'Z')

        # Torso & Legs
        body = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.9, 0.6, 3.4), verts=body["verts"])
        bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_z, verts=body["verts"])
        bmesh.ops.translate(bm, vec=(fx, fy, 3.8), verts=body["verts"])
        for f in [f for f in bm.faces if any(v in body["verts"] for v in f.verts)]:
            f.material_index = 1

        # Head with determined gaze
        head = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.35, radius2=0.25, depth=0.7)
        bmesh.ops.translate(bm, vec=(fx, fy, 5.8), verts=head["verts"])
        for f in [f for f in bm.faces if any(v in head["verts"] for v in f.verts)]:
            f.material_index = 1

        # Interconnected Arm / Hand Clasp to next neighbor
        next_rad = math.radians(angles[(i + 1) % len(angles)])
        nx = radius_ring * math.cos(next_rad)
        ny = radius_ring * math.sin(next_rad)
        mid_x = (fx + nx) / 2.0
        mid_y = (fy + ny) / 2.0
        arm_dx = nx - fx
        arm_dy = ny - fy
        arm_len = math.sqrt(arm_dx*arm_dx + arm_dy*arm_dy)
        arm_angle = math.atan2(arm_dy, arm_dx)

        arm = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(arm_len * 0.95, 0.25, 0.25), verts=arm["verts"])
        rot_arm = mathutils.Matrix.Rotation(arm_angle, 3, 'Z')
        bmesh.ops.rotate(bm, cent=(0.0, 0.0, 0.0), matrix=rot_arm, verts=arm["verts"])
        bmesh.ops.translate(bm, vec=(mid_x, mid_y, 4.4), verts=arm["verts"])
        for f in [f for f in bm.faces if any(v in arm["verts"] for v in f.verts)]:
            f.material_index = 1

    # Central Raised Freedom / Anti-Terrorism Torch & Triumphant Figure
    core_pedestal = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=1.6, radius2=1.4, depth=1.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.85), verts=core_pedestal["verts"])

    # Heroic Central Figure
    center_body = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.1, 0.8, 3.8), verts=center_body["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 5.5), verts=center_body["verts"])
    for f in [f for f in bm.faces if any(v in center_body["verts"] for v in f.verts)]:
        f.material_index = 1

    center_head = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.4, radius2=0.3, depth=0.75)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 7.7), verts=center_head["verts"])
    for f in [f for f in bm.faces if any(v in center_head["verts"] for v in f.verts)]:
        f.material_index = 1

    # Raised Central Standard / Banner of Defiance reaching 9m high
    standard = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.15, radius2=0.1, depth=5.5)
    bmesh.ops.translate(bm, vec=(0.4, 0.3, 7.2), verts=standard["verts"])
    for f in [f for f in bm.faces if any(v in standard["verts"] for v in f.verts)]:
        f.material_index = 1

    banner = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.6, 0.1, 1.2), verts=banner["verts"])
    bmesh.ops.translate(bm, vec=(1.2, 0.3, 9.2), verts=banner["verts"])
    for f in [f for f in bm.faces if any(v in banner["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_RajuSculpture.fbx")

# 8. Teacher-Student Centre (TSC) Complex (Constantinos Doxiadis 1961 Modernism)
def build_tsc_building():
    reset_scene()
    mat_concrete = get_or_create_material("M_Hero_Modern", (0.88, 0.88, 0.88, 1.0), roughness=0.55)
    mat_brick = get_or_create_material("M_Curzon_StonePaving", (0.55, 0.22, 0.18, 1.0), roughness=0.7)
    mat_mullion = get_or_create_material("M_Curzon_Accent", (0.15, 0.15, 0.15, 1.0), roughness=0.3, metallic=0.7)

    mesh = bpy.data.meshes.new("SM_TSC_Building")
    obj = bpy.data.objects.new("SM_TSC_Building", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_concrete)  # Slot 0: Modernist Concrete Frame / Folded Canopy
    obj.data.materials.append(mat_brick)     # Slot 1: Terracotta Brick Walls & Plinth
    obj.data.materials.append(mat_mullion)   # Slot 2: Dark Louvers / Mullions

    bm = bmesh.new()

    # Ground Foundation Plinth (54m wide x 44m deep x 0.8m high)
    plinth = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(54.0, 44.0, 0.8), verts=plinth["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.4), verts=plinth["verts"])
    for f in [f for f in bm.faces if any(v in plinth["verts"] for v in f.verts)]:
        f.material_index = 1

    # Main Auditorium Drum Block (Modernist hexagonal/octagonal volume)
    # Centered at (0, 6, 7.5), dimensions: 36m wide, 28m deep, 13m high
    aud = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(36.0, 28.0, 13.0), verts=aud["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 6.0, 7.3), verts=aud["verts"])
    for f in [f for f in bm.faces if any(v in aud["verts"] for v in f.verts)]:
        f.material_index = 1  # Brick auditorium envelope

    # Folded-Plate Concrete Cantilevered Roof Canopy over Auditorium
    # 40m x 32m x 1.4m cantilevered cap
    roof = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(40.0, 32.0, 1.4), verts=roof["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 6.0, 14.5), verts=roof["verts"])
    for f in [f for f in bm.faces if any(v in roof["verts"] for v in f.verts)]:
        f.material_index = 0  # White concrete folded roof

    # Front Cafeteria & Lounge Wing (Modernist 2-storey pavilion facing South towards TSC Mor)
    # Dimensions: 46m wide, 14m deep, 7.5m high, centered at (0, -14, 4.5)
    cafe_slab = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(46.0, 14.0, 0.8), verts=cafe_slab["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -14.0, 4.5), verts=cafe_slab["verts"])
    for f in [f for f in bm.faces if any(v in cafe_slab["verts"] for v in f.verts)]:
        f.material_index = 0

    cafe_roof = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(48.0, 15.0, 0.8), verts=cafe_roof["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -14.0, 8.5), verts=cafe_roof["verts"])
    for f in [f for f in bm.faces if any(v in cafe_roof["verts"] for v in f.verts)]:
        f.material_index = 0

    # First floor enclosure with ribbon louvers
    cafe_upper = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(44.0, 12.0, 3.2), verts=cafe_upper["verts"])
    bmesh.ops.translate(bm, vec=(0.0, -14.0, 6.5), verts=cafe_upper["verts"])
    for f in [f for f in bm.faces if any(v in cafe_upper["verts"] for v in f.verts)]:
        f.material_index = 2  # Louvers / mullions

    # Ground floor open pilotis / colonnade (Doxiadis's tropical passive breeze corridor)
    for col_x in range(-20, 21, 5):
        for col_y in [-19.0, -9.0]:
            col = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(0.7, 0.7, 3.7), verts=col["verts"])
            bmesh.ops.translate(bm, vec=(float(col_x), col_y, 2.65), verts=col["verts"])
            for f in [f for f in bm.faces if any(v in col["verts"] for v in f.verts)]:
                f.material_index = 0

    # East-West Connecting Courtyard Arcade Wings
    for wing_x, sign in [(-22.0, -1.0), (22.0, 1.0)]:
        wing = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(6.0, 16.0, 6.0), verts=wing["verts"])
        bmesh.ops.translate(bm, vec=(wing_x, -1.0, 3.8), verts=wing["verts"])
        for f in [f for f in bm.faces if any(v in wing["verts"] for v in f.verts)]:
            f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_TSC_Building.fbx")

def main():
    print("=== Generating High-Fidelity Phase 3 DU Campus Assets in Blender ===")
    build_doyel_monument()
    build_shaheed_minar()
    build_nazrul_mausoleum()
    build_campus_tree()
    build_central_library()
    build_aparajeyo_bangla()
    build_raju_sculpture()
    build_tsc_building()
    print("=== All Phase 3 environment models successfully generated! ===")

if __name__ == "__main__":
    main()
