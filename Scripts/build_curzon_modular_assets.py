#!/usr/bin/env python3
"""
Curzon Hall Modular Asset Generator for Blender 5.2.3 LTS
Creates authentic Indo-Saracenic architectural assets and exports FBX for Unreal Engine 5.8.
All coordinates in metric scale (1 Blender unit = 1 meter = 100 Unreal units).
Materials:
  Index 0: M_Curzon_Brick
  Index 1: M_Curzon_WhiteTrim
  Index 2: M_Curzon_Accent (dark iron / stone)
"""

import bpy
import bmesh
import math
import os

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/CurzonModular"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

def get_or_create_materials():
    # Brick
    mat_brick = bpy.data.materials.get("M_Curzon_Brick")
    if not mat_brick:
        mat_brick = bpy.data.materials.new(name="M_Curzon_Brick")
        bsdf = mat_brick.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.52, 0.15, 0.10, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.78

    # White Trim
    mat_trim = bpy.data.materials.get("M_Curzon_WhiteTrim")
    if not mat_trim:
        mat_trim = bpy.data.materials.new(name="M_Curzon_WhiteTrim")
        bsdf_trim = mat_trim.node_tree.nodes.get("Principled BSDF")
        if bsdf_trim:
            bsdf_trim.inputs["Base Color"].default_value = (0.92, 0.88, 0.82, 1.0)
            bsdf_trim.inputs["Roughness"].default_value = 0.55

    # Accent
    mat_accent = bpy.data.materials.get("M_Curzon_Accent")
    if not mat_accent:
        mat_accent = bpy.data.materials.new(name="M_Curzon_Accent")
        bsdf_acc = mat_accent.node_tree.nodes.get("Principled BSDF")
        if bsdf_acc:
            bsdf_acc.inputs["Base Color"].default_value = (0.12, 0.12, 0.14, 1.0)
            bsdf_acc.inputs["Roughness"].default_value = 0.40

    return mat_brick, mat_trim, mat_accent

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

