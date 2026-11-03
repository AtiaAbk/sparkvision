import os
import sys
import math
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models"
TEX_DIR = "/Users/atiaoishi/Downloads/sparkvision/Content/SparkVision/Textures"
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TEX_DIR, exist_ok=True)

def generate_koi_texture():
    print("Generating T_Pond_KoiFish_D...")
    w, h = 1024, 1024
    img = Image.new("RGB", (w, h), color=(245, 242, 235)) # Pearlescent white base
    draw = ImageDraw.Draw(img)
    
    # Vibrant Kohaku / Sanke patterns: vivid vermillion orange/red and golden yellow spots
    # Dorsal patches
    draw.ellipse([200, 100, 600, 450], fill=(235, 85, 25)) # Bright red-orange patch
    draw.ellipse([450, 300, 850, 700], fill=(245, 120, 20)) # Golden orange patch
    draw.ellipse([150, 550, 500, 900], fill=(225, 60, 20)) # Tail scarlet patch
    
    # Gills and head markings
    draw.ellipse([350, 50, 650, 220], fill=(240, 100, 25))
    # Eyes
    draw.ellipse([280, 80, 320, 120], fill=(20, 20, 20))
    draw.ellipse([680, 80, 720, 120], fill=(20, 20, 20))
    
    # Scale crosshatch pattern
    arr = np.array(img, dtype=np.int16)
    noise = (np.random.randn(h, w, 3) * 6).astype(np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    
    out_img = Image.fromarray(arr)
    tex_path = os.path.join(TEX_DIR, "T_Pond_KoiFish_D.png")
    out_img.save(tex_path)
    print("Saved", tex_path)
    return tex_path

def generate_koi_mesh_obj():
    print("Generating SM_Pond_KoiFish.obj...")
    obj_path = os.path.join(MODELS_DIR, "SM_Pond_KoiFish.obj")
    
    # Generate low-poly fish: 6 segments along length, 8 cross-section vertices
    segments = 8
    rings = 10
    length = 60.0 # 60 cm long fish
    
    verts = []
    uvs = []
    faces = []
    
    # Head tip (vertex 1)
    verts.append((0.0, 0.0, 0.0))
    uvs.append((0.5, 0.0))
    
    for r in range(1, rings):
        t = r / float(rings)
        # Body profile: sleek ellipse
        x = (t - 0.2) * length
        # Radius expands to mid-body then tapers
        radius_y = math.sin(t * math.pi) * 8.0 # width
        radius_z = math.sin(t * math.pi) * 11.0 # height
        
        for s in range(segments):
            angle = s * (2.0 * math.pi / segments)
            y = math.cos(angle) * radius_y
            z = math.sin(angle) * radius_z
            verts.append((x, y, z))
            uvs.append((s / float(segments), t))
            
    # Tail tip
    verts.append((length * 0.85, 0.0, 0.0))
    uvs.append((0.5, 1.0))
    
    # Build faces
    # Front cap (connecting head tip 1 to ring 1)
    for s in range(segments):
        s_next = (s + 1) % segments
        faces.append((1, 2 + s, 2 + s_next))
        
    # Middle rings
    for r in range(rings - 2):
        r_start = 2 + r * segments
        next_r_start = r_start + segments
        for s in range(segments):
            s_next = (s + 1) % segments
            v1 = r_start + s
            v2 = r_start + s_next
            v3 = next_r_start + s_next
            v4 = next_r_start + s
            faces.append((v1, v2, v3))
            faces.append((v1, v3, v4))
            
    # Tail cap
    tail_tip_idx = len(verts)
    last_ring_start = 2 + (rings - 2) * segments
    for s in range(segments):
        s_next = (s + 1) % segments
        faces.append((last_ring_start + s, tail_tip_idx, last_ring_start + s_next))
        
    # Write OBJ
    with open(obj_path, "w") as f:
        f.write("# Pond Koi Fish OBJ\n")
        f.write("o SM_Pond_KoiFish\n")
        for v in verts:
            f.write(f"v {v[0]:.3f} {v[1]:.3f} {v[2]:.3f}\n")
        for u in uvs:
            f.write(f"vt {u[0]:.3f} {u[1]:.3f}\n")
        for f_idx in faces:
            f.write(f"f {f_idx[0]}/{f_idx[0]} {f_idx[1]}/{f_idx[1]} {f_idx[2]}/{f_idx[2]}\n")
            
    print(f"Saved {obj_path} ({len(verts)} verts, {len(faces)} faces)")
    return obj_path

def import_and_spawn_fish():
    tex_path = generate_koi_texture()
    obj_path = generate_koi_mesh_obj()
    
    # 1. Import Texture
    print("Importing T_Pond_KoiFish_D...")
    try:
        invoke_tool("import_file", "editor_toolset.toolsets.texture.TextureTools", {
            "folder_path": "/Game/SparkVision/Textures",
            "asset_name": "T_Pond_KoiFish_D",
            "source_file": tex_path
        })
    except Exception as e:
        print("Tex import:", e)
        
    # 2. Create Material Instance
    mi_ref = "/Game/SparkVision/Materials/MI_Pond_KoiFish.MI_Pond_KoiFish"
    try:
        invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "folder_path": "/Game/SparkVision/Materials",
            "asset_name": "MI_Pond_KoiFish",
            "parent": {"refPath": "/Game/SparkVision/Materials/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"}
        })
        invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
            "instance": {"refPath": mi_ref},
            "name": "BaseColor_Texture",
            "value": {"refPath": "/Game/SparkVision/Textures/T_Pond_KoiFish_D.T_Pond_KoiFish_D"}
        })
    except Exception as e:
        print("Mat creation:", e)
        
    # 3. Import Static Mesh
    mesh_path = "/Game/SparkVision/Campus/Environment/SM_Pond_KoiFish.SM_Pond_KoiFish"
    try:
        invoke_tool("import_file", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
            "folder_path": "/Game/SparkVision/Campus/Environment",
            "asset_name": "SM_Pond_KoiFish",
            "source_file": obj_path,
            "import_materials": False,
            "combine_meshes": True
        })
        # Set material on fish mesh
        invoke_tool("set_material", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
            "mesh": {"refPath": mesh_path},
            "slot_name": "Material",
            "material": {"refPath": mi_ref}
        })
    except Exception as e:
        print("Mesh import:", e)
        
    # 4. Spawn 14 Koi Fish around Curzon Pond Ghat
    print("Spawning school of swimming fish in Curzon Pond...")
    # Pond water is at Z=7. Fish swim at Z = -4 to -8.
    fish_spawns = [
        # Clustered around the Ghat pier (X: 2450 to 2900, Y: -300 to 300)
        (2550, -120, -5, 25, 1.2),
        (2580, -90, -4, 45, 1.0),
        (2520, -180, -6, 15, 1.1),
        (2600, 140, -5, -35, 1.3),
        (2650, 180, -7, -20, 0.9),
        (2720, 80, -5, -60, 1.15),
        # Cruising along the water lilies
        (2850, -350, -6, 75, 1.25),
        (2920, -420, -5, 80, 1.0),
        (2800, 320, -6, -85, 1.1),
        (2950, 380, -7, -110, 1.3),
        # Center pond deep swimmers
        (3200, -100, -8, 140, 1.4),
        (3350, 150, -8, -135, 1.2),
        (3100, 20, -6, 10, 0.95),
        (3450, -80, -7, -170, 1.1),
    ]
    
    for idx, (x, y, z, yaw, scale) in enumerate(fish_spawns):
        label = f"CurzonPond_KoiFish_{idx+1:02d}"
        try:
            actor_ref = invoke_tool("spawn_actor", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": mesh_path,
                "location": {"x": x, "y": y, "z": z},
                "rotation": {"pitch": 0, "yaw": yaw, "roll": 0},
                "scale": {"x": scale, "y": scale, "z": scale}
            }).get("returnValue", {}).get("refPath")
            
            if actor_ref:
                invoke_tool("set_label", "editor_toolset.toolsets.actor.ActorTools", {
                    "actor": {"refPath": actor_ref},
                    "label": label
                })
                # Override material
                invoke_tool("set_override_material", "editor_toolset.toolsets.actor.ActorTools", {
                    "actor": {"refPath": actor_ref},
                    "material_index": 0,
                    "material": {"refPath": mi_ref}
                })
                print(f"  ✓ Spawned {label} at ({x}, {y}, {z})")
        except Exception as e:
            print(f"  Notice spawning {label}: {e}")

if __name__ == "__main__":
    import_and_spawn_fish()
