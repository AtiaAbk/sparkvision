#!/usr/bin/env python3
"""
Apply authentic architectural materials, window glazing, and door trims
to all University of Dhaka hero and supporting campus buildings:
- Removes featureless flat grey overrides (MI_Supporting_Building, MI_Hero_Modern)
- Restores red brick, white jali/trim, dark wood doors, and glazed ribbon windows
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

BUILDING_MATERIAL_CONFIGS = {
    # 1. Arts Faculty (Kala Bhaban) - Red brick modernist academic block with ribbon windows
    "ArtsFaculty_KalaBhaban_AcademicBlock": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    # 2. Central Library - Brutalist/Modernist concrete sunshades (brise-soleil) and glazed windows
    "Hero_CentralLibrary_Building": [
        "/Game/SparkVision/Materials/MI_Modern_ConcreteFin.MI_Modern_ConcreteFin",
        "/Game/SparkVision/Materials/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    # 3. TSC (Teacher-Student Centre) - Tropical modernist white jali screens, brick, and glass doors
    "Hero_TSC_AuditoriumComplex": [
        "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Modern_GlassDoor.MI_Modern_GlassDoor",
    ],
    # 4. Dr. Shahidullah Hall - Heritage colonial red brick hall with white window trim
    "Hero_DrShahidullah_Hall": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    # 5. Rokeya Hall - Heritage red brick female hall
    "Hero_Rokeya_Hall": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    # 6. Jagannath Hall - Historic colonial red brick hall
    "Supporting_JagannathHallComplex": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    # 7. Surja Sen Hall - Modernist red brick student hall
    "Supporting_SurjaSenHallBlock": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    # 8. Haji Muhammad Mohsin Hall
    "Supporting_HajiMuhammadMohsinHall": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    # 9. Curzon Chemistry & Physics Labs
    "Supporting_CurzonChemistryPhysicsLabs": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    # 10. Curzon Physics Annex
    "Supporting_Curzon_PhysicsAnnex": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    # 11. IBA Building - Business administration building with concrete and tinted glass
    "Supporting_IBA_Building": [
        "/Game/SparkVision/Materials/MI_Modern_ConcreteFin.MI_Modern_ConcreteFin",
        "/Game/SparkVision/Materials/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    # 12. Registrar / Administrative Building
    "Supporting_Admin_RegistrarBuilding": [
        "/Game/SparkVision/Materials/MI_Curzon_StonePaving.MI_Curzon_StonePaving",
        "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
        "/Game/SparkVision/Materials/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ]
}

def main():
    print("=" * 70)
    print("APPLYING AUTHENTIC ARCHITECTURAL DOORS, WINDOWS & FACADES...")
    print("=" * 70)

    folders = [
        "Hero_Buildings",
        "Hero_Buildings/Arts_Faculty",
        "Hero_Buildings/Central_Library",
        "Hero_Buildings/Curzon_Hall",
        "Hero_Buildings/Student_Halls",
        "Hero_Buildings/TSC_Raju",
        "Supporting_Buildings/Academic",
        "Supporting_Buildings/Administrative",
    ]

    updated_count = 0

    for fld in folders:
        actors = mcp_client.invoke_tool("get_actors_in_folder", "editor_toolset.toolsets.scene.SceneTools", {"folder_path": fld}).get("returnValue", [])
        for a in actors:
            lbl = mcp_client.invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
            for bname, mats in BUILDING_MATERIAL_CONFIGS.items():
                if bname in lbl:
                    comps = mcp_client.invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
                    if comps:
                        comp = comps[0]
                        override_list = [{"refPath": m} for m in mats]
                        mcp_client.invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                            "instance": comp,
                            "values": json.dumps({"OverrideMaterials": override_list})
                        })
                        print(f"  [UPDATED] {lbl}: Applied {len(mats)} authentic architectural materials (brick, windows, doors)")
                        updated_count += 1

    print("\n" + "=" * 70)
    print(f"SUCCESS: Upgraded {updated_count} campus buildings with authentic doors, windows, and brick facades!")
    print("=" * 70)

if __name__ == "__main__":
    main()
