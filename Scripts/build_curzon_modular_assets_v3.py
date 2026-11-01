#!/usr/bin/env python3
"""
Curzon Hall Master Architectural Asset Generator (v3) for Blender 5.2.3 LTS
Reconstructs the authentic Curzon Hall (Faculty of Science, University of Dhaka, 1904)
matching the user's photographic ground-truth references:
1. SM_Curzon_Entrance_Portal:
   - 4-corner chhatris + 3 intermediate domed merlon kiosks on the stepped tower crown
   - 6 vertical arched lancet slits / blind niches + 2 circular star rosettes
   - Projecting bracketed chhajja eave over central window
   - 3-light cusped arched central window with white geometric jali lace screen and glazed sashes
   - Flanking 2-tier arched windows with louvered shutters and white trim
   - Flanking octagonal minaret turrets with open domed chhatris
   - Grand Iwan arch leading to deep recessed vestibule with double dark wood entrance doors
   - 6-step light stone plinth staircase
2. SM_Curzon_Veranda_Arch_Lower:
   - Rhythmic horseshoe arches on chamfered piers with sandstone plinths
   - Inner corridor wall with colonial panelled double doors, arched glass fanlights, and tall shuttered windows
   - Terracotta floor slab, ceiling beams, and projecting chhajja with corbels
3. SM_Curzon_Veranda_Arch_Upper:
   - 7-lobed cusped arches on paired octagonal colonnettes with lotus capitals
   - White pierced geometric jali balustrade screen
   - Inner corridor wall with arched multi-pane windows, glass, and louvered shutters
   - Projecting chhajja with carved corbels
4. SM_Curzon_Parapet_Merlons:
   - Continuous white pierced geometric jali screen balustrade along roofline
   - Miniature domed chhatri kiosks at bay piers
5. SM_Curzon_Tower_Octagon:
   - 25.2m octagonal tower with tiered arched windows and louvered shutters on outer faces
   - Observation balcony with corbel brackets, jali balustrade, 8-pillar open chhatri, and brass finial
6. SM_Curzon_Hedge_Low:
   - Low trimmed manicured boxwood hedge (4m x 0.7m x 0.85m)
7. SM_Curzon_Sign_Physics:
   - Authentic blue Department of Physics signboard with white trim and brackets
"""

import bpy
import bmesh
import math
import mathutils
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
    materials = {}
    
    # 0: Brick (Dark Terracotta Red)
    mat = bpy.data.materials.get("M_Curzon_Brick") or bpy.data.materials.new(name="M_Curzon_Brick")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.52, 0.15, 0.10, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.78
    materials["brick"] = mat

    # 1: White Trim / Stucco / Jali
    mat = bpy.data.materials.get("M_Curzon_WhiteTrim") or bpy.data.materials.new(name="M_Curzon_WhiteTrim")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.88, 0.85, 0.80, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.65
    materials["trim"] = mat

    # 2: Dark Wood / Timber Doors & Window Frames
    mat = bpy.data.materials.get("M_Curzon_WoodDark") or bpy.data.materials.new(name="M_Curzon_WoodDark")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.18, 0.10, 0.05, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.45
    materials["wood"] = mat

    # 3: Louvers / Shutters (Vintage Olive/Sage Green)
    mat = bpy.data.materials.get("M_Curzon_Louvers") or bpy.data.materials.new(name="M_Curzon_Louvers")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.14, 0.22, 0.14, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.65
    materials["louvers"] = mat

    # 4: Glazed Window Glass
    mat = bpy.data.materials.get("M_Curzon_Glass") or bpy.data.materials.new(name="M_Curzon_Glass")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.07, 0.11, 0.16, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.12
    materials["glass"] = mat

    # 5: Sandstone / Steps / Plinth
    mat = bpy.data.materials.get("M_Curzon_Sandstone") or bpy.data.materials.new(name="M_Curzon_Sandstone")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.68, 0.52, 0.38, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.75
    materials["sandstone"] = mat

    # 6: Polished Brass / Kalasa Finials / Door Handles
    mat = bpy.data.materials.get("M_Curzon_Brass") or bpy.data.materials.new(name="M_Curzon_Brass")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.72, 0.56, 0.22, 1.0)
            bsdf.inputs["Metallic"].default_value = 0.90
            bsdf.inputs["Roughness"].default_value = 0.35
    materials["brass"] = mat

    # 7: Terracotta Floor Tiles
    mat = bpy.data.materials.get("M_Curzon_Tiles") or bpy.data.materials.new(name="M_Curzon_Tiles")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.48, 0.19, 0.14, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.55
    materials["tiles"] = mat

    # 8: Cast Iron / Hardware
    mat = bpy.data.materials.get("M_Curzon_CastIron") or bpy.data.materials.new(name="M_Curzon_CastIron")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.12, 0.12, 0.14, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.40
    materials["castiron"] = mat

    # 9: Department Signboard Blue
    mat = bpy.data.materials.get("M_Curzon_SignBlue") or bpy.data.materials.new(name="M_Curzon_SignBlue")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.05, 0.22, 0.62, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.50
    materials["signblue"] = mat

    # 10: Manicured Hedge Green
    mat = bpy.data.materials.get("M_Curzon_Hedge") or bpy.data.materials.new(name="M_Curzon_Hedge")
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.10, 0.32, 0.08, 1.0)
            bsdf.inputs["Roughness"].default_value = 0.65
    materials["hedge"] = mat

    return materials

def assign_mat(bm, verts, mat_idx):
    for f in bm.faces:
        if all(v in verts for v in f.verts):
            f.material_index = mat_idx

def export_fbx(obj, filename):
    out_path = os.path.join(OUTPUT_DIR, filename)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Fix orientation for Unreal Engine: -Y Forward, Z Up
    bpy.ops.export_scene.fbx(
        filepath=out_path,
        use_selection=True,
        global_scale=1.0,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_NONE',
        axis_forward='-Z',
        axis_up='Y',
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )
    print(f"Exported: {out_path} ({os.path.getsize(out_path):,} bytes)")

def add_chhajja_with_brackets(bm, width, depth, base_z, slope_angle=35, projection=1.2, num_brackets=8, y_offset=0.0):
    rad = math.radians(slope_angle)
    drop = projection * math.sin(rad)
    reach = projection * math.cos(rad)
    eave_thickness = 0.12

    y_back = depth / 2.0 + y_offset
    y_front = y_back + reach
    z_back = base_z
    z_front = base_z - drop

    # Eave slab
    eave = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width + 0.3, reach, eave_thickness), verts=eave["verts"])
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(-rad, 3, 'X'), verts=eave["verts"])
    bmesh.ops.translate(bm, vec=(0.0, (y_back + y_front) / 2.0, (z_back + z_front) / 2.0), verts=eave["verts"])

    # Carved Corbel Brackets
    spacing = width / (num_brackets - 1) if num_brackets > 1 else width
    for i in range(num_brackets):
        bx = -width / 2.0 + i * spacing
        # 3-tier stepped corbel
        for tier in range(3):
            t_reach = (tier + 1) * (reach * 0.3)
            t_drop = (3 - tier) * 0.22
            br = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(0.20, t_reach, 0.22), verts=br["verts"])
            bmesh.ops.translate(bm, vec=(bx, y_back + t_reach / 2.0, base_z - t_drop), verts=br["verts"])
            assign_mat(bm, br["verts"], 1) # White trim for brackets