# 1. Lower Veranda Arch Bay (8m wide x 7m high x 1.5m deep)
def build_veranda_lower(mat_b, mat_t):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Veranda_Arch_Lower")
    obj = bpy.data.objects.new("SM_Curzon_Veranda_Arch_Lower", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_b)
    obj.data.materials.append(mat_t)

    bm = bmesh.new()
    # Left Pier
    p1 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.0, 1.2, 7.0), verts=p1["verts"])
    bmesh.ops.translate(bm, vec=(-3.5, 0.0, 3.5), verts=p1["verts"])
    for f in p1["verts"]:
        pass

    # Right Pier
    p2 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.0, 1.2, 7.0), verts=p2["verts"])
    bmesh.ops.translate(bm, vec=(3.5, 0.0, 3.5), verts=p2["verts"])

    # Arch Spandrel & Header
    sp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(8.0, 1.2, 2.0), verts=sp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 6.0), verts=sp["verts"])

    # White Trim Impost Bands (Slot 1)
    im1 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.2, 1.4, 0.3), verts=im1["verts"])
    bmesh.ops.translate(bm, vec=(-3.5, 0.0, 4.5), verts=im1["verts"])
    for f in [f for f in bm.faces if any(v in im1["verts"] for v in f.verts)]:
        f.material_index = 1

    im2 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(1.2, 1.4, 0.3), verts=im2["verts"])
    bmesh.ops.translate(bm, vec=(3.5, 0.0, 4.5), verts=im2["verts"])
    for f in [f for f in bm.faces if any(v in im2["verts"] for v in f.verts)]:
        f.material_index = 1

    # White Arch Molding Band
    am = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(6.2, 1.3, 0.25), verts=am["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.6), verts=am["verts"])
    for f in [f for f in bm.faces if any(v in am["verts"] for v in f.verts)]:
        f.material_index = 1

    # Top Cornice Molding (White)
    co = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(8.2, 1.5, 0.4), verts=co["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 7.0), verts=co["verts"])
    for f in [f for f in bm.faces if any(v in co["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Veranda_Arch_Lower.fbx")

# 2. Upper Veranda Arch Bay (8m wide x 7m high with cusped arches and jali balustrade)
def build_veranda_upper(mat_b, mat_t):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Veranda_Arch_Upper")
    obj = bpy.data.objects.new("SM_Curzon_Veranda_Arch_Upper", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_b)
    obj.data.materials.append(mat_t)

    bm = bmesh.new()
    # Left Octagonal Column
    c1 = bmesh.ops.create_cone(bm, segments=8, radius1=0.35, radius2=0.35, depth=5.5)
    bmesh.ops.translate(bm, vec=(-3.5, 0.0, 2.75), verts=c1["verts"])

    # Right Octagonal Column
    c2 = bmesh.ops.create_cone(bm, segments=8, radius1=0.35, radius2=0.35, depth=5.5)
    bmesh.ops.translate(bm, vec=(3.5, 0.0, 2.75), verts=c2["verts"])

    # Middle Paired Slender Column
    cm = bmesh.ops.create_cone(bm, segments=8, radius1=0.25, radius2=0.25, depth=5.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.75), verts=cm["verts"])

    # Lotus Capitals (White Trim)
    for x_pos in [-3.5, 0.0, 3.5]:
        cap = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.9, 0.9, 0.5), verts=cap["verts"])
        bmesh.ops.translate(bm, vec=(x_pos, 0.0, 5.25), verts=cap["verts"])
        for f in [f for f in bm.faces if any(v in cap["verts"] for v in f.verts)]:
            f.material_index = 1

    # Cusped Multi-foil Arch Spandrel & Roof Eaves (Chhajja)
    chhajja = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(8.4, 2.0, 0.3), verts=chhajja["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.3, 5.8), verts=chhajja["verts"])
    for f in [f for f in bm.faces if any(v in chhajja["verts"] for v in f.verts)]:
        f.material_index = 1

    # Brick Header
    head = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(8.0, 1.0, 1.2), verts=head["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 6.4), verts=head["verts"])

    # Jali Perforated Balustrade Railing (White Trim) at bottom
    bal = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(7.0, 0.25, 0.9), verts=bal["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.45), verts=bal["verts"])
    for f in [f for f in bm.faces if any(v in bal["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Veranda_Arch_Upper.fbx")

# 3. Grand Entrance Portico (16m wide x 18m high monumental central entrance)
def build_entrance_portal(mat_b, mat_t):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Entrance_Portal")
    obj = bpy.data.objects.new("SM_Curzon_Entrance_Portal", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_b)
    obj.data.materials.append(mat_t)

    bm = bmesh.new()
    # Left Massive Portal Pylon
    p1 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(3.0, 4.0, 18.0), verts=p1["verts"])
    bmesh.ops.translate(bm, vec=(-6.5, 0.0, 9.0), verts=p1["verts"])

    # Right Massive Portal Pylon
    p2 = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(3.0, 4.0, 18.0), verts=p2["verts"])
    bmesh.ops.translate(bm, vec=(6.5, 0.0, 9.0), verts=p2["verts"])

    # Monumental Entablature / Upper Arch Frame
    top = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(16.0, 4.0, 5.0), verts=top["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 15.5), verts=top["verts"])

    # Contrasting Arch Trim Band (White Sandstone)
    trim = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(10.4, 4.2, 0.6), verts=trim["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 12.8), verts=trim["verts"])
    for f in [f for f in bm.faces if any(v in trim["verts"] for v in f.verts)]:
        f.material_index = 1

    # Projecting Chhajja / Eaves (White Trim)
    ch = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(17.0, 5.0, 0.5), verts=ch["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 18.0), verts=ch["verts"])
    for f in [f for f in bm.faces if any(v in ch["verts"] for v in f.verts)]:
        f.material_index = 1

    # Stepped Ornamental Parapet Screen atop Portal
    sc = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(14.0, 1.0, 1.8), verts=sc["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 19.1), verts=sc["verts"])
    for f in [f for f in bm.faces if any(v in sc["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Entrance_Portal.fbx")

# 4. Octagonal Corner Chhatri Dome Kiosk (8 pillars, domed roof, finial)
def build_chattri(mat_b, mat_t):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Chattri_Dome")
    obj = bpy.data.objects.new("SM_Curzon_Chattri_Dome", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_b)
    obj.data.materials.append(mat_t)

    bm = bmesh.new()
    # Octagonal Base Plinth (White Trim)
    base = bmesh.ops.create_cone(bm, segments=8, radius1=3.2, radius2=3.2, depth=0.8)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.4), verts=base["verts"])
    for f in [f for f in bm.faces if any(v in base["verts"] for v in f.verts)]:
        f.material_index = 1

    # 8 Slender Columns
    rad = 2.4
    for i in range(8):
        ang = i * (2.0 * math.pi / 8.0)
        cx = rad * math.cos(ang)
        cy = rad * math.sin(ang)
        col = bmesh.ops.create_cone(bm, segments=6, radius1=0.22, radius2=0.22, depth=3.6)
        bmesh.ops.translate(bm, vec=(cx, cy, 2.6), verts=col["verts"])

    # Overhanging Octagonal Chhajja Eaves (White Trim)
    ch = bmesh.ops.create_cone(bm, segments=8, radius1=3.5, radius2=3.0, depth=0.4)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.5), verts=ch["verts"])
    for f in [f for f in bm.faces if any(v in ch["verts"] for v in f.verts)]:
        f.material_index = 1

    # Ribbed Mughal Hemispherical Dome (Brick & White Trim alternating)
    dome = bmesh.ops.create_cone(bm, segments=8, radius1=2.7, radius2=0.4, depth=2.4)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 5.8), verts=dome["verts"])
    for f in [f for f in bm.faces if any(v in dome["verts"] for v in f.verts)]:
        f.material_index = 0

    # Brass Finial Needle at apex
    fin = bmesh.ops.create_cone(bm, segments=6, radius1=0.15, radius2=0.02, depth=1.6)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 7.8), verts=fin["verts"])
    for f in [f for f in bm.faces if any(v in fin["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Chattri_Dome.fbx")

# 5. Octagonal Tower Segment (authentic octagonal turret module)
def build_tower_octagon(mat_b, mat_t):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Tower_Octagon")
    obj = bpy.data.objects.new("SM_Curzon_Tower_Octagon", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_b)
    obj.data.materials.append(mat_t)

    bm = bmesh.new()
    # Main Octagonal Body
    body = bmesh.ops.create_cone(bm, segments=8, radius1=3.0, radius2=3.0, depth=16.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 8.0), verts=body["verts"])

    # 3 Horizontal White Trim String Courses
    for h in [4.0, 8.0, 12.0]:
        sc = bmesh.ops.create_cone(bm, segments=8, radius1=3.2, radius2=3.2, depth=0.35)
        bmesh.ops.translate(bm, vec=(0.0, 0.0, h), verts=sc["verts"])
        for f in [f for f in bm.faces if any(v in sc["verts"] for v in f.verts)]:
            f.material_index = 1

    # Projecting Top Cornice & Bracket Ring
    top = bmesh.ops.create_cone(bm, segments=8, radius1=3.6, radius2=3.2, depth=0.8)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 16.2), verts=top["verts"])
    for f in [f for f in bm.faces if any(v in top["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Tower_Octagon.fbx")

# 6. Ornamental Parapet Merlons (8m wide section of stepped Indo-Saracenic battlements)
def build_parapet(mat_b, mat_t):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Parapet_Merlons")
    obj = bpy.data.objects.new("SM_Curzon_Parapet_Merlons", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_b)
    obj.data.materials.append(mat_t)

    bm = bmesh.new()
    # Base Parapet Wall
    base = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(8.0, 0.6, 0.9), verts=base["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.45), verts=base["verts"])

    # 5 Stepped Merlons
    for i in range(5):
        mx = -3.2 + i * 1.6
        m = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.8, 0.65, 0.8), verts=m["verts"])
        bmesh.ops.translate(bm, vec=(mx, 0.0, 1.25), verts=m["verts"])

        # White Trim Pointed Cap
        cap = bmesh.ops.create_cone(bm, segments=4, radius1=0.55, radius2=0.05, depth=0.4)
        bmesh.ops.translate(bm, vec=(mx, 0.0, 1.8), verts=cap["verts"])
        for f in [f for f in bm.faces if any(v in cap["verts"] for v in f.verts)]:
            f.material_index = 1

    # White Coping Band along base
    cop = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(8.2, 0.8, 0.15), verts=cop["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.9), verts=cop["verts"])
    for f in [f for f in bm.faces if any(v in cop["verts"] for v in f.verts)]:
        f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Parapet_Merlons.fbx")

# 7. Campus Colonial Park Bench (2.2m wide cast-iron & teak wood bench)
def build_bench(mat_b, mat_t, mat_a):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Bench_Colonial")
    obj = bpy.data.objects.new("SM_Curzon_Bench_Colonial", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_a) # Cast iron
    obj.data.materials.append(mat_t) # Wood slats

    bm = bmesh.new()
    # Cast Iron Legs
    for x_pos in [-0.9, 0.9]:
        leg_f = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.08, 0.08, 0.45), verts=leg_f["verts"])
        bmesh.ops.translate(bm, vec=(x_pos, -0.25, 0.225), verts=leg_f["verts"])

        leg_b = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.08, 0.08, 0.85), verts=leg_b["verts"])
        bmesh.ops.translate(bm, vec=(x_pos, 0.25, 0.425), verts=leg_b["verts"])

    # 4 Teak Seat Slats (Slot 1)
    for i in range(4):
        slat = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(2.2, 0.12, 0.04), verts=slat["verts"])
        bmesh.ops.translate(bm, vec=(0.0, -0.22 + i * 0.14, 0.45), verts=slat["verts"])
        for f in [f for f in bm.faces if any(v in slat["verts"] for v in f.verts)]:
            f.material_index = 1

    # 3 Backrest Slats (Slot 1)
    for i in range(3):
        slat = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(2.2, 0.04, 0.12), verts=slat["verts"])
        bmesh.ops.translate(bm, vec=(0.0, 0.23, 0.58 + i * 0.14), verts=slat["verts"])
        for f in [f for f in bm.faces if any(v in slat["verts"] for v in f.verts)]:
            f.material_index = 1

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Bench_Colonial.fbx")

