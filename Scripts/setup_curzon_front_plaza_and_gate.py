import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

BENCH_MESH = "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Bench_Colonial.SM_Curzon_Bench_Colonial"
LAMP_MESH = "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Lamp_Colonial.SM_Curzon_Lamp_Colonial"
HEDGE_MESH = "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Hedge_Low.SM_Curzon_Hedge_Low"
MERLONS_MESH = "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Parapet_Merlons.SM_Curzon_Parapet_Merlons"
CUBE_MESH = "/Engine/BasicShapes/Cube.Cube"

DOOR_MAT = "/Game/SparkVision/Materials/MI_Curzon_EntranceDoor.MI_Curzon_EntranceDoor"
BRICK_MAT = "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick"
WOOD_MAT = "/Game/SparkVision/Materials/MI_Curzon_WoodDark.MI_Curzon_WoodDark"

def setup_curzon_gate_and_portal():
    print("=== 1. CLOSING PORTAL HOLLOW GAPS & ADDING GRAND TEAK ENTRANCE DOORS ===")
    
    # 1. Grand Double-Leaf Entrance Door inside the archway at x = -2520, y = 0, z = 180
    door_name = "Curzon_Hero_GrandEntranceDoor_Arch"
    try:
        res = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": CUBE_MESH,
            "name": door_name,
            "xform": {
                "location": {"x": -2515.0, "y": 0.0, "z": 180.0},
                "rotation": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0},
                "scale": {"x": 0.15, "y": 3.8, "z": 3.6}
            }
        })
        # Set door material
        actor_ref = res.get("returnValue", {}).get("refPath")
        if actor_ref:
            comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": {"refPath": actor_ref}}).get("returnValue", [])
            for c in comps:
                if "StaticMeshComponent" in c.get("refPath", ""):
                    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                        "instance": {"refPath": c.get("refPath")},
                        "properties": {"overrideMaterials": [{"refPath": DOOR_MAT}]}
                    })
        print(f"  ✓ Placed {door_name} inside entrance portal")
    except Exception as e:
        print("Door notice:", e)

    # 2. Upper Window Interior Backing (so 2nd floor windows are not open sky)
    backing_name = "Curzon_Hero_UpperWindow_InteriorBacking"
    try:
        res = invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": CUBE_MESH,
            "name": backing_name,
            "xform": {
                "location": {"x": -2530.0, "y": 0.0, "z": 510.0},
                "rotation": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0},
                "scale": {"x": 0.2, "y": 4.5, "z": 2.2}
            }
        })
        actor_ref = res.get("returnValue", {}).get("refPath")
        if actor_ref:
            comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": {"refPath": actor_ref}}).get("returnValue", [])
            for c in comps:
                if "StaticMeshComponent" in c.get("refPath", ""):
                    invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                        "instance": {"refPath": c.get("refPath")},
                        "properties": {"overrideMaterials": [{"refPath": WOOD_MAT}]}
                    })
        print(f"  ✓ Placed {backing_name} behind 2nd floor windows")
    except Exception as e:
        print("Backing notice:", e)

    # 3. Portal Roof Crown Merlons (capping the top parapet)
    merlon_name = "Curzon_Hero_PortalRoof_Merlons"
    try:
        invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
            "asset_path": MERLONS_MESH,
            "name": merlon_name,
            "xform": {
                "location": {"x": -2500.0, "y": 0.0, "z": 730.0},
                "rotation": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0},
                "scale": {"x": 1.2, "y": 1.4, "z": 1.0}
            }
        })
        print(f"  ✓ Placed {merlon_name} capping portal roof")
    except Exception as e:
        print("Merlon notice:", e)

def setup_curzon_promenade_plaza():
    print("\n=== 2. ADDING PROMENADE SEATING, COLONIAL LAMPS & HEDGE GARDENS ===")
    
    # Benches: 4 pairs on Left and Right sides of central promenade
    bench_coords = [
        # Left side (facing +Y towards central walkway)
        (-3850, -260, 10, 90.0),
        (-3450, -260, 10, 90.0),
        (-3050, -260, 10, 90.0),
        (-2700, -260, 10, 90.0),
        # Right side (facing -Y towards central walkway)
        (-3850, 260, 10, -90.0),
        (-3450, 260, 10, -90.0),
        (-3050, 260, 10, -90.0),
        (-2700, 260, 10, -90.0),
    ]
    for idx, (x, y, z, yaw) in enumerate(bench_coords):
        bname = f"Curzon_Plaza_Bench_{idx+1:02d}"
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": BENCH_MESH,
                "name": bname,
                "xform": {
                    "location": {"x": float(x), "y": float(y), "z": float(z)},
                    "rotation": {"pitch": 0.0, "yaw": float(yaw), "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
                }
            })
            print(f"  ✓ Spawned {bname} at ({x}, {y})")
        except Exception as e:
            print(f"Bench {bname}:", e)

    # Street Lamps: 4 pairs along promenade
    lamp_coords = [
        (-4050, -270, 10, 0.0),
        (-3650, -270, 10, 0.0),
        (-3250, -270, 10, 0.0),
        (-2850, -270, 10, 0.0),
        (-4050, 270, 10, 0.0),
        (-3650, 270, 10, 0.0),
        (-3250, 270, 10, 0.0),
        (-2850, 270, 10, 0.0),
    ]
    for idx, (x, y, z, yaw) in enumerate(lamp_coords):
        lname = f"Curzon_Plaza_ColonialLamp_{idx+1:02d}"
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": LAMP_MESH,
                "name": lname,
                "xform": {
                    "location": {"x": float(x), "y": float(y), "z": float(z)},
                    "rotation": {"pitch": 0.0, "yaw": float(yaw), "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
                }
            })
            print(f"  ✓ Spawned {lname} at ({x}, {y})")
        except Exception as e:
            print(f"Lamp {lname}:", e)

    # Manicured Hedges lining the promenade gardens
    hedge_coords = [
        (-4100, -360, 5, 0.0, 2.0),
        (-3700, -360, 5, 0.0, 2.0),
        (-3300, -360, 5, 0.0, 2.0),
        (-2900, -360, 5, 0.0, 2.0),
        (-4100, 360, 5, 0.0, 2.0),
        (-3700, 360, 5, 0.0, 2.0),
        (-3300, 360, 5, 0.0, 2.0),
        (-2900, 360, 5, 0.0, 2.0),
    ]
    for idx, (x, y, z, yaw, sx) in enumerate(hedge_coords):
        hname = f"Curzon_Plaza_GardenHedge_{idx+1:02d}"
        try:
            invoke_tool("add_to_scene_from_asset", "editor_toolset.toolsets.scene.SceneTools", {
                "asset_path": HEDGE_MESH,
                "name": hname,
                "xform": {
                    "location": {"x": float(x), "y": float(y), "z": float(z)},
                    "rotation": {"pitch": 0.0, "yaw": float(yaw), "roll": 0.0},
                    "scale": {"x": float(sx), "y": 1.0, "z": 1.0}
                }
            })
            print(f"  ✓ Spawned {hname} at ({x}, {y})")
        except Exception as e:
            print(f"Hedge {hname}:", e)

if __name__ == "__main__":
    setup_curzon_gate_and_portal()
    setup_curzon_promenade_plaza()
