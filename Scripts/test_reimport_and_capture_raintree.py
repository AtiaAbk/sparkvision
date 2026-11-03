import sys
import os
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

STATIC_MESH_TOOLS = "editor_toolset.toolsets.static_mesh.StaticMeshTools"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"
SCENE_TOOLS = "editor_toolset.toolsets.scene.SceneTools"
EDITOR_APP_TOOLS = "EditorToolset.EditorAppToolset"

VEG_FOLDER = "/Game/SparkVision/Environment/Vegetation"
MODELS_DIR = "/Users/atiaoishi/Downloads/sparkvision/SourceAssets/Models/Vegetation"
MAT_FOLDER = "/Game/SparkVision/Materials"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"

m = "SM_Tree_Raintree_Master"
fbx = os.path.join(MODELS_DIR, f"{m}.fbx")

# 1. Delete and Reimport
print("Reimporting SM_Tree_Raintree_Master...")
try:
    invoke_tool("delete", ASSET_TOOLS, {"path": f"{VEG_FOLDER}/{m}"})
except Exception as e:
    print(f"Delete note: {e}")

time.sleep(0.3)
invoke_tool("import_file", STATIC_MESH_TOOLS, {
    "folder_path": VEG_FOLDER,
    "asset_name": m,
    "source_file": fbx,
    "import_materials": False,
    "import_textures": False,
    "combine_meshes": True
})

b = invoke_tool("get_bounds", STATIC_MESH_TOOLS, {"mesh": {"refPath": f"{VEG_FOLDER}/{m}.{m}"}}).get("returnValue", {})
print("Mesh bounds:", b)

# 2. Assign materials
bark_mat = f"{MAT_FOLDER}/MI_Bark_Natural_Gnarled.MI_Bark_Natural_Gnarled"
raintree_foliage = f"{MAT_FOLDER}/MI_Foliage_Raintree_Natural.MI_Foliage_Raintree_Natural"

slots = invoke_tool("get_material_slots", STATIC_MESH_TOOLS, {"mesh": {"refPath": f"{VEG_FOLDER}/{m}.{m}"}}).get("returnValue", [])
print("Slots:", slots)

invoke_tool("set_material", STATIC_MESH_TOOLS, {
    "mesh": {"refPath": f"{VEG_FOLDER}/{m}.{m}"},
    "slot_name": "M_Bark_Tree",
    "material": {"refPath": bark_mat}
})
invoke_tool("set_material", STATIC_MESH_TOOLS, {
    "mesh": {"refPath": f"{VEG_FOLDER}/{m}.{m}"},
    "slot_name": "M_Master_NaturalFoliage",
    "material": {"refPath": raintree_foliage}
})

invoke_tool("save_assets", ASSET_TOOLS, {"asset_paths": [f"{VEG_FOLDER}/{m}.{m}"]})
print("Saved mesh!")

# 3. Re-spawn Prototype Actor in scene
try:
    found = invoke_tool("find_actors", SCENE_TOOLS, {"name": "Prototype_Master_Raintree"}).get("returnValue", [])
    for a in found:
        invoke_tool("remove_from_scene", SCENE_TOOLS, {"actor": {"refPath": a["refPath"]}})
except Exception as e:
    print("Cleanup:", e)

invoke_tool("add_to_scene_from_asset", SCENE_TOOLS, {
    "asset_path": f"{VEG_FOLDER}/{m}",
    "name": "Prototype_Master_Raintree",
    "xform": {
        "location": {"x": -4600.0, "y": 1200.0, "z": 20.0},
        "rotation": {"pitch": 0.0, "yaw": 25.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    }
})

# 4. Capture validation shots
test_views = [
    {
        "id": "TEST_DENSE_RAINTREE_FULL_VIEW",
        "loc": {"x": -3200.0, "y": 1400.0, "z": 500.0},
        "rot": {"pitch": -10.0, "yaw": -170.0, "roll": 0.0}
    },
    {
        "id": "TEST_DENSE_RAINTREE_LEAF_CLUSTERS",
        "loc": {"x": -4100.0, "y": 1200.0, "z": 650.0},
        "rot": {"pitch": 0.0, "yaw": -170.0, "roll": 0.0}
    },
    {
        "id": "TEST_DENSE_RAINTREE_GAMEPLAY_VIEW",
        "loc": {"x": -5600.0, "y": 0.0, "z": 180.0},
        "rot": {"pitch": -2.0, "yaw": 0.0, "roll": 0.0}
    }
]

for v in test_views:
    vid = v["id"]
    xform = {"location": v["loc"], "rotation": v["rot"], "scale": {"x": 1.0, "y": 1.0, "z": 1.0}}
    invoke_tool("SetCameraTransform", EDITOR_APP_TOOLS, {"transform": xform})
    time.sleep(0.4)
    cap = invoke_tool("CaptureViewport", EDITOR_APP_TOOLS, {
        "captureTransform": xform,
        "annotations": {"gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0},
        "bShowUI": False
    })
    img_b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
    if img_b64:
        out_file = os.path.join(ARTIFACT_DIR, f"{vid}.png")
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(img_b64))
        print(f"✓ Saved {vid}.png")

print("Done!")
