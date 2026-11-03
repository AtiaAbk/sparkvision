import sys, os, time, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

xform = {
    "location": {"x": -4300, "y": 0, "z": 200},
    "rotation": {"pitch": -10, "yaw": 0, "roll": 0},
    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
}
invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {"transform": xform})
time.sleep(0.5)

cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
    "captureTransform": xform,
    "annotations": {
        "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
        "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
    },
    "bShowUI": False
})

img_data = cap.get("returnValue", {}).get("image", {}).get("data", "")
if img_data:
    os.makedirs("Documentation/Screenshots/Characters", exist_ok=True)
    with open("Documentation/Screenshots/Characters/test_viewport.png", "wb") as f:
        f.write(base64.b64decode(img_data))
    print(f"Captured: {len(img_data)} bytes -> Documentation/Screenshots/Characters/test_viewport.png")
else:
    print("Failed to capture image")