def create_cusped_arch(center_x, spring_z, crown_z, clear_width, num_cusps=7):
    pts = []
    r_main = clear_width / 2.0
    for s in range(num_cusps + 1):
        theta = math.pi * (s / num_cusps)
        x_base = center_x - r_main * math.cos(theta)
        z_base = spring_z + (crown_z - spring_z) * math.sin(theta)
        pts.append((x_base, z_base))
    return pts

def add_door_with_fanlight(bm, center_x, center_y, base_z, width=1.8, height=3.2, frame_depth=0.25):
    # 1. Outer Dark Timber Frame
    door_h = height - 0.9 # Door leaf height
    fan_h = 0.9          # Arched fanlight height
    
    # Outer frame jambs
    jamb_w = 0.12
    for jx in [center_x - width/2.0 + jamb_w/2.0, center_x + width/2.0 - jamb_w/2.0]:
        j = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(jamb_w, frame_depth, height), verts=j["verts"])
        bmesh.ops.translate(bm, vec=(jx, center_y, base_z + height/2.0), verts=j["verts"])
        assign_mat(bm, j["verts"], 2) # Wood Dark
        
    # Transom beam dividing door from fanlight
    tb = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, frame_depth, 0.12), verts=tb["verts"])
    bmesh.ops.translate(bm, vec=(center_x, center_y, base_z + door_h), verts=tb["verts"])
    assign_mat(bm, tb["verts"], 2)

    # 2. Double-Leaf Wooden Doors with Recessed Moulded Panels
    leaf_w = (width - 2 * jamb_w) / 2.0
    for l_idx, lx in enumerate([center_x - leaf_w/2.0 - 0.01, center_x + leaf_w/2.0 + 0.01]):
        # Door leaf body
        leaf = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(leaf_w, 0.08, door_h), verts=leaf["verts"])
        bmesh.ops.translate(bm, vec=(lx, center_y, base_z + door_h/2.0), verts=leaf["verts"])
        assign_mat(bm, leaf["verts"], 2) # Wood Dark
        
        # Two recessed panels per leaf
        for pz in [base_z + door_h * 0.3, base_z + door_h * 0.72]:
            p = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(leaf_w * 0.65, 0.03, door_h * 0.32), verts=p["verts"])
            bmesh.ops.translate(bm, vec=(lx, center_y + 0.03, pz), verts=p["verts"])
            assign_mat(bm, p["verts"], 2)
            
        # Polished Brass Door Handle / Plate
        h_x = lx + (leaf_w * 0.35 if l_idx == 0 else -leaf_w * 0.35)
        h = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.04, 0.06, 0.22), verts=h["verts"])
        bmesh.ops.translate(bm, vec=(h_x, center_y + 0.05, base_z + 1.05), verts=h["verts"])
        assign_mat(bm, h["verts"], 6) # Brass

    # 3. Arched Fanlight Transom with Glass and Radial Glazing Bars
    # Glass pane
    fan_glass = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width - 2*jamb_w, 0.02, fan_h - 0.06), verts=fan_glass["verts"])
    bmesh.ops.translate(bm, vec=(center_x, center_y, base_z + door_h + fan_h/2.0), verts=fan_glass["verts"])
    assign_mat(bm, fan_glass["verts"], 4) # Glass
    
    # White decorative fanlight arch trim
    fan_arch = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, frame_depth + 0.04, 0.12), verts=fan_arch["verts"])
    bmesh.ops.translate(bm, vec=(center_x, center_y, base_z + height), verts=fan_arch["verts"])
    assign_mat(bm, fan_arch["verts"], 1) # White Trim

def add_colonial_window_with_shutters(bm, center_x, center_y, base_z, width=1.3, height=2.6, frame_depth=0.25, is_arched=False):
    # 1. Outer Frame (White Trim Surround & Dark Wood Jambs)
    f_surround = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width + 0.22, frame_depth + 0.06, height + 0.22), verts=f_surround["verts"])
    bmesh.ops.translate(bm, vec=(center_x, center_y, base_z + height/2.0), verts=f_surround["verts"])
    assign_mat(bm, f_surround["verts"], 1) # White Trim
    
    # Dark timber inner frame
    f_inner = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, frame_depth, height), verts=f_inner["verts"])
    bmesh.ops.translate(bm, vec=(center_x, center_y, base_z + height/2.0), verts=f_inner["verts"])
    assign_mat(bm, f_inner["verts"], 2) # Wood Dark

    # 2. Multi-Pane Glazed Window Sash (Center)
    glass_w = width * 0.52
    glass_h = height * 0.88
    glass = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(glass_w, 0.02, glass_h), verts=glass["verts"])
    bmesh.ops.translate(bm, vec=(center_x, center_y, base_z + height/2.0), verts=glass["verts"])
    assign_mat(bm, glass["verts"], 4) # Glass
    
    # Window glazing bars (mullion and transoms)
    # Vertical mullion
    vm = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(0.04, 0.04, glass_h), verts=vm["verts"])
    bmesh.ops.translate(bm, vec=(center_x, center_y + 0.02, base_z + height/2.0), verts=vm["verts"])
    assign_mat(bm, vm["verts"], 2)
    # Horizontal transoms (3 bars)
    for ti in range(3):
        hz = base_z + height * 0.22 + ti * (height * 0.24)
        hm = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(glass_w, 0.04, 0.04), verts=hm["verts"])
        bmesh.ops.translate(bm, vec=(center_x, center_y + 0.02, hz), verts=hm["verts"])
        assign_mat(bm, hm["verts"], 2)

    # 3. Flanking Louvered Timber Shutters (Open at angle / folded back)
    shutter_w = (width - glass_w) / 2.0 + 0.15
    for s_idx, sx in enumerate([center_x - width/2.0 + shutter_w/2.0, center_x + width/2.0 - shutter_w/2.0]):
        # Shutter stile & rail frame
        sf = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(shutter_w, 0.05, height * 0.88), verts=sf["verts"])
        bmesh.ops.translate(bm, vec=(sx, center_y + 0.04, base_z + height/2.0), verts=sf["verts"])
        assign_mat(bm, sf["verts"], 3) # Louvers Green
        
        # Louver blade texture / ribs (horizontal slats)
        for blade in range(6):
            bz = base_z + height * 0.15 + blade * (height * 0.12)
            bl = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(shutter_w * 0.75, 0.07, 0.03), verts=bl["verts"])
            bmesh.ops.translate(bm, vec=(sx, center_y + 0.04, bz), verts=bl["verts"])
            assign_mat(bm, bl["verts"], 3)

