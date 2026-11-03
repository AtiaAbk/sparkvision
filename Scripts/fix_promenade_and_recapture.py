import sys
import os
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

# 1. Remove blob bushes that obstructed walkway
blob_names = [
    "Flowerbed_Rangan_01", "Flowerbed_Rangan_02", "Flowerbed_Rangan_03", "Flowerbed_Rangan_04",
    "Flowerbed_Kamini_01", "Flowerbed_Kamini_02", "Flowerbed_Kamini_03", "Flowerbed_Kamini_04"
]

for name in blob_names:
    res = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": name, "tag": "", "collision_channels": []}).get("returnValue", [])
    for a in res:
        try:
            invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {"actor": {"refPath": a.get("refPath")}})
            print(f"  ✓ Removed blob bush: {name}")
        except Exception as e:
            pass

# 2. Add realistic flowerbed border and circular garden beds
FLOWERBED_BORDER = "/Game/SparkVision/Campus/Environment/SM_Garden_Flowerbed_Border.SM_Garden_Flowerbed_Border"
FLOWERBED_CIRCULAR = "/Game/SparkVision/Campus/Environment/SM_Garden_Flowerbed_Circular.SM_Garden_Flowerbed_Circular"
FERN_CLUSTER = "/Game/SparkVision/Campus/Environment/SM_Natural_Fern_Cluster.SM_Natural_Fern_Cluster"

beds = [
    # Circular heritage flowerbeds on flanking lawns
    (FLOWERBED_CIRCULAR, "Garden_Flowerbed_Left", -3400, -600, 10, 0, 1.8),
    (FLOWERBED_CIRCULAR, "Garden_Flowerbed_Right", -3400, 600, 10, 0, 1.8),
    # Fern undergrowth near the benches
    (FERN_CLUSTER, "Garden_Fern_01", -3850, -320, 10, 20, 1.2),
    (FERN_CLUSTER, "Garden_Fern_02", -3050, -320, 10, -40, 1.2),
    (FERN_CLUSTER, "Garden_Fern_03", -3850, 320, 10, 45, 1.2),
    (FERN_CLUSTER, "Garden_Fern_04", -3050, 320, 10, -15, 1.2),
]

for mesh_path, name, x, y, z, yaw, scale in beds:
    try:
        invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": mesh_path,
            "name": name,
            "xform": {
                "location": {"x": float(x), "y": float(y), "z": float(z)},
                "rotation": {"pitch": 0.0, "yaw": float(yaw), "roll": 0.0},
                "scale": {"x": float(scale), "y": float(scale), "z": float(scale)}
            }
        })
        print(f"  ✓ Placed {name}")
    except Exception as e:
        print(f"Notice {name}:", e)

# 3. Recapture SHOWCASE_01 from clean unoccluded position (-3350, 0, 140) looking at Curzon Portal
out_path_01 = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90/SHOWCASE_01_Curzon_Authentic_Indo_Saracenic_Doors_Windows.png"
print("Capturing SHOWCASE_01...")
res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
    "captureTransform": {
        "location": {"x": -3350.0, "y": 0.0, "z": 140.0},
        "rotation": {"pitch": 4.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    },
    "annotations": {
        "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
    },
    "bShowUI": False
})
data = res.get("returnValue", {}).get("image", {}).get("data")
if data:
    with open(out_path_01, "wb") as f:
        f.write(base64.b64decode(data))
    print(f"✓ Saved SHOWCASE_01 ({os.path.getsize(out_path_01)} bytes)")

# 4. Recapture SHOWCASE_02 at Curzon Pond Ghat looking at swimming fish
# Ghat is at x = 2350, y = 0, z = 20. Pond extends from x=2400 to 5000.
# Camera placed standing on the Ghat looking down into clear water (x = 2420, y = 0, z = 60, pitch = -22, yaw = 0)
out_path_02 = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90/SHOWCASE_02_Curzon_Pond_Water_And_Living_Fish.png"
print("Capturing SHOWCASE_02 (Pond & Fish)...")
res = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
    "captureTransform": {
        "location": {"x": 2420.0, "y": 0.0, "z": 65.0},
        "rotation": {"pitch": -22.0, "yaw": 0.0, "roll": 0.0},
        "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
    },
    "annotations": {
        "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
    },
    "bShowUI": False
})
data = res.get("returnValue", {}).get("image", {}).get("data")
if data:
    with open(out_path_02, "wb") as f:
        f.write(base64.b64decode(data))
    print(f"✓ Saved SHOWCASE_02 ({os.path.getsize(out_path_02)} bytes)")

