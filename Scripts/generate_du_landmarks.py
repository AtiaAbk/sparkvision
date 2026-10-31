import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def export_fbx(filepath):
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=False,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Z',
        axis_up='Y'
    )

def create_curzon_hall():
    clear_scene()
    # Main Central Pavilion (Mughal-Gothic brick hall)
    # Dimensions: 40m wide, 20m deep, 14m high (in Blender 1 unit = 1m)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 7))
    main = bpy.context.active_object
    main.name = "Curzon_Main_Hall"
    main.scale = (40.0, 20.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)

    # Front Arcade Corridor (Veranda)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -11.5, 4.5))
    arcade = bpy.context.active_object
    arcade.name = "Curzon_Arcade"
    arcade.scale = (42.0, 3.0, 9.0)
    bpy.ops.object.transform_apply(scale=True)

    # Central High Arch / Portal
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -12.5, 9.0))
    portal = bpy.context.active_object
    portal.name = "Curzon_Central_Portal"
    portal.scale = (10.0, 3.5, 18.0)
    bpy.ops.object.transform_apply(scale=True)

    # Flanking Corner Wings (East and West)
    for x_pos, name in [(-24.0, "Curzon_Wing_West"), (24.0, "Curzon_Wing_East")]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos, 0, 8.0))
        wing = bpy.context.active_object
        wing.name = name
        wing.scale = (12.0, 24.0, 16.0)
        bpy.ops.object.transform_apply(scale=True)

    # Indo-Saracenic Domes & Chattris (Octagonal pavilions atop roof corners)
    corners = [(-24, -10), (-24, 10), (24, -10), (24, 10), (0, -12)]
    for i, (cx, cy) in enumerate(corners):
        # Base column
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1.8, depth=4.0, location=(cx, cy, 18.0))
        tower = bpy.context.active_object
        tower.name = f"Curzon_Tower_{i}"
        
        # Bulbous Mughal Dome
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=2.2, location=(cx, cy, 21.0))
        dome = bpy.context.active_object
        dome.name = f"Curzon_Dome_{i}"
        dome.scale = (1.0, 1.0, 1.4)
        bpy.ops.object.transform_apply(scale=True)

    # Front stairs
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -14.5, 0.75))
    stairs = bpy.context.active_object
    stairs.name = "Curzon_Plaza_Stairs"
    stairs.scale = (20.0, 4.0, 1.5)
    bpy.ops.object.transform_apply(scale=True)

    export_fbx("/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/SM_CurzonHall.fbx")

def create_raju_sculpture():
    clear_scene()
    # Anti-Terrorism Raju Memorial: Curved base with interconnected standing figures
    # Base Pedestal
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=6.0, depth=1.2, location=(0, 0, 0.6))
    base = bpy.context.active_object
    base.name = "Raju_Base"

    # Secondary tiered drum
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=4.5, depth=0.8, location=(0, 0, 1.6))
    base2 = bpy.context.active_object
    base2.name = "Raju_Tier2"

    # Human figures linked arm in arm in solidarity (Stylized bronze statues)
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    for i, deg in enumerate(angles):
        rad = math.radians(deg)
        fx = 3.2 * math.cos(rad)
        fy = 3.2 * math.sin(rad)
        
        # Body
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.45, depth=3.2, location=(fx, fy, 3.6))
        body = bpy.context.active_object
        body.name = f"Raju_Figure_{i}"

        # Head
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.35, location=(fx, fy, 5.5))
        head = bpy.context.active_object
        head.name = f"Raju_Head_{i}"

    # Central raised flag / arm of protest
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.15, depth=6.5, location=(0, 0, 5.0))
    torch = bpy.context.active_object
    torch.name = "Raju_Central_Standard"

    export_fbx("/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/SM_RajuSculpture.fbx")

def create_aparajeyo_bangla():
    clear_scene()
    # Aparajeyo Bangla: 3 heroic freedom fighters (Farmer with rifle, student, nurse/female aid)
    # High massive concrete pedestal
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 2.5))
    pedestal = bpy.context.active_object
    pedestal.name = "Aparajeyo_Pedestal"
    pedestal.scale = (8.0, 5.0, 5.0)
    bpy.ops.object.transform_apply(scale=True)

    # 3 Statues
    offsets = [(-2.2, 0.0, "Nurse"), (0.0, 0.5, "Leader_Rifle"), (2.2, 0.0, "Student")]
    for ox, oy, role in offsets:
        # Legs and torso
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy, 7.5))
        statue = bpy.context.active_object
        statue.name = f"Aparajeyo_{role}"
        statue.scale = (1.4, 1.2, 5.0)
        bpy.ops.object.transform_apply(scale=True)

        # Head
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.6, location=(ox, oy, 10.5))
        shead = bpy.context.active_object
        shead.name = f"Aparajeyo_Head_{role}"

    export_fbx("/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/SM_AparajeyoBangla.fbx")

def create_tsc_building():
    clear_scene()
    # Teacher-Student Centre (TSC): Iconic Modernist Greek-Bengali canopy & auditorium
    # Main Auditorium Block
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 7.0))
    aud = bpy.context.active_object
    aud.name = "TSC_Auditorium"
    aud.scale = (36.0, 30.0, 14.0)
    bpy.ops.object.transform_apply(scale=True)

    # Slanted cantilevered Modernist Roof Canopy
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -18.0, 6.0))
    cafeteria = bpy.context.active_object
    cafeteria.name = "TSC_Cafeteria_Wing"
    cafeteria.scale = (40.0, 14.0, 6.0)
    bpy.ops.object.transform_apply(scale=True)

    # Open Veranda Pillars
    for px in [-16, -8, 0, 8, 16]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.5, depth=6.0, location=(px, -25.0, 3.0))
        col = bpy.context.active_object
        col.name = f"TSC_Pillar_{px}"

    export_fbx("/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/SM_TSC_Building.fbx")

def create_central_library():
    clear_scene()
    # DU Central Library: Brutalist 4-story rectangular building with solar louvres
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 9.0))
    lib = bpy.context.active_object
    lib.name = "DU_Central_Library"
    lib.scale = (50.0, 28.0, 18.0)
    bpy.ops.object.transform_apply(scale=True)

    # Entrance portico
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -16.0, 4.0))
    portico = bpy.context.active_object
    portico.name = "Library_Portico"
    portico.scale = (18.0, 6.0, 8.0)
    bpy.ops.object.transform_apply(scale=True)

    export_fbx("/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/SM_CentralLibrary.fbx")

def create_archive_terminal_mesh():
    clear_scene()
    # Historical Archive Pedestal with Open Book / Documents
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.6))
    pedestal = bpy.context.active_object
    pedestal.name = "Archive_Pedestal"
    pedestal.scale = (0.8, 0.8, 1.2)
    bpy.ops.object.transform_apply(scale=True)

    # Book / Document stand
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 1.35))
    book = bpy.context.active_object
    book.name = "Archive_Record"
    book.scale = (0.9, 0.7, 0.15)
    book.rotation_euler = (math.radians(25), 0, 0)
    bpy.ops.object.transform_apply(rotation=True, scale=True)

    export_fbx("/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/SM_ArchiveTerminal.fbx")

if __name__ == "__main__":
    create_curzon_hall()
    create_raju_sculpture()
    create_aparajeyo_bangla()
    create_tsc_building()
    create_central_library()
    create_archive_terminal_mesh()
    print("[SUCCESS] All DU Landmark FBX models generated.")