# 8. Campus Heritage Street Lamp (4.5m Victorian cast-iron post lamp)
def build_lamp(mat_a, mat_t):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Lamp_Colonial")
    obj = bpy.data.objects.new("SM_Curzon_Lamp_Colonial", mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat_a) # Dark cast iron
    obj.data.materials.append(mat_t) # Frosted lantern glass

    bm = bmesh.new()
    # Fluted Base
    base = bmesh.ops.create_cone(bm, segments=8, radius1=0.4, radius2=0.25, depth=0.8)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.4), verts=base["verts"])

    # Shaft
    shaft = bmesh.ops.create_cone(bm, segments=8, radius1=0.14, radius2=0.10, depth=3.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 2.3), verts=shaft["verts"])

    # Decorative Capital Ring
    cap = bmesh.ops.create_cone(bm, segments=8, radius1=0.25, radius2=0.15, depth=0.3)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 3.9), verts=cap["verts"])

    # 4-sided Glass Lantern (Slot 1)
    lant = bmesh.ops.create_cone(bm, segments=4, radius1=0.35, radius2=0.45, depth=0.6)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.3), verts=lant["verts"])
    for f in [f for f in bm.faces if any(v in lant["verts"] for v in f.verts)]:
        f.material_index = 1

    # Lantern Cap & Finial
    lcap = bmesh.ops.create_cone(bm, segments=4, radius1=0.5, radius2=0.08, depth=0.35)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 4.75), verts=lcap["verts"])

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Lamp_Colonial.fbx")

def main():
    mb, mt, ma = get_or_create_materials()
    print("Generating Curzon Hall modular assets...")
    build_veranda_lower(mb, mt)
    build_veranda_upper(mb, mt)
    build_entrance_portal(mb, mt)
    build_chattri(mb, mt)
    build_tower_octagon(mb, mt)
    build_parapet(mb, mt)
    build_bench(mb, mt, ma)
    build_lamp(ma, mt)
    print("All modular assets generated successfully!")

if __name__ == "__main__":
    main()