# ==============================================================================
# ASSET 1: SM_Curzon_Entrance_Portal (18m wide x 5.6m deep x 23.4m high)
# ==============================================================================
def build_curzon_entrance_portal(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Entrance_Portal")
    obj = bpy.data.objects.new("SM_Curzon_Entrance_Portal", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    # Material slot assignments:
    # 0: Brick, 1: WhiteTrim, 2: WoodDark, 3: Louvers, 4: Glass, 5: Sandstone, 6: Brass, 7: Tiles, 8: CastIron
    for m in [mats["brick"], mats["trim"], mats["wood"], mats["louvers"], mats["glass"], mats["sandstone"], mats["brass"], mats["tiles"], mats["castiron"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 18.0
    depth = 5.6
    height = 23.4

    # 1. Ceremonial 6-Step Sandstone Staircase (Plinth Access)
    num_steps = 6
    st_w_base = 12.0
    for st in range(num_steps):
        st_w = st_w_base - st * 0.3
        st_d = 2.4 - st * 0.32
        st_h = 0.15
        s = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(st_w, st_d, st_h), verts=s["verts"])
        bmesh.ops.translate(bm, vec=(0.0, depth/2.0 + st_d/2.0, (st + 0.5) * st_h), verts=s["verts"])
        assign_mat(bm, s["verts"], 5) # Sandstone

    # 2. Main Portal Pylons (Left & Right)
    pylon_w = 4.8
    pylon_d = depth
    pylon_h = 19.4
    
    for px in [-width/2.0 + pylon_w/2.0, width/2.0 - pylon_w/2.0]:
        p = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pylon_w, pylon_d, pylon_h), verts=p["verts"])
        bmesh.ops.translate(bm, vec=(px, 0.0, pylon_h/2.0), verts=p["verts"])
        assign_mat(bm, p["verts"], 0) # Brick
        
        # Sandstone base plinth
        pb = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pylon_w + 0.2, pylon_d + 0.2, 0.9), verts=pb["verts"])
        bmesh.ops.translate(bm, vec=(px, 0.0, 0.45), verts=pb["verts"])
        assign_mat(bm, pb["verts"], 5) # Sandstone
        
        # Horizontal white string courses at +7.6m and +14.4m
        for zh in [7.6, 14.4]:
            sc = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(pylon_w + 0.15, pylon_d + 0.15, 0.32), verts=sc["verts"])
            bmesh.ops.translate(bm, vec=(px, 0.0, zh), verts=sc["verts"])
            assign_mat(bm, sc["verts"], 1) # White Trim

        # Flanking Ground Floor Arched Windows on Pylons
        add_colonial_window_with_shutters(bm, center_x=px, center_y=depth/2.0 + 0.05, base_z=1.2, width=1.4, height=3.6, is_arched=True)
        
        # Flanking Upper Floor 2-Light Arched Windows on Pylons
        add_colonial_window_with_shutters(bm, center_x=px, center_y=depth/2.0 + 0.05, base_z=8.8, width=1.5, height=3.8, is_arched=True)

        # Flanking Octagonal Minaret Turrets rising to +18.4m
        turret_x = px + (1.6 if px < 0 else -1.6)
        turret = bmesh.ops.create_cone(bm, segments=8, radius1=0.85, radius2=0.75, depth=14.4)
        bmesh.ops.translate(bm, vec=(turret_x, depth/2.0 - 0.2, 7.2), verts=turret["verts"])
        assign_mat(bm, turret["verts"], 0)
        
        # Turret Observation Balcony & Corbelled Kiosk at +14.4m
        bal_c = bmesh.ops.create_cone(bm, segments=8, radius1=1.1, radius2=0.85, depth=0.45)
        bmesh.ops.translate(bm, vec=(turret_x, depth/2.0 - 0.2, 14.6), verts=bal_c["verts"])
        assign_mat(bm, bal_c["verts"], 1)
        
        # Turret Open 8-Pillar Chhatri Kiosk
        for tpi in range(8):
            tang = tpi * (2.0 * math.pi / 8)
            tpx = turret_x + 0.75 * math.cos(tang)
            tpy = (depth/2.0 - 0.2) + 0.75 * math.sin(tang)
            tpil = bmesh.ops.create_cone(bm, segments=8, radius1=0.07, radius2=0.07, depth=1.6)
            bmesh.ops.translate(bm, vec=(tpx, tpy, 15.6), verts=tpil["verts"])
            assign_mat(bm, tpil["verts"], 1)
            
        # Turret Cupola Dome & Finial
        tdome = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=0.9)
        for v in tdome["verts"]:
            if v.co.z < 0: v.co.z = 0
        bmesh.ops.translate(bm, vec=(turret_x, depth/2.0 - 0.2, 16.4), verts=tdome["verts"])
        assign_mat(bm, tdome["verts"], 1)
        
        tfin = bmesh.ops.create_cone(bm, segments=8, radius1=0.10, radius2=0.01, depth=0.9)
        bmesh.ops.translate(bm, vec=(turret_x, depth/2.0 - 0.2, 17.7), verts=tfin["verts"])
        assign_mat(bm, tfin["verts"], 6) # Brass

    # 3. Grand Ground Floor Iwan Archway & Recessed Entrance Vestibule
    iwan_span = 6.4
    iwan_spring_z = 4.2
    iwan_crown_z = 7.6
    
    # Recessed vestibule floor (tiles) & rear wall
    vest_fl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(iwan_span + 0.4, 2.6, 0.2), verts=vest_fl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - 1.3, 0.8), verts=vest_fl["verts"])
    assign_mat(bm, vest_fl["verts"], 7) # Tiles
    
    # Rear vestibule wall with Authentic Double Entrance Doors
    vest_rw = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(iwan_span + 0.4, 0.4, 7.2), verts=vest_rw["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - 2.5, 4.4), verts=vest_rw["verts"])
    assign_mat(bm, vest_rw["verts"], 0)
    
    # Grand Double Entrance Doors inside vestibule
    add_door_with_fanlight(bm, center_x=0.0, center_y=depth/2.0 - 2.3, base_z=0.9, width=2.8, height=4.2)

    # Iwan Arch Ring (Stepped multi-cusped reveals in brick & white trim)
    iwan_pts = create_cusped_arch(center_x=0.0, spring_z=iwan_spring_z, crown_z=iwan_crown_z, clear_width=iwan_span, num_cusps=9)
    for i in range(len(iwan_pts) - 1):
        x1, z1 = iwan_pts[i]
        x2, z2 = iwan_pts[i+1]
        mid_x = (x1 + x2) / 2.0
        mid_z = (z1 + z2) / 2.0
        seg = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.08, 1.4, 0.65), verts=seg["verts"])
        bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.7, mid_z + 0.2), verts=seg["verts"])
        assign_mat(bm, seg["verts"], 0) # Brick
        
        # White plaster trim reveal
        t_seg = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.06, 1.5, 0.20), verts=t_seg["verts"])
        bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.7, mid_z - 0.08), verts=t_seg["verts"])
        assign_mat(bm, t_seg["verts"], 1) # White Trim

    # 4. Second Floor Central Triple Window Unit (Grand 3-Light Jali Unit)
    # Spans X = -2.8m to +2.8m, Z = 8.4m to 14.2m
    c_win_w = 5.6
    c_win_h = 5.8
    
    # Window recessed brick envelope
    c_win_back = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(c_win_w + 0.4, 0.5, c_win_h + 0.4), verts=c_win_back["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - 0.6, 8.4 + c_win_h/2.0), verts=c_win_back["verts"])
    assign_mat(bm, c_win_back["verts"], 0)
    
    # White multi-cusped outer arch frame
    c_arch_pts = create_cusped_arch(center_x=0.0, spring_z=11.6, crown_z=14.2, clear_width=c_win_w, num_cusps=7)
    for i in range(len(c_arch_pts) - 1):
        x1, z1 = c_arch_pts[i]
        x2, z2 = c_arch_pts[i+1]
        mid_x = (x1 + x2) / 2.0
        mid_z = (z1 + z2) / 2.0
        aseg = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.06, 0.4, 0.35), verts=aseg["verts"])
        bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.25, mid_z), verts=aseg["verts"])
        assign_mat(bm, aseg["verts"], 1) # White Trim

    # Upper Tympanum: White Pierced Geometric Jali Screen
    jali_tym = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(c_win_w * 0.85, 0.08, 1.6), verts=jali_tym["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - 0.3, 12.8), verts=jali_tym["verts"])
    assign_mat(bm, jali_tym["verts"], 1) # White Trim

    # Three Vertical Arched Window Lights separated by Colonnettes
    light_w = 1.3
    light_positions = [-1.6, 0.0, 1.6]
    for lx in light_positions:
        # Arched light top
        ltop = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(light_w, 0.15, 0.25), verts=ltop["verts"])
        bmesh.ops.translate(bm, vec=(lx, depth/2.0 - 0.3, 11.8), verts=ltop["verts"])
        assign_mat(bm, ltop["verts"], 1)
        
        # Glazed window sash
        lsash = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(light_w * 0.8, 0.04, 2.4), verts=lsash["verts"])
        bmesh.ops.translate(bm, vec=(lx, depth/2.0 - 0.35, 10.4), verts=lsash["verts"])
        assign_mat(bm, lsash["verts"], 4) # Glass
        
        # Dark timber mullions
        lmul = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.04, 0.06, 2.4), verts=lmul["verts"])
        bmesh.ops.translate(bm, vec=(lx, depth/2.0 - 0.33, 10.4), verts=lmul["verts"])
        assign_mat(bm, lmul["verts"], 2) # Wood Dark
        
        # Lower White Geometric Jali Balustrade Screen
        lbal = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(light_w + 0.1, 0.12, 0.95), verts=lbal["verts"])
        bmesh.ops.translate(bm, vec=(lx, depth/2.0 - 0.28, 9.0), verts=lbal["verts"])
        assign_mat(bm, lbal["verts"], 1) # White Trim

    # Colonnettes separating the 3 lights
    for cx in [-0.8, 0.8]:
        col = bmesh.ops.create_cone(bm, segments=8, radius1=0.12, radius2=0.12, depth=3.2)
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - 0.26, 10.2), verts=col["verts"])
        assign_mat(bm, col["verts"], 1) # White Trim

    # 5. Projecting Chhajja Eave Over Central Window at +14.4m
    add_chhajja_with_brackets(bm, width=c_win_w + 1.6, depth=depth, base_z=14.4, slope_angle=35, projection=1.2, num_brackets=6)

    # 6. Third Level Tower Shaft (Z = 14.8m to 19.2m)
    tower_top_w = 11.2
    tower_top_h = 4.4
    t_shaft = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(tower_top_w, depth, tower_top_h), verts=t_shaft["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 14.8 + tower_top_h/2.0), verts=t_shaft["verts"])
    assign_mat(bm, t_shaft["verts"], 0) # Brick

    # Row of 6 Vertical Arched Lancet Slits / Blind Niches
    num_niches = 6
    niche_spacing = 1.05
    for ni in range(num_niches):
        nx = - (num_niches - 1) * niche_spacing / 2.0 + ni * niche_spacing
        # Recessed arched niche
        niche = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.48, 0.35, 1.8), verts=niche["verts"])
        bmesh.ops.translate(bm, vec=(nx, depth/2.0 - 0.1, 16.6), verts=niche["verts"])
        assign_mat(bm, niche["verts"], 1) # White Trim
        
        # Corbel bracket beneath niche
        nbr = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.25, 0.40, 0.22), verts=nbr["verts"])
        bmesh.ops.translate(bm, vec=(nx, depth/2.0 - 0.08, 15.55), verts=nbr["verts"])
        assign_mat(bm, nbr["verts"], 1)

    # Twin Circular Star / Wheel Rosettes (Medallions) flanking the niches
    for rx in [-4.2, 4.2]:
        rosette = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.6, radius2=0.6, depth=0.15)
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(math.pi/2, 3, 'X'), verts=rosette["verts"])
        bmesh.ops.translate(bm, vec=(rx, depth/2.0 + 0.05, 16.6), verts=rosette["verts"])
        assign_mat(bm, rosette["verts"], 1) # White Trim
        
        # Inner brass hub
        rhub = bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.2, radius2=0.2, depth=0.18)
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(math.pi/2, 3, 'X'), verts=rhub["verts"])
        bmesh.ops.translate(bm, vec=(rx, depth/2.0 + 0.08, 16.6), verts=rhub["verts"])
        assign_mat(bm, rhub["verts"], 6) # Brass

    # 7. Top Projecting Cornice with White Bracket Dentils at +18.8m
    cornice = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(tower_top_w + 0.8, depth + 0.8, 0.35), verts=cornice["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 19.0), verts=cornice["verts"])
    assign_mat(bm, cornice["verts"], 5) # Sandstone

    # White Pierced Jali Parapet along roofline
    t_parapet = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(tower_top_w + 0.6, depth + 0.6, 0.85), verts=t_parapet["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 19.6), verts=t_parapet["verts"])
    assign_mat(bm, t_parapet["verts"], 1) # White Trim

    # 8. Four Corner Chhatris at the Four Corners of Tower Top (+19.4m to +23.4m)
    c_corners = [
        (-tower_top_w/2.0 + 0.8, depth/2.0 - 0.8),
        (tower_top_w/2.0 - 0.8, depth/2.0 - 0.8),
        (-tower_top_w/2.0 + 0.8, -depth/2.0 + 0.8),
        (tower_top_w/2.0 - 0.8, -depth/2.0 + 0.8)
    ]
    for ch_x, ch_y in c_corners:
        base_z = 19.8
        # Sandstone octagonal base
        cb = bmesh.ops.create_cone(bm, segments=8, radius1=0.8, radius2=0.75, depth=0.4)
        bmesh.ops.translate(bm, vec=(ch_x, ch_y, base_z + 0.2), verts=cb["verts"])
        assign_mat(bm, cb["verts"], 5)
        
        # 4 Slender Pillars
        ch_r = 0.55
        for pi in range(4):
            pang = pi * (math.pi / 2) + math.pi/4
            cpx = ch_x + ch_r * math.cos(pang)
            cpy = ch_y + ch_r * math.sin(pang)
            cpil = bmesh.ops.create_cone(bm, segments=8, radius1=0.08, radius2=0.08, depth=1.5)
            bmesh.ops.translate(bm, vec=(cpx, cpy, base_z + 0.4 + 0.75), verts=cpil["verts"])
            assign_mat(bm, cpil["verts"], 1)
            
        # Octagonal Chhajja Eave
        ceave = bmesh.ops.create_cone(bm, segments=8, radius1=1.1, radius2=0.9, depth=0.18)
        bmesh.ops.translate(bm, vec=(ch_x, ch_y, base_z + 1.9 + 0.09), verts=ceave["verts"])
        assign_mat(bm, ceave["verts"], 1)
        
        # Cupola Dome (Fluted Hemisphere)
        cdome = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=0.85)
        for v in cdome["verts"]:
            if v.co.z < 0: v.co.z = 0
        bmesh.ops.translate(bm, vec=(ch_x, ch_y, base_z + 2.0), verts=cdome["verts"])
        assign_mat(bm, cdome["verts"], 1)
        
        # Brass Kalasa Finial
        cfin = bmesh.ops.create_cone(bm, segments=8, radius1=0.11, radius2=0.01, depth=0.95)
        bmesh.ops.translate(bm, vec=(ch_x, ch_y, base_z + 2.85 + 0.45), verts=cfin["verts"])
        assign_mat(bm, cfin["verts"], 6) # Brass

    # 9. Three Intermediate Domed Merlon Kiosks along Front Battlement
    merlon_xs = [-2.4, 0.0, 2.4]
    for mx in merlon_xs:
        m_base_z = 20.0
        # Stepped pedestal
        mped = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.7, 0.5, 0.7), verts=mped["verts"])
        bmesh.ops.translate(bm, vec=(mx, depth/2.0 - 0.25, m_base_z + 0.35), verts=mped["verts"])
        assign_mat(bm, mped["verts"], 1)
        
        # Domed cupola
        mdome = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.45)
        for v in mdome["verts"]:
            if v.co.z < 0: v.co.z = 0
        bmesh.ops.translate(bm, vec=(mx, depth/2.0 - 0.25, m_base_z + 0.7), verts=mdome["verts"])
        assign_mat(bm, mdome["verts"], 1)
        
        # Finial
        mfin = bmesh.ops.create_cone(bm, segments=8, radius1=0.06, radius2=0.01, depth=0.5)
        bmesh.ops.translate(bm, vec=(mx, depth/2.0 - 0.25, m_base_z + 1.15 + 0.25), verts=mfin["verts"])
        assign_mat(bm, mfin["verts"], 6)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Entrance_Portal.fbx")

