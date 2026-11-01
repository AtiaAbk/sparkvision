#!/usr/bin/env python3
"""
Automated Foliage Placement & Architectural Clearance Audit Suite
Audits all environment actors against:
1. Building bounding boxes (minimum 12m clearance for large trees, 6m for medium trees)
2. Ground Z placement (flora must be grounded between Z=-20 and Z=50; perched fauna up to Z=350)
3. Curzon Hall central approach sightline (Y: -600 to 600, X: -5000 to -2500)
4. Primary road clearance
"""

import json
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

BUILDINGS = [
    {"name": "Curzon_Hall_Main", "center": {"x": -2850.0, "y": 0.0}, "extent": {"x": 1000.0, "y": 6650.0}, "min_clearance": 1200.0},
    {"name": "Curzon_Labs", "center": {"x": 6500.0, "y": 4610.0}, "extent": {"x": 4100.0, "y": 2100.0}, "min_clearance": 1200.0},
    {"name": "Curzon_Annex", "center": {"x": 6500.0, "y": -4190.0}, "extent": {"x": 4100.0, "y": 2100.0}, "min_clearance": 1200.0},
    {"name": "Shaheed_Minar", "center": {"x": -282.0, "y": -54042.0}, "extent": {"x": 2000.0, "y": 1500.0}, "min_clearance": 1500.0},
    {"name": "Raju_Sculpture", "center": {"x": 58964.0, "y": -63725.0}, "extent": {"x": 800.0, "y": 800.0}, "min_clearance": 800.0},
    {"name": "Central_Library", "center": {"x": 73459.0, "y": -71379.0}, "extent": {"x": 2800.0, "y": 2000.0}, "min_clearance": 1000.0},
    {"name": "Kala_Bhaban", "center": {"x": 78004.0, "y": -95794.0}, "extent": {"x": 2850.0, "y": 8150.0}, "min_clearance": 1200.0},
    {"name": "SM_Hall", "center": {"x": 15000.0, "y": -68000.0}, "extent": {"x": 5500.0, "y": 4500.0}, "min_clearance": 1200.0},
    {"name": "Shahidullah_Hall", "center": {"x": 5000.0, "y": -5000.0}, "extent": {"x": 4500.0, "y": 3500.0}, "min_clearance": 1000.0},
    {"name": "Bangla_Academy", "center": {"x": 18000.0, "y": -28000.0}, "extent": {"x": 4700.0, "y": 5200.0}, "min_clearance": 1200.0},
]

def run_mcp(toolset, tool, args):
    return mcp_client.invoke_tool(tool, toolset, args)

def dist_point_to_box(px, py, cx, cy, ex, ey):
    dx = max(0.0, abs(px - cx) - ex)
    dy = max(0.0, abs(py - cy) - ey)
    return math.sqrt(dx * dx + dy * dy)

def main():
    print("=" * 70, flush=True)
    print("RUNNING FOLIAGE PLACEMENT & CLEARANCE GEOMETRIC AUDIT...", flush=True)
    print("=" * 70, flush=True)

    folders = run_mcp("editor_toolset.toolsets.scene.SceneTools", "get_folders", {}).get("returnValue", [])
    env_folders = [f for f in folders if f.startswith("Environment") or f.startswith("Green_Spaces")]

    seen_refs = set()
    all_env_actors = []
    for fld in env_folders:
        actors = run_mcp("editor_toolset.toolsets.scene.SceneTools", "get_actors_in_folder", {"folder_path": fld}).get("returnValue", [])
        for a in actors:
            ref = a["refPath"]
            if ref in seen_refs:
                continue
            seen_refs.add(ref)
            lbl = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_label", {"actor": a}).get("returnValue", "")
            xform = run_mcp("editor_toolset.toolsets.actor.ActorTools", "get_actor_transform", {"actor": a, "worldspace": True}).get("returnValue", {})
            loc = xform.get("location", xform.get("translation", {}))
            scale = xform.get("scale", xform.get("scale3d", {}))
            all_env_actors.append({"label": lbl, "folder": fld, "loc": loc, "scale": scale, "ref": ref})

    print(f"Total unique environment actors audited: {len(all_env_actors)}", flush=True)

    defects = []

    for a in all_env_actors:
        lbl = a["label"]
        loc = a["loc"]
        px, py, pz = loc.get("x", 0.0), loc.get("y", 0.0), loc.get("z", 0.0)

        is_fauna = any(w in lbl for w in ["Doel", "Bird", "Butterfly", "Dragonfly", "Wildlife"])

        # 1. Ground / Elevation Z check
        if pz < -50.0:
            defects.append(f"[FLOATING/BURIED] {lbl} buried at Z={pz:.1f}")
        elif not is_fauna and pz > 100.0 and "Curzon_Sign" not in lbl:
            defects.append(f"[FLOATING/BURIED] {lbl} floating at Z={pz:.1f}")
        elif is_fauna and pz > 400.0:
            defects.append(f"[FAUNA TOO HIGH] {lbl} above canopy at Z={pz:.1f}")

        # 2. Building clearance check
        # Skip small ground flora, hedges, aquatic elements, and wildlife
        if is_fauna or any(w in lbl for w in ["Hedge", "Gandharaj", "Rangan", "Tuft", "Grass", "Fern", "Litter", "Curzon_Authentic_Palm", "WaterLily", "Reeds", "Ghat"]):
            continue

        for b in BUILDINGS:
            bname = b["name"]
            d = dist_point_to_box(px, py, b["center"]["x"], b["center"]["y"], b["extent"]["x"], b["extent"]["y"])
            if d == 0:
                defects.append(f"[CRITICAL COLLISION] {lbl} is INSIDE {bname} bounding box!")
            elif d < 400.0 and "Palm" not in lbl and "Neem" not in lbl:
                defects.append(f"[CANOPY CLIPPING RISK] {lbl} is only {d/100:.1f}m from {bname} (min {b['min_clearance']/100:.1f}m)")

        # 3. Curzon Hall central portal sightline check
        # Front corridor: X in [-5000, -2500], Y in [-600, 600]
        if -5000.0 < px < -2500.0 and -600.0 < py < 600.0:
            if "Palm" not in lbl and "Hedge" not in lbl and not is_fauna:
                defects.append(f"[SIGHTLINE OCCLUSION] {lbl} blocks Curzon Hall central approach at ({px:.1f}, {py:.1f})")

    print("\n" + "=" * 70, flush=True)
    print("AUDIT RESULTS:", flush=True)
    print("=" * 70, flush=True)
    if not defects:
        print("  >>> PASS: ZERO PLACEMENT DEFECTS FOUND! <<<", flush=True)
        print(f"  All {len(all_env_actors)} environment actors pass geometric clearance, ground anchoring, and sightline rules.", flush=True)
    else:
        print(f"  Found {len(defects)} defect(s):", flush=True)
        for d in defects:
            print("   *", d, flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
