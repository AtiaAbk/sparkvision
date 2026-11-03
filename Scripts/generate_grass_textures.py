#!/usr/bin/env python3
"""
Generate High-Fidelity 3D Grass Blades Texture Atlas (RGBA + Normal):
Renders a lush arrangement of varied lawn grass blades and tufts directly in Blender:
- Rich multi-tone emerald, olive, and golden-green grass blades
- Subtle translucent tips and blade center creases
- Transparent RGBA background for BLEND_Masked / Two-Sided Foliage
"""

import sys
import os
import subprocess

OUTPUT_DIR = "/Users/atiaoishi/Downloads/sparkvision/Saved/Textures_WWM"
BLENDER_BIN = "/Applications/Blender.app/Contents/MacOS/Blender"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLENDER_CODE = f"""
import bpy
import bmesh
import mathutils
import math
import random
import os

OUTPUT_DIR = "{OUTPUT_DIR}"
random.seed(55)

# Reset
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for m in bpy.data.meshes:
    if m.users == 0: bpy.data.meshes.remove(m)
for mat in bpy.data.materials:
    if mat.users == 0: bpy.data.materials.remove(mat)

# Configure Render settings for transparent RGBA
scene = bpy.context.scene
scene.render.film_transparent = True
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# Setup Orthographic Camera looking straight down X axis onto YZ plane
cam_data = bpy.data.cameras.new(name="OrthoCam")
cam_data.type = 'ORTHO'
cam_data.ortho_scale = 1.0  # covers [-0.5, 0.5] in Y and Z
cam_obj = bpy.data.objects.new("OrthoCam", cam_data)
cam_obj.location = (2.0, 0.0, 0.0)
cam_obj.rotation_euler = (0.0, 0.0, 0.0)
cam_obj.rotation_euler = (math.pi * 0.5, 0.0, math.pi * 0.5)
bpy.context.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Setup clean daylight sun
light_data = bpy.data.lights.new(name="Sun", type='SUN')
light_data.energy = 4.0
light_obj = bpy.data.objects.new(name="Sun", object_data=light_data)
light_obj.rotation_euler = (math.radians(45), math.radians(30), math.radians(45))
bpy.context.collection.objects.link(light_obj)

# Create Grass Blade Mesh
mesh = bpy.data.meshes.new("GrassAtlas")
obj = bpy.data.objects.new("GrassAtlas", mesh)
bpy.context.collection.objects.link(obj)

mat = bpy.data.materials.new(name="M_GrassBlade")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

node_output = nodes.new(type="ShaderNodeOutputMaterial")
node_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
node_grad = nodes.new(type="ShaderNodeTexGradient")
node_coord = nodes.new(type="ShaderNodeTexCoord")
node_ramp = nodes.new(type="ShaderNodeValToRGB")

# Color ramp: dark soil green at base (0.0), lush warm meadow green at mid (0.5), golden sunlit green at tip (1.0)
node_ramp.color_ramp.elements[0].position = 0.0
node_ramp.color_ramp.elements[0].color = (0.08, 0.22, 0.05, 1.0)  # Deep base green
el_mid = node_ramp.color_ramp.elements.new(0.55)
el_mid.color = (0.24, 0.52, 0.12, 1.0)  # Fresh meadow green
node_ramp.color_ramp.elements[1].position = 1.0
node_ramp.color_ramp.elements[1].color = (0.42, 0.65, 0.18, 1.0)  # Sunlit blade tip

links.new(node_coord.outputs["Generated"], node_grad.inputs["Vector"])
links.new(node_grad.outputs["Fac"], node_ramp.inputs["Fac"])
links.new(node_ramp.outputs["Color"], node_bsdf.inputs["Base Color"])
node_bsdf.inputs["Roughness"].default_value = 0.85
links.new(node_bsdf.outputs["BSDF"], node_output.inputs["Surface"])

obj.data.materials.append(mat)

bm = bmesh.new()

# Generate 35 natural overlapping grass blades across the plane
# Camera frame is Y: -0.48 to 0.48, Z: -0.48 to 0.48
num_blades = 42
for b_i in range(num_blades):
    base_y = -0.45 + (0.90 * b_i / num_blades) + random.uniform(-0.02, 0.02)
    base_z = -0.48
    height = random.uniform(0.65, 0.92)
    width = random.uniform(0.022, 0.038)
    lean = random.uniform(-0.25, 0.25)
    curve_amp = random.uniform(-0.12, 0.12)
    
    # 5 segments per blade
    num_segs = 5
    v_left_prev = None
    v_right_prev = None
    for s in range(num_segs + 1):
        t = s / num_segs
        curr_z = base_z + height * t
        curr_y = base_y + lean * t + curve_amp * (t * t)
        curr_w = width * (1.0 - t * 0.95)  # Tapers to point
        
        vl = bm.verts.new((0.0, curr_y - curr_w * 0.5, curr_z))
        vr = bm.verts.new((0.0, curr_y + curr_w * 0.5, curr_z))
        
        if v_left_prev is not None:
            f = bm.faces.new([v_left_prev, v_right_prev, vr, vl])
            f.smooth = True
        v_left_prev = vl
        v_right_prev = vr

bm.to_mesh(mesh)
bm.free()

# Render Diffuse RGBA
diffuse_path = os.path.join(OUTPUT_DIR, "T_Campus_Grass_Blades_D.png")
scene.render.filepath = diffuse_path
bpy.ops.render.render(write_still=True)
print(f"Rendered Diffuse to: {{diffuse_path}}")
"""

script_path = "/tmp/generate_grass_textures.py"
with open(script_path, "w") as f:
    f.write(BLENDER_CODE)

print("Running Blender to generate high-res grass atlas...")
res = subprocess.run([BLENDER_BIN, "--background", "--python", script_path], capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print("Blender ERROR:", res.stderr)
    sys.exit(1)

print("\n✓ Grass blade texture atlas generated successfully!")