# ==============================================================================
# ASSET 2: SM_Curzon_Veranda_Arch_Lower (8m wide x 2.6m deep x 6.4m high)
# ==============================================================================
def build_curzon_veranda_lower(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Veranda_Arch_Lower")
    obj = bpy.data.objects.new("SM_Curzon_Veranda_Arch_Lower", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    for m in [mats["brick"], mats["trim"], mats["wood"], mats["louvers"], mats["glass"], mats["sandstone"], mats["brass"], mats["tiles"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 8.0
    depth = 2.6
    height = 6.4

    # 1. Floor / Plinth Slab (Tiles)
    fl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.4), verts=fl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.2), verts=fl["verts"])
    assign_mat(bm, fl["verts"], 7) # Tiles

    # 2. Ceiling / Floor Header Slab
    cl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.5), verts=cl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, height - 0.25), verts=cl["verts"])
    assign_mat(bm, cl["verts"], 0)

    # 3. Three Massive Piers (Left, Center, Right)
    pier_w = 0.8
    pier_d = 0.85
    pier_xs = [-width/2.0 + pier_w/2.0, 0.0, width/2.0 - pier_w/2.0]
    
    for px in pier_xs:
        p = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pier_w, pier_d, 3.8), verts=p["verts"])
        bmesh.ops.translate(bm, vec=(px, depth/2.0 - pier_d/2.0, 2.3), verts=p["verts"])
        assign_mat(bm, p["verts"], 0)
        
        # Sandstone plinth base
        pb = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pier_w + 0.15, pier_d + 0.15, 0.5), verts=pb["verts"])
        bmesh.ops.translate(bm, vec=(px, depth/2.0 - pier_d/2.0, 0.65), verts=pb["verts"])
        assign_mat(bm, pb["verts"], 5)
        
        # White molded impost capital
        ic = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(pier_w + 0.12, pier_d + 0.12, 0.3), verts=ic["verts"])
        bmesh.ops.translate(bm, vec=(px, depth/2.0 - pier_d/2.0, 4.2), verts=ic["verts"])
        assign_mat(bm, ic["verts"], 1)

    # 4. Two Curved Horseshoe Arches (Left Bay: x = -2.0m, Right Bay: x = +2.0m)
    bay_centers = [-2.0, 2.0]
    arch_clear_w = 2.8
    spring_z = 4.2
    
    for cx in bay_centers:
        r_in = arch_clear_w / 2.0
        r_out = r_in + 0.40
        num_seg = 12
        start_a = -math.radians(12)
        end_a = math.pi + math.radians(12)
        
        for s in range(num_seg):
            a1 = start_a + (s / num_seg) * (end_a - start_a)
            a2 = start_a + ((s + 1) / num_seg) * (end_a - start_a)
            x1_in = cx - r_in * math.cos(a1)
            z1_in = spring_z + r_in * math.sin(a1)
            x2_in = cx - r_in * math.cos(a2)
            z2_in = spring_z + r_in * math.sin(a2)
            x1_out = cx - r_out * math.cos(a1)
            z1_out = spring_z + r_out * math.sin(a1)
            x2_out = cx - r_out * math.cos(a2)
            z2_out = spring_z + r_out * math.sin(a2)
            
            seg = bmesh.ops.create_cube(bm, size=1.0)
            avg_x = (x1_in + x2_in + x1_out + x2_out) / 4.0
            avg_z = (z1_in + z2_in + z1_out + z2_out) / 4.0
            bmesh.ops.scale(bm, vec=(abs(x2_in - x1_in) + 0.05, pier_d, 0.45), verts=seg["verts"])
            bmesh.ops.translate(bm, vec=(avg_x, depth/2.0 - pier_d/2.0, avg_z), verts=seg["verts"])
            assign_mat(bm, seg["verts"], 0)
            
        # Keystone at apex (White Trim)
        ks = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.45, pier_d + 0.1, 0.65), verts=ks["verts"])
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - pier_d/2.0, spring_z + r_out + 0.15), verts=ks["verts"])
        assign_mat(bm, ks["verts"], 1)

    # 5. Upper Spandrel Wall
    sp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, pier_d, 0.65), verts=sp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - pier_d/2.0, height - 0.7), verts=sp["verts"])
    assign_mat(bm, sp["verts"], 0)

    # 6. INNER CORRIDOR WALL WITH REAL COLONIAL DOORS AND WINDOWS!
    rw_y = -depth/2.0 + 0.2
    # Base brick wall
    rw = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, 0.4, height), verts=rw["verts"])
    bmesh.ops.translate(bm, vec=(0.0, rw_y, height/2.0), verts=rw["verts"])
    assign_mat(bm, rw["verts"], 0)

    # Add Authentic Colonial Double Door with Arched Fanlight at Left Bay (cx = -2.0m)
    add_door_with_fanlight(bm, center_x=-2.0, center_y=rw_y + 0.2, base_z=0.4, width=1.8, height=3.2)
    
    # Add Authentic Colonial Window with Louvered Shutters at Right Bay (cx = +2.0m)
    add_colonial_window_with_shutters(bm, center_x=2.0, center_y=rw_y + 0.2, base_z=0.8, width=1.3, height=2.6, is_arched=True)

    # 7. Projecting Chhajja at +6.4m with Corbel Brackets
    add_chhajja_with_brackets(bm, width=width, depth=depth, base_z=height - 0.1, slope_angle=35, projection=1.2, num_brackets=8)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Veranda_Arch_Lower.fbx")

