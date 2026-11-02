#!/usr/bin/env python3
import sys, os, time, base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

EMPTY_ANNOTATIONS = {
    "gridSpacing": 0, "gridExtent": 0, "gridHeight": 0,
    "maxLabelDistance": 0, "classFilter": None, "maxLabels": 0
}

HERO_VIEWS = [
    {
        "name": "HERO_01_Curzon_Facade",
        "loc": {"x": -4500.0, "y": 0.0, "z": 300.0},
        "rot": {"pitch": -4.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "name": "HERO_02_Promenade_Avenue",
        "loc": {"x": -150.0, "y": 0.0, "z": 210.0},
        "rot": {"pitch": -4.0, "yaw": 0.0, "roll": 0.0}
    },
    {
        "name": "HERO_03_Pond_Ghat_Reflection",
        "loc": {"x": 2100.0, "y": -650.0, "z": 220.0},
        "rot": {"pitch": -8.0, "yaw": 30.0, "roll": 0.0}
    },
    {
        "name": "HERO_04_Banyan_Krishnachura_Grove",
        "loc": {"x": 1050.0, "y": -900.0, "z": 320.0},
        "rot": {"pitch": -10.0, "yaw": 20.0, "roll": 0.0}
    }
]

def main():
    print("=" * 70)
    print("CAPTURING 4 HERO VERIFICATION VIEWS (EDITOR VIEWPORT, NO PIE)")
    print("=" * 70)

    # Deselect all
    try:
        invoke_tool("SelectActors", "EditorToolset.EditorAppToolset", {"actors": []})
    except Exception:
        pass

    # Ensure no dangling PIE
    try:
        invoke_tool("StopPIE", "EditorToolset.EditorAppToolset")
        time.sleep(1.0)
    except Exception:
        pass

    for view in HERO_VIEWS:
        name = view["name"]
        loc = view["loc"]
        rot = view["rot"]
        xform = {"location": loc, "rotation": rot, "scale": {"x": 1.0, "y": 1.0, "z": 1.0}}

        print(f"\nPositioning camera for {name}...")
        invoke_tool("SetCameraTransform", "EditorToolset.EditorAppToolset", {"transform": xform})
        time.sleep(1.0)

        print(f"Capturing {name}...")
        cap = invoke_tool("CaptureViewport", "EditorToolset.EditorAppToolset", {
            "captureTransform": xform,
            "annotations": EMPTY_ANNOTATIONS,
            "bShowUI": False
        })
        b64 = cap.get("returnValue", {}).get("image", {}).get("data", "")
        if b64:
            data = base64.b64decode(b64)
            path = f"/tmp/{name}.png"
            with open(path, "wb") as f:
                f.write(data)
            artifact_dir = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
            artifact_path = os.path.join(artifact_dir, f"{name}.png")
            with open(artifact_path, "wb") as f:
                f.write(data)
            print(f"  ✓ Saved {path} and {artifact_path} ({len(data)/1024.0:.1f} KB)")
        else:
            print(f"  ✗ Failed to capture {name}")

    print("\nDone capturing 4 hero views.")

if __name__ == "__main__":
    main()
