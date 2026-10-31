#!/usr/bin/env python3
"""
Full University of Dhaka Campus Architectural Asset Generator
for Blender 5.2.3 LTS.

Creates authentic 3D architectural models for all primary sectors of DU:
  1. SM_KalaBhaban (Arts Faculty Building - Modernist brise-soleil academic block)
  2. SM_CentralMosque (DU Central Mosque - Classical central dome & 4 minarets)
  3. SM_SalimullahMuslim_Hall (SM Hall - 1931 Indo-Saracenic colonial quadrangle)
  4. SM_Shahidullah_Hall (Colonial red-brick science residential quadrangle)
  5. SM_Curzon_ScienceAnnex (Colonial Indo-Saracenic departmental wings)
  6. SM_Jagannath_Hall (Colonial red-brick residential quadrangle)
  7. SM_Rokeya_Hall (Colonial red-brick women's hall with gated quad)
  8. SM_SurjaSen_Hall (Modernist multi-storey residential block)
  9. SM_Admin_Building (DU Administrative Registrar Building)
  10. SM_IBA_Building (Institute of Business Administration complex)
  11. SM_BanglaAcademy (Burdwan House heritage pavilion complex)
  12. SM_Campus_BoundaryWall (20m modular brick pillar & wrought-iron railing)
  13. SM_Campus_Skyline (Low-poly urban silhouette backdrop for campus perimeter)

Scale standard: 1 Blender unit = 1 meter = 100 Unreal units.
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
    for mat in bpy.data.materials:
        if mat.users == 0:
            bpy.data.materials.remove(mat)

def get_or_create_material(name, color, roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = roughness
            bsdf.inputs["Metallic"].default_value = metallic
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

# ==============================================================================
# 1. KALA BHABAN (ARTS FACULTY BUILDING)
# Dimensions: 160m long x 50m wide x 24m high. 4 storeys.
# Modernist brise-soleil (sun louvers), red brick infill panels, grand entrance.
# ==============================================================================
def build_kala_bhaban():
    reset_scene()
    mat_concrete = get_or_create_material("M_Hero_Modern", (0.82, 0.81, 0.78, 1.0), roughness=0.6)
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.55, 0.18, 0.12, 1.0), roughness=0.85)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth / Foundation (162m x 52m x 1.5m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.75))
    plinth = bpy.context.active_object
    plinth.scale = (162.0, 52.0, 1.5)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # Grand Entrance Steps at Front (South): 30m wide, 8m deep, 1.5m high stepped
    for step_i in range(5):
        h = 0.3 * (step_i + 1)
        depth = 8.0 - (step_i * 1.5)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -26.0 - (step_i * 0.8), h / 2.0))
        st = bpy.context.active_object
        st.scale = (32.0, depth, h)
        bpy.ops.object.transform_apply(scale=True)
        st.data.materials.append(mat_stone)
        parts.append(st)

    # Main Building Body (160m x 48m x 22.5m, from Z=1.5 to Z=24.0)
    # Divided into East, West, North wings around an interior courtyard
    # South Wing (Front Facade): 160m x 14m x 22.5m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -17.0, 12.75))
    s_wing = bpy.context.active_object
    s_wing.scale = (160.0, 14.0, 22.5)
    bpy.ops.object.transform_apply(scale=True)
    s_wing.data.materials.append(mat_brick)
    parts.append(s_wing)

    # North Wing (Rear): 160m x 14m x 22.5m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 17.0, 12.75))
    n_wing = bpy.context.active_object
    n_wing.scale = (160.0, 14.0, 22.5)
    bpy.ops.object.transform_apply(scale=True)
    n_wing.data.materials.append(mat_brick)
    parts.append(n_wing)

    # East Wing Connecting Block: 14m x 20m x 22.5m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(73.0, 0, 12.75))
    e_wing = bpy.context.active_object
    e_wing.scale = (14.0, 20.0, 22.5)
    bpy.ops.object.transform_apply(scale=True)
    e_wing.data.materials.append(mat_brick)
    parts.append(e_wing)

    # West Wing Connecting Block: 14m x 20m x 22.5m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-73.0, 0, 12.75))
    w_wing = bpy.context.active_object
    w_wing.scale = (14.0, 20.0, 22.5)
    bpy.ops.object.transform_apply(scale=True)
    w_wing.data.materials.append(mat_brick)
    parts.append(w_wing)

    # Brise-Soleil Concrete Horizontal Sun Louvers across South Facade
    # 4 floor bands + roof cornice
    for floor in range(5):
        floor_z = 2.0 + (floor * 5.2)
        # Continuous concrete fascia band
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -24.3, floor_z))
        band = bpy.context.active_object
        band.scale = (160.8, 1.2, 0.7)
        bpy.ops.object.transform_apply(scale=True)
        band.data.materials.append(mat_concrete)
        parts.append(band)

        # 3 intermediate horizontal sun louvers per floor
        if floor < 4:
            for louver_i in range(3):
                lz = floor_z + 1.2 + (louver_i * 1.2)
                bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -24.2, lz))
                lv = bpy.context.active_object
                lv.scale = (160.4, 0.9, 0.15)
                bpy.ops.object.transform_apply(scale=True)
                lv.data.materials.append(mat_concrete)
                parts.append(lv)

    # Vertical Concrete Mullions / Fin Columns along South Facade (every 8 meters)
    for col_x in range(-76, 77, 8):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(col_x, -24.2, 12.75))
        col = bpy.context.active_object
        col.scale = (0.7, 1.0, 22.5)
        bpy.ops.object.transform_apply(scale=True)
        col.data.materials.append(mat_concrete)
        parts.append(col)

    # Monumental South Entrance Portico: Double-height open columned portal (24m wide x 6m deep x 10m high)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -26.0, 6.5))
    portico = bpy.context.active_object
    portico.scale = (24.0, 4.0, 10.0)
    bpy.ops.object.transform_apply(scale=True)
    portico.data.materials.append(mat_concrete)
    parts.append(portico)

    # Entrance Portal Opening Cutout (Carved visual illusion by dark recessed lintel)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -26.5, 5.0))
    entry_recess = bpy.context.active_object
    entry_recess.scale = (18.0, 2.0, 7.0)
    bpy.ops.object.transform_apply(scale=True)
    entry_recess.data.materials.append(mat_stone)
    parts.append(entry_recess)

    # Roof Mechanical Rooms & Water Tank Penthouses
    for rx in [-40.0, 0.0, 40.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(rx, 0, 25.5))
        penthouse = bpy.context.active_object
        penthouse.scale = (16.0, 12.0, 3.0)
        bpy.ops.object.transform_apply(scale=True)
        penthouse.data.materials.append(mat_concrete)
        parts.append(penthouse)

    # Join all into single mesh
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    kala_bhaban = bpy.context.active_object
    kala_bhaban.name = "SM_KalaBhaban"

    export_fbx(kala_bhaban, "SM_KalaBhaban.fbx")

# ==============================================================================
# 2. DU CENTRAL MOSQUE
# Dimensions: 50m long x 40m wide x 26m high.
# Classical Islamic central dome (16m dia), 4 tall corner minarets, arched portals.
# ==============================================================================
def build_central_mosque():
    reset_scene()
    mat_marble = get_or_create_material("M_Shaheed_Marble", (0.92, 0.92, 0.90, 1.0), roughness=0.3)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.95, 0.95, 0.94, 1.0), roughness=0.4)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (52m x 42m x 1.2m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.6))
    plinth = bpy.context.active_object
    plinth.scale = (52.0, 42.0, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # Main Prayer Hall (44m x 34m x 14m, from Z=1.2 to Z=15.2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 8.2))
    hall = bpy.context.active_object
    hall.scale = (44.0, 34.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    hall.data.materials.append(mat_marble)
    parts.append(hall)

    # Roof Parapet Cornice with battlements / decorative frieze
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 15.6))
    cornice = bpy.context.active_object
    cornice.scale = (45.2, 35.2, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    cornice.data.materials.append(mat_trim)
    parts.append(cornice)

    # Octagonal Dome Drum Base (18m diameter, 3.5m high, Z=15.2 to 18.7)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=9.0, depth=3.5, location=(0, 0, 16.95))
    drum = bpy.context.active_object
    drum.data.materials.append(mat_trim)
    parts.append(drum)

    # Grand Central Hemispherical Dome (16m diameter, 8m high, Z=18.7 to 26.7)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=8.0, location=(0, 0, 18.7))
    dome = bpy.context.active_object
    dome.scale = (1.0, 1.0, 0.95)
    bpy.ops.object.transform_apply(scale=True)
    # Clip lower hemisphere below Z=18.7
    bm = bmesh.new()
    bm.from_mesh(dome.data)
    for v in bm.verts:
        if v.co.z < 18.7:
            v.co.z = 18.7
    bm.to_mesh(dome.data)
    bm.free()
    dome.data.materials.append(mat_marble)
    parts.append(dome)

    # Crescent / Brass Finial Spire on Dome (Z=26.0 to 29.0)
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.4, radius2=0.05, depth=3.0, location=(0, 0, 27.5))
    finial = bpy.context.active_object
    finial.data.materials.append(mat_trim)
    parts.append(finial)

    # 4 Slender Octagonal Minarets at Corners
    # Minaret positions: (+-21m, +-16m)
    for mx, my in [(-21.0, -16.0), (21.0, -16.0), (-21.0, 16.0), (21.0, 16.0)]:
        # Minaret Shaft: 2.8m diameter, 22m high (Z=1.2 to 23.2)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.4, depth=22.0, location=(mx, my, 12.2))
        shaft = bpy.context.active_object
        shaft.data.materials.append(mat_marble)
        parts.append(shaft)

        # Minaret Balcony / Gallery (Z=22.5 to 23.5)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=2.2, depth=1.0, location=(mx, my, 23.0))
        balcony = bpy.context.active_object
        balcony.data.materials.append(mat_trim)
        parts.append(balcony)

        # Minaret Conical Spire / Dome Cupola (Z=23.5 to 27.5)
        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=1.5, radius2=0.1, depth=4.0, location=(mx, my, 25.5))
        cupola = bpy.context.active_object
        cupola.data.materials.append(mat_trim)
        parts.append(cupola)

    # Symmetrical Arched Portico on Entrance Facade (South)
    for px in [-12.0, 0.0, 12.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, -17.8, 6.0))
        portal = bpy.context.active_object
        portal.scale = (8.0, 2.0, 10.0)
        bpy.ops.object.transform_apply(scale=True)
        portal.data.materials.append(mat_trim)
        parts.append(portal)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    mosque = bpy.context.active_object
    mosque.name = "SM_CentralMosque"

    export_fbx(mosque, "SM_CentralMosque.fbx")

# ==============================================================================
# 3. SALIMULLAH MUSLIM (SM) HALL
# Dimensions: 110m long x 85m wide x 18m high.
# Symmetrical colonial Indo-Saracenic quadrangle (1931 G.W. Hendry).
# Arched double-tier verandas enclosing a 70m x 50m courtyard, corner turrets.
# ==============================================================================
def build_salimullah_hall():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.58, 0.20, 0.14, 1.0), roughness=0.85)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.92, 0.90, 0.85, 1.0), roughness=0.45)
    mat_tile = get_or_create_material("M_Curzon_RoofTile", (0.42, 0.16, 0.12, 1.0), roughness=0.7)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Outer Plinth (112m x 87m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (112.0, 87.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # 4 Wings enclosing Quadrangle (Inner Quad: 72m x 47m)
    # Wing width = 16m, height = 14m (Z=1.0 to 15.0)
    # North Wing: 110m x 16m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 34.5, 8.0))
    nw = bpy.context.active_object
    nw.scale = (110.0, 16.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    nw.data.materials.append(mat_brick)
    parts.append(nw)

    # South Wing (Front Facade): 110m x 16m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -34.5, 8.0))
    sw = bpy.context.active_object
    sw.scale = (110.0, 16.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    sw.data.materials.append(mat_brick)
    parts.append(sw)

    # East Wing: 16m x 53m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(47.0, 0, 8.0))
    ew = bpy.context.active_object
    ew.scale = (16.0, 53.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ew.data.materials.append(mat_brick)
    parts.append(ew)

    # West Wing: 16m x 53m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-47.0, 0, 8.0))
    ww = bpy.context.active_object
    ww.scale = (16.0, 53.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ww.data.materials.append(mat_brick)
    parts.append(ww)

    # Pitched Terracotta Roof Eaves along all 4 wings
    for wx, wy, sx, sy in [(0, 34.5, 111.0, 17.0), (0, -34.5, 111.0, 17.0), (47.0, 0, 17.0, 54.0), (-47.0, 0, 17.0, 54.0)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(wx, wy, 15.5))
        eave = bpy.context.active_object
        eave.scale = (sx, sy, 1.2)
        bpy.ops.object.transform_apply(scale=True)
        eave.data.materials.append(mat_tile)
        parts.append(eave)

    # Monumental Central Gatehouse (South Facade Center): 24m wide x 18m deep x 18m high
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -34.5, 10.0))
    gatehouse = bpy.context.active_object
    gatehouse.scale = (24.0, 18.0, 18.0)
    bpy.ops.object.transform_apply(scale=True)
    gatehouse.data.materials.append(mat_brick)
    parts.append(gatehouse)

    # Gatehouse White Sandstone Arch Trim & Parapet
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -43.8, 18.5))
    gh_trim = bpy.context.active_object
    gh_trim.scale = (24.8, 1.2, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    gh_trim.data.materials.append(mat_trim)
    parts.append(gh_trim)

    # Grand Arched Portal Recess on South Entrance (10m wide x 12m high)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -44.0, 6.5))
    portal = bpy.context.active_object
    portal.scale = (10.0, 2.0, 11.0)
    bpy.ops.object.transform_apply(scale=True)
    portal.data.materials.append(mat_trim)
    parts.append(portal)

    # 4 Corner Octagonal Turrets with Domed Chhatris (Positions: +-53m, +-40m)
    for cx, cy in [(-53.0, -40.0), (53.0, -40.0), (-53.0, 40.0), (53.0, 40.0)]:
        # Turret Tower (4.0m dia x 17m high)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=2.0, depth=17.0, location=(cx, cy, 9.5))
        turret = bpy.context.active_object
        turret.data.materials.append(mat_brick)
        parts.append(turret)

        # Chhatri Domed Cap (Z=18.0 to 21.0)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=2.4, location=(cx, cy, 18.5))
        cap = bpy.context.active_object
        cap.scale = (1.0, 1.0, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        cap.data.materials.append(mat_trim)
        parts.append(cap)

    # Gatehouse Twin Accent Chhatris (Z=19.0 to 22.0)
    for gx in [-10.0, 10.0]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.6, depth=4.0, location=(gx, -42.0, 20.0))
        g_turret = bpy.context.active_object
        g_turret.data.materials.append(mat_trim)
        parts.append(g_turret)

        bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=1.8, radius2=0.05, depth=2.5, location=(gx, -42.0, 22.5))
        g_cone = bpy.context.active_object
        g_cone.data.materials.append(mat_trim)
        parts.append(g_cone)

    # Interior Courtyard Colonnade Verandas (White arched horizontal bands along quad)
    for qx, qy, qsx, qsy in [(0, 26.0, 72.0, 1.2), (0, -26.0, 72.0, 1.2), (38.5, 0, 1.2, 47.0), (-38.5, 0, 1.2, 47.0)]:
        # Tier 1 band
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(qx, qy, 6.0))
        t1 = bpy.context.active_object
        t1.scale = (qsx, qsy, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        t1.data.materials.append(mat_trim)
        parts.append(t1)
        # Tier 2 band
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(qx, qy, 12.0))
        t2 = bpy.context.active_object
        t2.scale = (qsx, qsy, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        t2.data.materials.append(mat_trim)
        parts.append(t2)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    sm_hall = bpy.context.active_object
    sm_hall.name = "SM_SalimullahMuslim_Hall"

    export_fbx(sm_hall, "SM_SalimullahMuslim_Hall.fbx")

# ==============================================================================
# 4. DR. MUHAMMAD SHAHIDULLAH HALL
# Dimensions: 90m long x 70m wide x 16m high.
# Colonial red brick quadrangle with arched verandas and heritage entrance portal.
# ==============================================================================
def build_shahidullah_hall():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.56, 0.19, 0.13, 1.0), roughness=0.85)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.91, 0.89, 0.84, 1.0), roughness=0.45)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (92m x 72m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (92.0, 72.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # 4 Wings around inner quad (inner quad: 60m x 40m)
    # North Wing: 90m x 15m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 27.5, 8.0))
    nw = bpy.context.active_object
    nw.scale = (90.0, 15.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    nw.data.materials.append(mat_brick)
    parts.append(nw)

    # South Wing: 90m x 15m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -27.5, 8.0))
    sw = bpy.context.active_object
    sw.scale = (90.0, 15.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    sw.data.materials.append(mat_brick)
    parts.append(sw)

    # East Wing: 15m x 40m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(37.5, 0, 8.0))
    ew = bpy.context.active_object
    ew.scale = (15.0, 40.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ew.data.materials.append(mat_brick)
    parts.append(ew)

    # West Wing: 15m x 40m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-37.5, 0, 8.0))
    ww = bpy.context.active_object
    ww.scale = (15.0, 40.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ww.data.materials.append(mat_brick)
    parts.append(ww)

    # Central Arched Entrance Block (South Facade)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -27.5, 9.5))
    ent = bpy.context.active_object
    ent.scale = (20.0, 17.0, 17.0)
    bpy.ops.object.transform_apply(scale=True)
    ent.data.materials.append(mat_brick)
    parts.append(ent)

    # Entrance White Cornice
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -36.2, 17.5))
    cornice = bpy.context.active_object
    cornice.scale = (20.6, 1.2, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    cornice.data.materials.append(mat_trim)
    parts.append(cornice)

    # 4 Corner Octagonal Turrets (Z=1.0 to 17.0)
    for tx, ty in [(-43.0, -33.0), (43.0, -33.0), (-43.0, 33.0), (43.0, 33.0)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.8, depth=16.0, location=(tx, ty, 9.0))
        turret = bpy.context.active_object
        turret.data.materials.append(mat_trim)
        parts.append(turret)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    sh_hall = bpy.context.active_object
    sh_hall.name = "SM_Shahidullah_Hall"

    export_fbx(sh_hall, "SM_Shahidullah_Hall.fbx")

# ==============================================================================
# 5. CURZON SCIENCE ANNEX (PHYSICS & CHEMISTRY DEPARTMENTS)
# Dimensions: 80m long x 35m wide x 14m high. 2-storey Indo-Saracenic block.
# ==============================================================================
def build_curzon_science_annex():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.57, 0.18, 0.13, 1.0), roughness=0.85)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.92, 0.90, 0.85, 1.0), roughness=0.45)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (82m x 37m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (82.0, 37.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # Main 2-Storey Block (80m x 35m x 13m, Z=1.0 to 14.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 7.5))
    body = bpy.context.active_object
    body.scale = (80.0, 35.0, 13.0)
    bpy.ops.object.transform_apply(scale=True)
    body.data.materials.append(mat_brick)
    parts.append(body)

    # White Sandstone Stringcourses (Floor dividing band & roof parapet band)
    for bz in [7.0, 13.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, bz))
        band = bpy.context.active_object
        band.scale = (81.2, 36.2, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        band.data.materials.append(mat_trim)
        parts.append(band)

    # Front Veranda Bays / Colonnade Rhythm along South Facade
    for vx in range(-35, 36, 10):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(vx, -17.8, 7.5))
        pilaster = bpy.context.active_object
        pilaster.scale = (1.2, 1.0, 13.0)
        bpy.ops.object.transform_apply(scale=True)
        pilaster.data.materials.append(mat_trim)
        parts.append(pilaster)

    # Central Entrance Portico
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -19.5, 7.5))
    portico = bpy.context.active_object
    portico.scale = (16.0, 4.0, 13.5)
    bpy.ops.object.transform_apply(scale=True)
    portico.data.materials.append(mat_brick)
    parts.append(portico)

    # Portico Roof Chhatri (Z=14.0 to 18.0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=3.0, depth=2.0, location=(0, -19.5, 15.0))
    ch_base = bpy.context.active_object
    ch_base.data.materials.append(mat_trim)
    parts.append(ch_base)

    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=3.2, location=(0, -19.5, 16.5))
    ch_dome = bpy.context.active_object
    ch_dome.scale = (1.0, 1.0, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    ch_dome.data.materials.append(mat_trim)
    parts.append(ch_dome)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    annex = bpy.context.active_object
    annex.name = "SM_Curzon_ScienceAnnex"

    export_fbx(annex, "SM_Curzon_ScienceAnnex.fbx")

# ==============================================================================
# 6. JAGANNATH HALL COMPLEX
# Dimensions: 95m long x 75m wide x 16m high.
# Heritage colonial red-brick quadrangle with interior courtyard & prayer hall.
# ==============================================================================
def build_jagannath_hall():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.57, 0.19, 0.13, 1.0), roughness=0.85)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.91, 0.89, 0.84, 1.0), roughness=0.45)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (97m x 77m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (97.0, 77.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # 4 Residential Wings (Inner Quad: 65m x 45m)
    # North Wing: 95m x 15m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 30.0, 8.0))
    nw = bpy.context.active_object
    nw.scale = (95.0, 15.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    nw.data.materials.append(mat_brick)
    parts.append(nw)

    # South Wing: 95m x 15m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -30.0, 8.0))
    sw = bpy.context.active_object
    sw.scale = (95.0, 15.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    sw.data.materials.append(mat_brick)
    parts.append(sw)

    # East Wing: 15m x 45m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(40.0, 0, 8.0))
    ew = bpy.context.active_object
    ew.scale = (15.0, 45.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ew.data.materials.append(mat_brick)
    parts.append(ew)

    # West Wing: 15m x 45m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-40.0, 0, 8.0))
    ww = bpy.context.active_object
    ww.scale = (15.0, 45.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ww.data.materials.append(mat_brick)
    parts.append(ww)

    # Monumental Prayer Hall Pavilion in North Wing Center (20m x 20m x 18m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 30.0, 10.0))
    prayer_hall = bpy.context.active_object
    prayer_hall.scale = (22.0, 18.0, 18.0)
    bpy.ops.object.transform_apply(scale=True)
    prayer_hall.data.materials.append(mat_brick)
    parts.append(prayer_hall)

    # Prayer Hall White Octagonal Dome (Z=18.0 to 22.5)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=4.5, depth=4.0, location=(0, 30.0, 20.0))
    dome = bpy.context.active_object
    dome.data.materials.append(mat_trim)
    parts.append(dome)

    # Cornice trim along all wings
    for cx, cy, sx, sy in [(0, 30.0, 96.0, 16.0), (0, -30.0, 96.0, 16.0), (40.0, 0, 16.0, 46.0), (-40.0, 0, 16.0, 46.0)]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, 14.5))
        c = bpy.context.active_object
        c.scale = (sx, sy, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        c.data.materials.append(mat_trim)
        parts.append(c)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    j_hall = bpy.context.active_object
    j_hall.name = "SM_Jagannath_Hall"

    export_fbx(j_hall, "SM_Jagannath_Hall.fbx")

# ==============================================================================
# 7. ROKEYA HALL COMPLEX
# Dimensions: 85m long x 60m wide x 15m high.
# Historic colonial red-brick women's residential hall along Fuller Road.
# ==============================================================================
def build_rokeya_hall():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.57, 0.18, 0.13, 1.0), roughness=0.85)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.91, 0.89, 0.84, 1.0), roughness=0.45)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (87m x 62m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (87.0, 62.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # Main U-Shaped Complex (East, West, and Central wings)
    # Central Main Wing: 85m x 16m x 14m (Z=1.0 to 15.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 22.0, 8.0))
    mw = bpy.context.active_object
    mw.scale = (85.0, 16.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    mw.data.materials.append(mat_brick)
    parts.append(mw)

    # East Flanking Wing: 16m x 36m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(34.5, -4.0, 8.0))
    ew = bpy.context.active_object
    ew.scale = (16.0, 36.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ew.data.materials.append(mat_brick)
    parts.append(ew)

    # West Flanking Wing: 16m x 36m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-34.5, -4.0, 8.0))
    ww = bpy.context.active_object
    ww.scale = (16.0, 36.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    ww.data.materials.append(mat_brick)
    parts.append(ww)

    # Front Enclosed Security Gatehouse & Wall
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -22.0, 4.0))
    gate = bpy.context.active_object
    gate.scale = (85.0, 2.0, 7.0)
    bpy.ops.object.transform_apply(scale=True)
    gate.data.materials.append(mat_brick)
    parts.append(gate)

    # Decorative White Cornice Bands
    for bz in [7.5, 14.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 22.0, bz))
        b = bpy.context.active_object
        b.scale = (86.0, 17.0, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        b.data.materials.append(mat_trim)
        parts.append(b)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    r_hall = bpy.context.active_object
    r_hall.name = "SM_Rokeya_Hall"

    export_fbx(r_hall, "SM_Rokeya_Hall.fbx")

# ==============================================================================
# 8. SURJA SEN & MOHSIN HALLS (MODERNIST RESIDENTIAL BLOCKS)
# Dimensions: 90m long x 70m wide x 18m high. 5-storey modernist quad.
# ==============================================================================
def build_surjasen_hall():
    reset_scene()
    mat_support = get_or_create_material("M_Supporting_Building", (0.75, 0.73, 0.70, 1.0), roughness=0.65)
    mat_modern = get_or_create_material("M_Hero_Modern", (0.85, 0.84, 0.80, 1.0), roughness=0.55)
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.55, 0.18, 0.12, 1.0), roughness=0.85)

    parts = []

    # Plinth Base (92m x 72m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (92.0, 72.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_support)
    parts.append(plinth)

    # 4 Wings around central sports courtyard (Inner Quad: 60m x 40m)
    # 5 storeys, total height = 18m (Z=1.0 to 19.0)
    # North Wing: 90m x 15m x 18m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 27.5, 10.0))
    nw = bpy.context.active_object
    nw.scale = (90.0, 15.0, 18.0)
    bpy.ops.object.transform_apply(scale=True)
    nw.data.materials.append(mat_support)
    parts.append(nw)

    # South Wing: 90m x 15m x 18m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -27.5, 10.0))
    sw = bpy.context.active_object
    sw.scale = (90.0, 15.0, 18.0)
    bpy.ops.object.transform_apply(scale=True)
    sw.data.materials.append(mat_support)
    parts.append(sw)

    # East Wing: 15m x 40m x 18m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(37.5, 0, 10.0))
    ew = bpy.context.active_object
    ew.scale = (15.0, 40.0, 18.0)
    bpy.ops.object.transform_apply(scale=True)
    ew.data.materials.append(mat_support)
    parts.append(ew)

    # West Wing: 15m x 40m x 18m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-37.5, 0, 10.0))
    ww = bpy.context.active_object
    ww.scale = (15.0, 40.0, 18.0)
    bpy.ops.object.transform_apply(scale=True)
    ww.data.materials.append(mat_support)
    parts.append(ww)

    # Horizontal Balcony Louver Bands across North & South Facades (5 storeys)
    for fl in range(5):
        fz = 2.0 + (fl * 3.4)
        for fy in [-35.4, 35.4]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, fy, fz))
            balc = bpy.context.active_object
            balc.scale = (88.0, 1.2, 0.9)
            bpy.ops.object.transform_apply(scale=True)
            balc.data.materials.append(mat_modern)
            parts.append(balc)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    surjasen = bpy.context.active_object
    surjasen.name = "SM_SurjaSen_Hall"

    export_fbx(surjasen, "SM_SurjaSen_Hall.fbx")

# ==============================================================================
# 9. DU ADMINISTRATIVE BUILDING (REGISTRAR BHABAN)
# Dimensions: 75m long x 45m wide x 16m high. 4-storey modernist block.
# ==============================================================================
def build_admin_building():
    reset_scene()
    mat_modern = get_or_create_material("M_Hero_Modern", (0.84, 0.83, 0.80, 1.0), roughness=0.55)
    mat_support = get_or_create_material("M_Supporting_Building", (0.75, 0.73, 0.70, 1.0), roughness=0.65)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (77m x 47m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (77.0, 47.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # Main Body (75m x 45m x 15m, Z=1.0 to 16.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 8.5))
    body = bpy.context.active_object
    body.scale = (75.0, 45.0, 15.0)
    bpy.ops.object.transform_apply(scale=True)
    body.data.materials.append(mat_support)
    parts.append(body)

    # Continuous Ribbon Window Bands / Concrete Sunshades (4 storeys)
    for fl in range(4):
        fz = 2.5 + (fl * 3.4)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -22.8, fz))
        shade = bpy.context.active_object
        shade.scale = (75.6, 1.2, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        shade.data.materials.append(mat_modern)
        parts.append(shade)

    # Central Entrance Portico & Clock Tower (16m wide x 8m deep x 21m high)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -22.0, 11.0))
    tower = bpy.context.active_object
    tower.scale = (16.0, 6.0, 20.0)
    bpy.ops.object.transform_apply(scale=True)
    tower.data.materials.append(mat_modern)
    parts.append(tower)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    admin = bpy.context.active_object
    admin.name = "SM_Admin_Building"

    export_fbx(admin, "SM_Admin_Building.fbx")

# ==============================================================================
# 10. IBA BUILDING COMPLEX
# Dimensions: 65m long x 40m wide x 15m high.
# Exposed red-brick modernist academic facility along University Avenue.
# ==============================================================================
def build_iba_building():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.55, 0.18, 0.12, 1.0), roughness=0.85)
    mat_modern = get_or_create_material("M_Hero_Modern", (0.84, 0.83, 0.80, 1.0), roughness=0.55)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (67m x 42m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (67.0, 42.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # Main Academic Block (65m x 40m x 14m, Z=1.0 to 15.0)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 8.0))
    body = bpy.context.active_object
    body.scale = (65.0, 40.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)
    body.data.materials.append(mat_brick)
    parts.append(body)

    # Cantilevered Concrete Floor Bands
    for fz in [5.5, 10.0, 14.5]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -20.4, fz))
        b = bpy.context.active_object
        b.scale = (65.6, 1.2, 0.6)
        bpy.ops.object.transform_apply(scale=True)
        b.data.materials.append(mat_modern)
        parts.append(b)

    # Entrance Atrium / Glass Canopy Frame
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -22.0, 4.5))
    canopy = bpy.context.active_object
    canopy.scale = (20.0, 5.0, 7.0)
    bpy.ops.object.transform_apply(scale=True)
    canopy.data.materials.append(mat_modern)
    parts.append(canopy)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    iba = bpy.context.active_object
    iba.name = "SM_IBA_Building"

    export_fbx(iba, "SM_IBA_Building.fbx")

# ==============================================================================
# 11. BANGLA ACADEMY COMPLEX (BURDWAN HOUSE & MODERN HALL)
# Dimensions: 85m long x 55m wide x 16m high.
# Colonial heritage residence with surrounding modern conference facilities.
# ==============================================================================
def build_bangla_academy():
    reset_scene()
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.92, 0.90, 0.85, 1.0), roughness=0.45)
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.56, 0.19, 0.13, 1.0), roughness=0.85)
    mat_stone = get_or_create_material("M_Curzon_StonePaving", (0.45, 0.43, 0.40, 1.0), roughness=0.7)

    parts = []

    # Plinth Base (87m x 57m x 1.0m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    plinth = bpy.context.active_object
    plinth.scale = (87.0, 57.0, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    plinth.data.materials.append(mat_stone)
    parts.append(plinth)

    # Historic Burdwan House Pavilion (South Wing): 45m x 25m x 14m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-15.0, -12.0, 7.5))
    burdwan = bpy.context.active_object
    burdwan.scale = (45.0, 25.0, 13.0)
    bpy.ops.object.transform_apply(scale=True)
    burdwan.data.materials.append(mat_trim)
    parts.append(burdwan)

    # Modern Auditorium / Library Wing (North Wing): 75m x 25m x 15m
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 14.0, 8.5))
    auditorium = bpy.context.active_object
    auditorium.scale = (75.0, 25.0, 15.0)
    bpy.ops.object.transform_apply(scale=True)
    auditorium.data.materials.append(mat_brick)
    parts.append(auditorium)

    # Colonial Veranda Colonnade on Burdwan House
    for cx in range(-32, 5, 6):
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.6, depth=12.0, location=(cx, -25.2, 7.0))
        col = bpy.context.active_object
        col.data.materials.append(mat_trim)
        parts.append(col)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    ba = bpy.context.active_object
    ba.name = "SM_BanglaAcademy"

    export_fbx(ba, "SM_BanglaAcademy.fbx")

# ==============================================================================
# 12. CAMPUS BOUNDARY WALL (MODULAR 20M BAY)
# 20m long x 0.6m thick x 2.4m high with brick pillars & wrought iron railings.
# ==============================================================================
def build_boundary_wall():
    reset_scene()
    mat_brick = get_or_create_material("M_Curzon_Brick", (0.56, 0.19, 0.13, 1.0), roughness=0.85)
    mat_iron = get_or_create_material("M_Curzon_CastIron", (0.15, 0.15, 0.16, 1.0), roughness=0.35, metallic=0.9)
    mat_trim = get_or_create_material("M_Curzon_WhiteTrim", (0.92, 0.90, 0.85, 1.0), roughness=0.45)

    parts = []

    # Concrete Low Base Wall (20m x 0.5m x 0.8m, Z=0 to 0.8)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.4))
    base = bpy.context.active_object
    base.scale = (20.0, 0.5, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    base.data.materials.append(mat_brick)
    parts.append(base)

    # 5 Red-brick pillars along 20m (every 5 meters: -10, -5, 0, 5, 10)
    for px in [-10.0, -5.0, 0.0, 5.0, 10.0]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, 0, 1.3))
        pillar = bpy.context.active_object
        pillar.scale = (0.7, 0.7, 2.6)
        bpy.ops.object.transform_apply(scale=True)
        pillar.data.materials.append(mat_brick)
        parts.append(pillar)

        # White stone pyramidal cap
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.5, radius2=0.05, depth=0.4, location=(px, 0, 2.7))
        cap = bpy.context.active_object
        cap.rotation_euler = (0, 0, math.pi / 4.0)
        bpy.ops.object.transform_apply(rotation=True)
        cap.data.materials.append(mat_trim)
        parts.append(cap)

    # Wrought Iron Spear-Topped Railings between pillars
    for span in [(-7.5, 4.3), (-2.5, 4.3), (2.5, 4.3), (7.5, 4.3)]:
        # Horizontal iron rails (top and bottom)
        for rz in [1.0, 2.2]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(span[0], 0, rz))
            rail = bpy.context.active_object
            rail.scale = (span[1], 0.08, 0.08)
            bpy.ops.object.transform_apply(scale=True)
            rail.data.materials.append(mat_iron)
            parts.append(rail)

        # Vertical iron pickets (every 0.4m)
        p_count = int(span[1] / 0.4)
        for pi in range(p_count):
            pick_x = (span[0] - (span[1] / 2.0)) + 0.2 + (pi * 0.4)
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.03, depth=1.5, location=(pick_x, 0, 1.6))
            picket = bpy.context.active_object
            picket.data.materials.append(mat_iron)
            parts.append(picket)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    wall = bpy.context.active_object
    wall.name = "SM_Campus_BoundaryWall"

    export_fbx(wall, "SM_Campus_BoundaryWall.fbx")

# ==============================================================================
# 13. CAMPUS SKYLINE SILHOUETTE (PERIPHERAL CITY CONTEXT)
# 250m long x 40m deep x 45m high low-draw-call urban facade silhouette.
# ==============================================================================
def build_campus_skyline():
    reset_scene()
    mat_support = get_or_create_material("M_Supporting_Building", (0.70, 0.69, 0.66, 1.0), roughness=0.8)
    mat_modern = get_or_create_material("M_Hero_Modern", (0.80, 0.79, 0.76, 1.0), roughness=0.7)

    parts = []

    # Array of varied-height city buildings forming an authentic skyline
    # Total width = 260m
    building_configs = [
        (-110.0, 32.0, 24.0, 38.0),
        (-75.0, 28.0, 28.0, 48.0),
        (-45.0, 26.0, 22.0, 32.0),
        (-18.0, 24.0, 25.0, 44.0),
        (10.0, 30.0, 26.0, 52.0),
        (42.0, 28.0, 22.0, 35.0),
        (72.0, 32.0, 28.0, 46.0),
        (105.0, 28.0, 24.0, 36.0),
    ]

    for bx, bw, bd, bh in building_configs:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, bh / 2.0))
        b = bpy.context.active_object
        b.scale = (bw, bd, bh)
        bpy.ops.object.transform_apply(scale=True)
        b.data.materials.append(mat_support if bh < 40.0 else mat_modern)
        parts.append(b)

        # Rooftop tank / antenna / parapet detail
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, 0, bh + 2.0))
        tank = bpy.context.active_object
        tank.scale = (bw * 0.4, bd * 0.4, 4.0)
        bpy.ops.object.transform_apply(scale=True)
        tank.data.materials.append(mat_support)
        parts.append(tank)

    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    skyline = bpy.context.active_object
    skyline.name = "SM_Campus_Skyline"

    export_fbx(skyline, "SM_Campus_Skyline.fbx")

# ==============================================================================
# MAIN EXECUTION ENTRYPOINT
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("STARTING FULL CAMPUS ASSET MODELING PIPELINE...")
    print("=" * 70)

    generators = [
        ("1. Kala Bhaban (Arts Faculty)", build_kala_bhaban),
        ("2. DU Central Mosque", build_central_mosque),
        ("3. Salimullah Muslim (SM) Hall", build_salimullah_hall),
        ("4. Dr. M. Shahidullah Hall", build_shahidullah_hall),
        ("5. Curzon Science Annex", build_curzon_science_annex),
        ("6. Jagannath Hall Complex", build_jagannath_hall),
        ("7. Rokeya Hall Complex", build_rokeya_hall),
        ("8. Surja Sen & Mohsin Halls", build_surjasen_hall),
        ("9. DU Administrative Building", build_admin_building),
        ("10. IBA Building Complex", build_iba_building),
        ("11. Bangla Academy Complex", build_bangla_academy),
        ("12. Campus Boundary Wall", build_boundary_wall),
        ("13. Campus Skyline Backdrop", build_campus_skyline)
    ]

    for label, gen_func in generators:
        print(f"\n--- Generating {label} ---")
        try:
            gen_func()
            print(f"SUCCESS: {label} generated.")
        except Exception as e:
            print(f"ERROR in {label}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("ALL 13 FULL CAMPUS ARCHITECTURAL ASSETS GENERATED!")
    print("=" * 70)