# ==============================================================================
# ASSET 3: SM_Curzon_Veranda_Arch_Upper (8m wide x 2.6m deep x 6.2m high)
# ==============================================================================
def build_curzon_veranda_upper(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Veranda_Arch_Upper")
    obj = bpy.data.objects.new("SM_Curzon_Veranda_Arch_Upper", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    for m in [mats["brick"], mats["trim"], mats["wood"], mats["louvers"], mats["glass"], mats["sandstone"], mats["tiles"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 8.0
    depth = 2.6
    height = 6.2

    # 1. Floor Slab (Tiles) & Ceiling Slab
    fl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.35), verts=fl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.175), verts=fl["verts"])
    assign_mat(bm, fl["verts"], 7) # Tiles

    cl = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, depth, 0.45), verts=cl["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, height - 0.225), verts=cl["verts"])
    assign_mat(bm, cl["verts"], 0)

    # 2. Octagonal Slender Colonnade
    col_r = 0.22
    col_d = 4.2
    col_xs = [-3.6, -0.4, 0.4, 3.6]
    for cx in col_xs:
        c = bmesh.ops.create_cone(bm, segments=8, radius1=col_r, radius2=col_r, depth=col_d)
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - 0.45, col_d/2.0 + 0.35), verts=c["verts"])
        assign_mat(bm, c["verts"], 0)
        
        # Molded Sandstone Base
        bs = bmesh.ops.create_cone(bm, segments=8, radius1=col_r + 0.12, radius2=col_r + 0.06, depth=0.35)
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - 0.45, 0.52), verts=bs["verts"])
        assign_mat(bm, bs["verts"], 5)
        
        # Carved Lotus Capital (White Trim)
        cp = bmesh.ops.create_cone(bm, segments=8, radius1=col_r + 0.15, radius2=col_r + 0.22, depth=0.45)
        bmesh.ops.translate(bm, vec=(cx, depth/2.0 - 0.45, col_d + 0.35 + 0.22), verts=cp["verts"])
        assign_mat(bm, cp["verts"], 1)

    # 3. White Pierced Jali Balustrade Screen along front (Height 1.0m)
    bal_w = 3.1
    for bx in [-2.0, 2.0]:
        bal = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(bal_w, 0.16, 0.95), verts=bal["verts"])
        bmesh.ops.translate(bm, vec=(bx, depth/2.0 - 0.45, 0.85), verts=bal["verts"])
        assign_mat(bm, bal["verts"], 1) # White Trim
        
        hr = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(bal_w + 0.1, 0.24, 0.12), verts=hr["verts"])
        bmesh.ops.translate(bm, vec=(bx, depth/2.0 - 0.45, 1.38), verts=hr["verts"])
        assign_mat(bm, hr["verts"], 5) # Sandstone

    # 4. Two Mughal Multi-Cusped Arches (7 cusps each)
    for ax in [-2.0, 2.0]:
        arch_pts = create_cusped_arch(center_x=ax, spring_z=4.6, crown_z=5.6, clear_width=3.2, num_cusps=7)
        for i in range(len(arch_pts) - 1):
            x1, z1 = arch_pts[i]
            x2, z2 = arch_pts[i+1]
            seg = bmesh.ops.create_cube(bm, size=1.0)
            mid_x = (x1 + x2) / 2.0
            mid_z = (z1 + z2) / 2.0
            bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.05, 0.6, 0.35), verts=seg["verts"])
            bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.45, mid_z + 0.15), verts=seg["verts"])
            assign_mat(bm, seg["verts"], 0)
            
            t_seg = bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.scale(bm, vec=(abs(x2 - x1) + 0.04, 0.65, 0.12), verts=t_seg["verts"])
            bmesh.ops.translate(bm, vec=(mid_x, depth/2.0 - 0.45, mid_z - 0.06), verts=t_seg["verts"])
            assign_mat(bm, t_seg["verts"], 1)

    # 5. Upper Spandrel Wall
    sp = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, 0.6, 0.5), verts=sp["verts"])
    bmesh.ops.translate(bm, vec=(0.0, depth/2.0 - 0.45, height - 0.5), verts=sp["verts"])
    assign_mat(bm, sp["verts"], 0)

    # 6. INNER CORRIDOR WALL WITH TWO AUTHENTIC ARCHED WINDOWS!
    rw_y = -depth/2.0 + 0.2
    rw = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, 0.4, height), verts=rw["verts"])
    bmesh.ops.translate(bm, vec=(0.0, rw_y, height/2.0), verts=rw["verts"])
    assign_mat(bm, rw["verts"], 0)

    # Two authentic arched multi-pane windows with louvered shutters
    add_colonial_window_with_shutters(bm, center_x=-2.0, center_y=rw_y + 0.2, base_z=0.6, width=1.4, height=3.0, is_arched=True)
    add_colonial_window_with_shutters(bm, center_x=2.0, center_y=rw_y + 0.2, base_z=0.6, width=1.4, height=3.0, is_arched=True)

    # 7. Upper Projecting Chhajja at +6.2m with Corbel Brackets
    add_chhajja_with_brackets(bm, width=width, depth=depth, base_z=height - 0.1, slope_angle=35, projection=1.2, num_brackets=8)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Veranda_Arch_Upper.fbx")

