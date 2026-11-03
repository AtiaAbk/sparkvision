import sys
import os
import time
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

EDITOR_APP_TOOLS = "EditorToolset.EditorAppToolset"
ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

VIEWPOINTS = [
    {
        "id": "01_Curzon_Hall_Front",
        "title": "Curzon Hall Front Facade & Promenade",
        "loc": {"x": -5600.0, "y": 0.0, "z": 200.0},
        "rot": {"pitch": -4.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "02_Curzon_Hall_Side_View",
        "title": "Curzon Hall Oblique Side View with Pavilions",
        "loc": {"x": -3200.0, "y": -2200.0, "z": 300.0},
        "rot": {"pitch": -8.0, "yaw": 65.0, "roll": 0.0}
    },
    {
        "id": "03_Open_Campus_Road",
        "title": "Open Campus Approach Road",
        "loc": {"x": -1500.0, "y": 0.0, "z": 350.0},
        "rot": {"pitch": -10.0, "yaw": -70.0, "roll": 0.0}
    },
    {
        "id": "04_Tree_Covered_Area",
        "title": "Tree-Covered Campus Area with Dappled Shadows",
        "loc": {"x": -4200.0, "y": 1200.0, "z": 220.0},
        "rot": {"pitch": -5.0, "yaw": 160.0, "roll": 0.0}
    },
    {
        "id": "05_Campus_Courtyard",
        "title": "Curzon Courtyard & Garden Lawns",
        "loc": {"x": -2600.0, "y": 400.0, "z": 250.0},
        "rot": {"pitch": -8.0, "yaw": -150.0, "roll": 0.0}
    },
    {
        "id": "06_Pond_And_Reflections",
        "title": "Curzon Botanical Pond and Southern Ghat",
        "loc": {"x": -1800.0, "y": 2600.0, "z": 220.0},
        "rot": {"pitch": -12.0, "yaw": 35.0, "roll": 0.0}
    },
    {
        "id": "07_Character_Direct_Sunlight",
        "title": "Main Student Character in Direct Sunlight",
        "loc": {"x": -3600.0, "y": 180.0, "z": 160.0},
        "rot": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "id": "08_Character_Tree_Shade",
        "title": "Main Student Character Under Tree Shade",
        "loc": {"x": -3350.0, "y": -450.0, "z": 160.0},
        "rot": {"pitch": -6.0, "yaw": 0.0, "roll": 0.0}
    }
]

def capture_suite(prefix="BASELINE"):
    print(f"Capturing 8 {prefix} viewpoints...")
    for v in VIEWPOINTS:
        vid = f"{prefix}_{v['id']}"
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
            print(f"  ✓ Saved {vid}.png ({v['title']})")
        else:
            print(f"  ✗ Failed to capture {vid}")

if __name__ == "__main__":
    prefix = sys.argv[1] if len(sys.argv) > 1 else "BASELINE"
    capture_suite(prefix)
