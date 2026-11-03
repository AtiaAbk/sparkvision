import sys
import os
import json
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MI_TOOLS = "editor_toolset.toolsets.material_instance.MaterialInstanceTools"
OBJ_TOOLS = "editor_toolset.toolsets.object.ObjectTools"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"
EDITOR_APP_TOOLS = "EditorToolset.EditorAppToolset"

MAT_FOLDER = "/Game/SparkVision/Materials"
TEX_FOLDER = "/Game/SparkVision/Textures/NaturalFoliage"
MASTER_FOLIAGE = f"{MAT_FOLDER}/M_Master_NaturalFoliage.M_Master_NaturalFoliage"

mi_ref = f"{MAT_FOLDER}/MI_Foliage_Raintree_Natural.MI_Foliage_Raintree_Natural"

print("1. Setting Parent of MI_Foliage_Raintree_Natural to M_Master_NaturalFoliage...")
invoke_tool("set_properties", OBJ_TOOLS, {
    "instance": {"refPath": mi_ref},
    "values": json.dumps({"Parent": {"refPath": MASTER_FOLIAGE}})
})

print("2. Setting BaseColor_Texture to T_Leaf_Raintree_D...")
invoke_tool("set_texture_parameter", MI_TOOLS, {
    "instance": {"refPath": mi_ref},
    "name": "BaseColor_Texture",
    "value": {"refPath": f"{TEX_FOLDER}/T_Leaf_Raintree_D.T_Leaf_Raintree_D"}
})

print("3. Setting Normal_Texture to T_Leaf_Raintree_N...")
invoke_tool("set_texture_parameter", MI_TOOLS, {
    "instance": {"refPath": mi_ref},
    "name": "Normal_Texture",
    "value": {"refPath": f"{TEX_FOLDER}/T_Leaf_Raintree_N.T_Leaf_Raintree_N"}
})

print("4. Setting SubsurfaceColor...")
invoke_tool("set_vector_parameter", MI_TOOLS, {
    "instance": {"refPath": mi_ref},
    "name": "SubsurfaceColor",
    "value": {"r": 0.32, "g": 0.72, "b": 0.15, "a": 1.0}
})

invoke_tool("save_assets", ASSET_TOOLS, {"asset_paths": [f"{MAT_FOLDER}/MI_Foliage_Raintree_Natural"]})
print("Saved MI_Foliage_Raintree_Natural!")

# Capture validation shot
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
xform = {
    "location": {"x": -3200.0, "y": 1400.0, "z": 500.0},
    "rotation": {"pitch": -10.0, "yaw": -170.0, "roll": 0.0},
    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
}
invoke_tool("SetCameraTransform", EDITOR_APP_TOOLS, {"transform": xform})
time.sleep(0.5)
cap = invoke_tool("CaptureViewport", EDITOR_APP_TOOLS, {
    "captureTransform": xform,
    "annotations": {"gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0},
    "bShowUI": False
})
img_b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
if img_b64:
    out_file = os.path.join(ARTIFACT_DIR, "TEST_FIXED_RAINTREE_VIEW.png")
    with open(out_file, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print("✓ Saved TEST_FIXED_RAINTREE_VIEW.png")

print("Done!")