# ==============================================================================
# ASSET 4: SM_Curzon_Parapet_Merlons (Continuous White Jali & Miniature Kiosks)
# ==============================================================================
def build_curzon_parapet_merlons(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Parapet_Merlons")
    obj = bpy.data.objects.new("SM_Curzon_Parapet_Merlons", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    for m in [mats["brick"], mats["trim"], mats["brass"], mats["sandstone"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 8.0
    wall_d = 0.45
    parapet_h = 1.1

    # Base stone stringer
    base = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, wall_d + 0.1, 0.22), verts=base["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.11), verts=base["verts"])
    assign_mat(bm, base["verts"], 3) # Sandstone

    # Continuous Pierced White Jali Screen Balustrade
    jali = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, wall_d, parapet_h - 0.22), verts=jali["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.22 + (parapet_h - 0.22)/2.0), verts=jali["verts"])
    assign_mat(bm, jali["verts"], 1) # White Trim

    # Handrail capping
    rail = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, wall_d + 0.12, 0.14), verts=rail["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, parapet_h + 0.07), verts=rail["verts"])
    assign_mat(bm, rail["verts"], 1)

    # Miniature Domed Chhatri Kiosks at bay center and ends (x = -4.0m, 0.0m, +4.0m)
    for kx in [-4.0, 0.0, 4.0]:
        # Kiosk pedestal
        kped = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.6, wall_d + 0.15, 0.4), verts=kped["verts"])
        bmesh.ops.translate(bm, vec=(kx, 0.0, parapet_h + 0.2), verts=kped["verts"])
        assign_mat(bm, kped["verts"], 1)
        
        # 4 slender colonnettes
        for cpi in range(4):
            cang = cpi * (math.pi / 2) + math.pi/4
            cpx = kx + 0.22 * math.cos(cang)
            cpy = 0.22 * math.sin(cang)
            cpil = bmesh.ops.create_cone(bm, segments=8, radius1=0.04, radius2=0.04, depth=0.6)
            bmesh.ops.translate(bm, vec=(cpx, cpy, parapet_h + 0.4 + 0.3), verts=cpil["verts"])
            assign_mat(bm, cpil["verts"], 1)
            
        # Hemispherical dome
        kdome = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.32)
        for v in kdome["verts"]:
            if v.co.z < 0: v.co.z = 0
        bmesh.ops.translate(bm, vec=(kx, 0.0, parapet_h + 1.0), verts=kdome["verts"])
        assign_mat(bm, kdome["verts"], 1)
        
        # Brass finial
        kfin = bmesh.ops.create_cone(bm, segments=8, radius1=0.04, radius2=0.01, depth=0.4)
        bmesh.ops.translate(bm, vec=(kx, 0.0, parapet_h + 1.35 + 0.2), verts=kfin["verts"])
        assign_mat(bm, kfin["verts"], 2) # Brass

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Parapet_Merlons.fbx")

# ==============================================================================
# ASSET 5: SM_Curzon_Tower_Octagon (25.2m High Corner Octagonal Tower)
# ==============================================================================
def build_curzon_tower_octagon(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Tower_Octagon")
    obj = bpy.data.objects.new("SM_Curzon_Tower_Octagon", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    for m in [mats["brick"], mats["trim"], mats["wood"], mats["louvers"], mats["glass"], mats["sandstone"], mats["brass"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    total_h = 25.2
    radius = 3.6 # Octagonal face-to-face ~ 7.2m

    # 1. Solid Sandstone Plinth Base (Z = 0.0m to 1.2m)
    base = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.4, radius2=radius + 0.2, depth=1.2)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.6), verts=base["verts"])
    assign_mat(bm, base["verts"], 5) # Sandstone

    # 2. Lower Tower Drum (Z = 1.2m to 7.6m)
    drum_lower = bmesh.ops.create_cone(bm, segments=8, radius1=radius, radius2=radius, depth=6.4)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 1.2 + 3.2), verts=drum_lower["verts"])
    assign_mat(bm, drum_lower["verts"], 0) # Brick

    # Arched Windows with Louvers on visible outer faces (faces 0, 1, 2, 6, 7)
    for f_idx in [0, 1, 2, 6, 7]:
        ang = f_idx * (2.0 * math.pi / 8.0)
        wx = (radius - 0.1) * math.cos(ang)
        wy = (radius - 0.1) * math.sin(ang)
        
        # Window frame
        wf = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(1.1, 0.35, 2.4), verts=wf["verts"])
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(ang, 3, 'Z'), verts=wf["verts"])
        bmesh.ops.translate(bm, vec=(wx, wy, 4.4), verts=wf["verts"])
        assign_mat(bm, wf["verts"], 1) # White Trim
        
        # Louvers
        wl = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.85, 0.2, 1.8), verts=wl["verts"])
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(ang, 3, 'Z'), verts=wl["verts"])
        bmesh.ops.translate(bm, vec=(wx * 1.02, wy * 1.02, 4.4), verts=wl["verts"])
        assign_mat(bm, wl["verts"], 3) # Louvers

    # 3. Intermediate String Course at +7.6m
    sc = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.25, radius2=radius + 0.15, depth=0.5)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 7.85), verts=sc["verts"])
    assign_mat(bm, sc["verts"], 1)

    # 4. Upper Tower Drum (Z = 8.1m to 14.4m)
    drum_upper = bmesh.ops.create_cone(bm, segments=8, radius1=radius - 0.15, radius2=radius - 0.15, depth=6.3)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 8.1 + 3.15), verts=drum_upper["verts"])
    assign_mat(bm, drum_upper["verts"], 0)

    # Upper Arched Windows on outer faces
    for f_idx in [0, 1, 2, 6, 7]:
        ang = f_idx * (2.0 * math.pi / 8.0)
        wx = (radius - 0.25) * math.cos(ang)
        wy = (radius - 0.25) * math.sin(ang)
        wf = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(1.1, 0.35, 2.6), verts=wf["verts"])
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(ang, 3, 'Z'), verts=wf["verts"])
        bmesh.ops.translate(bm, vec=(wx, wy, 11.2), verts=wf["verts"])
        assign_mat(bm, wf["verts"], 1)
        
        wl = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.85, 0.2, 2.0), verts=wl["verts"])
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=mathutils.Matrix.Rotation(ang, 3, 'Z'), verts=wl["verts"])
        bmesh.ops.translate(bm, vec=(wx * 1.02, wy * 1.02, 11.2), verts=wl["verts"])
        assign_mat(bm, wl["verts"], 3)

    # 5. Projecting Chhajja Eave at +14.4m
    chhajja_cone = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 1.2, radius2=radius - 0.1, depth=0.45)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 14.6), verts=chhajja_cone["verts"])
    assign_mat(bm, chhajja_cone["verts"], 1)

    # 6. Upper Drum & Observation Balcony (Z = 14.8m to 19.8m)
    drum_bal = bmesh.ops.create_cone(bm, segments=8, radius1=radius - 0.3, radius2=radius - 0.3, depth=5.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 14.8 + 2.5), verts=drum_bal["verts"])
    assign_mat(bm, drum_bal["verts"], 0)

    # Balcony cantilever corbels at +19.8m
    bal_slab = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.8, radius2=radius - 0.2, depth=0.6)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 20.1), verts=bal_slab["verts"])
    assign_mat(bm, bal_slab["verts"], 5) # Sandstone

    # White Pierced Jali Balustrade on Balcony (+20.4m to +21.4m)
    bal_rail = bmesh.ops.create_cone(bm, segments=8, radius1=radius + 0.8, radius2=radius + 0.8, depth=1.0)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 20.9), verts=bal_rail["verts"])
    assign_mat(bm, bal_rail["verts"], 1) # White Trim

    # 7. Grand 8-Pillar Rajput Chhatri Kiosk (+20.4m to +25.2m)
    ch_base_z = 20.4
    ch_r = radius * 0.72
    for pi in range(8):
        ang = pi * (2.0 * math.pi / 8.0)
        px = ch_r * math.cos(ang)
        py = ch_r * math.sin(ang)
        pil = bmesh.ops.create_cone(bm, segments=8, radius1=0.18, radius2=0.18, depth=2.4)
        bmesh.ops.translate(bm, vec=(px, py, ch_base_z + 1.2), verts=pil["verts"])
        assign_mat(bm, pil["verts"], 1)
        
    # Chhatri projecting chhajja eave
    c_eave = bmesh.ops.create_cone(bm, segments=8, radius1=ch_r + 1.1, radius2=ch_r + 0.2, depth=0.35)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, ch_base_z + 2.55), verts=c_eave["verts"])
    assign_mat(bm, c_eave["verts"], 1)
    
    # Fluted Hemispherical Cupola Dome
    dome = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=ch_r + 0.25)
    for v in dome["verts"]:
        if v.co.z < 0: v.co.z = 0
    bmesh.ops.translate(bm, vec=(0.0, 0.0, ch_base_z + 2.7), verts=dome["verts"])
    assign_mat(bm, dome["verts"], 1) # White Trim
    
    # Lotus Crest & Brass Kalasa Finial
    fin = bmesh.ops.create_cone(bm, segments=8, radius1=0.22, radius2=0.02, depth=1.3)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, ch_base_z + 4.1 + 0.65), verts=fin["verts"])
    assign_mat(bm, fin["verts"], 6) # Brass

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Tower_Octagon.fbx")

