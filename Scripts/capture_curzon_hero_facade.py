import sys
import os
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

output_path = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90/SHOWCASE_01_Curzon_Authentic_Indo_Saracenic_Doors_Windows.png"

print("Capturing Curzon Hall Hero Facade...")
res = invoke_tool("GetViewportImage", "EditorToolset.EditorAppToolset", {
    "cameraLocation": {"x": -4300.0, "y": 0.0, "z": 180.0},
    "cameraRotation": {"pitch": 5.0, "yaw": 0.0, "roll": 0.0},
    "bShowUI": False
})

img_data = res.get("returnValue", {}).get("image", {}).get("data")
if img_data:
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(img_data))
    print(f"✓ Saved image to {output_path} ({os.path.getsize(output_path)} bytes)")
else:
    print("✗ Failed to capture image:", res)