# ==============================================================================
# ASSET 6: SM_Curzon_Hedge_Low (Low Trimmed Boxwood Shrub)
# ==============================================================================
def build_curzon_hedge_low(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Hedge_Low")
    obj = bpy.data.objects.new("SM_Curzon_Hedge_Low", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    obj.data.materials.append(mats["hedge"])

    bm = bmesh.new()
    length = 4.0
    width = 0.7
    height = 0.85

    # Main manicured block with beveled rounded top edges
    hd = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(length, width, height), verts=hd["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, height/2.0), verts=hd["verts"])
    assign_mat(bm, hd["verts"], 0)

    # Organic top puff clusters
    for i in range(8):
        px = -length/2.0 + 0.25 + i * (length - 0.5) / 7.0
        py = (i % 2 - 0.5) * 0.15
        puff = bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.28)
        bmesh.ops.scale(bm, vec=(1.1, 1.0, 0.6), verts=puff["verts"])
        bmesh.ops.translate(bm, vec=(px, py, height), verts=puff["verts"])
        assign_mat(bm, puff["verts"], 0)

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Hedge_Low.fbx")

# ==============================================================================
# ASSET 7: SM_Curzon_Sign_Physics (Department Signboard)
# ==============================================================================
def build_curzon_sign_physics(mats):
    reset_scene()
    mesh = bpy.data.meshes.new("SM_Curzon_Sign_Physics")
    obj = bpy.data.objects.new("SM_Curzon_Sign_Physics", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    for m in [mats["signblue"], mats["trim"], mats["castiron"]]:
        obj.data.materials.append(m)

    bm = bmesh.new()
    width = 3.6
    height = 1.1
    thick = 0.08

    # Blue board plate
    board = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width, thick, height), verts=board["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, height/2.0), verts=board["verts"])
    assign_mat(bm, board["verts"], 0) # Sign Blue

    # White raised border frame
    f_top = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width + 0.08, thick + 0.04, 0.08), verts=f_top["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, height), verts=f_top["verts"])
    assign_mat(bm, f_top["verts"], 1) # White Trim

    f_bot = bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(width + 0.08, thick + 0.04, 0.08), verts=f_bot["verts"])
    bmesh.ops.translate(bm, vec=(0.0, 0.0, 0.04), verts=f_bot["verts"])
    assign_mat(bm, f_bot["verts"], 1)

    for fx in [-width/2.0, width/2.0]:
        f_side = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.08, thick + 0.04, height), verts=f_side["verts"])
        bmesh.ops.translate(bm, vec=(fx, 0.0, height/2.0), verts=f_side["verts"])
        assign_mat(bm, f_side["verts"], 1)

    # Cast Iron mounting wall brackets
    for bx in [-width * 0.35, width * 0.35]:
        br = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(0.08, 0.35, 0.3), verts=br["verts"])
        bmesh.ops.translate(bm, vec=(bx, -0.15, height * 0.75), verts=br["verts"])
        assign_mat(bm, br["verts"], 2) # Cast Iron

    bm.to_mesh(mesh)
    bm.free()
    export_fbx(obj, "SM_Curzon_Sign_Physics.fbx")

# ==============================================================================
# MAIN COMPILER EXECUTION
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("COMPILING CURZON HALL MASTER ARCHITECTURAL ASSETS (v3)...")
    print("=" * 70)
    mats = get_or_create_materials()
    build_curzon_entrance_portal(mats)
    build_curzon_veranda_lower(mats)
    build_curzon_veranda_upper(mats)
    build_curzon_parapet_merlons(mats)
    build_curzon_tower_octagon(mats)
    build_curzon_hedge_low(mats)
    build_curzon_sign_physics(mats)
    print("All assets successfully compiled and exported to FBX!")
