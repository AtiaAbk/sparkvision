#!/usr/bin/env python3
"""
Apply Authentic Distinct Materials to Dhaka University & Modern City Skyline:
- Curzon Hall: Preserves authentic Indo-Saracenic terracotta red brick & white trims
- Kala Bhaban: Tropical Modernist / Brutalist sand-toned concrete louvers & tinted ribbon glazing
- TSC: Konstantinos Doxiadis crisp white structural waffle fascia, modern terracotta panels & green-tinted glass
- Shaheed Minar: Pure Carrara white marble, dark polished basalt/granite terrace, deep crimson lacquer sun
- Doyel Chattar: Iridescent teal/black/white magpie robin plumage & turquoise mosaic pool tiles
- Modern Skyline: Reflective sky blue curtain wall glass, brushed titanium aluminum, dark spandrels
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MAT_DIR = "/Game/SparkVision/Materials"

DISTINCT_BUILDING_CONFIGS = {
    # 0. Curzon Hall Indo-Saracenic Heritage - Arched colonial doors, cusped windows & terracotta brick
    "Curzon_Main": [
        f"{MAT_DIR}/MI_Curzon_Facade_ArchedDoorsWindows.MI_Curzon_Facade_ArchedDoorsWindows",
        f"{MAT_DIR}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
        f"{MAT_DIR}/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
    ],
    "Curzon_East": [
        f"{MAT_DIR}/MI_Curzon_Facade_ArchedDoorsWindows.MI_Curzon_Facade_ArchedDoorsWindows",
        f"{MAT_DIR}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    "Curzon_West": [
        f"{MAT_DIR}/MI_Curzon_Facade_ArchedDoorsWindows.MI_Curzon_Facade_ArchedDoorsWindows",
        f"{MAT_DIR}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    "Curzon_Wing": [
        f"{MAT_DIR}/MI_Curzon_Facade_ArchedDoorsWindows.MI_Curzon_Facade_ArchedDoorsWindows",
        f"{MAT_DIR}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    "Hero_Curzon": [
        f"{MAT_DIR}/MI_Curzon_Facade_ArchedDoorsWindows.MI_Curzon_Facade_ArchedDoorsWindows",
        f"{MAT_DIR}/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    ],
    # 1. Kala Bhaban (Faculty of Arts) - Tropical modernist facade with ribbon windows, concrete louvers & glass doors
    "ArtsFaculty_KalaBhaban_AcademicBlock": [
        f"{MAT_DIR}/MI_KalaBhaban_ModernistFacade.MI_KalaBhaban_ModernistFacade",
        f"{MAT_DIR}/MI_Modern_ConcreteFin.MI_Modern_ConcreteFin",
        f"{MAT_DIR}/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    "Hero_KalaBhaban": [
        f"{MAT_DIR}/MI_KalaBhaban_ModernistFacade.MI_KalaBhaban_ModernistFacade",
        f"{MAT_DIR}/MI_Modern_ConcreteFin.MI_Modern_ConcreteFin",
        f"{MAT_DIR}/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    # 2. Central Library - Modernist concrete fins & ribbon solar glazing
    "Hero_CentralLibrary_Building": [
        f"{MAT_DIR}/MI_KalaBhaban_ModernistFacade.MI_KalaBhaban_ModernistFacade",
        f"{MAT_DIR}/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ],
    # 3. TSC (Teacher-Student Centre) - Tropical modernist white waffle fascia, terracotta panels & entrance portals
    "Hero_TSC_AuditoriumComplex": [
        f"{MAT_DIR}/MI_TSC_ModernistFacade.MI_TSC_ModernistFacade",
        f"{MAT_DIR}/MI_Modern_TerracottaPanel.MI_Modern_TerracottaPanel",
        f"{MAT_DIR}/MI_Modern_Glass_GreenTint.MI_Modern_Glass_GreenTint",
    ],
    # 4. Central Shaheed Minar - Pure Carrara marble columns & dark polished basalt/granite terrace
    "Hero_ShaheedMinar_Monument": [
        f"{MAT_DIR}/MI_Shaheed_BlackGranite.MI_Shaheed_BlackGranite",
        f"{MAT_DIR}/MI_Shaheed_Marble_Pure.MI_Shaheed_Marble_Pure",
        f"{MAT_DIR}/MI_Shaheed_Sun.MI_Shaheed_Sun",
    ],
    # 5. Doyel Chattar Roundabout Monument - Sculpted national birds, lotus petals & turquoise pool
    "Hero_DoyelChattar_Monument": [
        f"{MAT_DIR}/MI_Pool_Mosaic_Turquoise.MI_Pool_Mosaic_Turquoise",
        f"{MAT_DIR}/MI_Fauna_Doel_Black.MI_Fauna_Doel_Black",
        f"{MAT_DIR}/MI_Fauna_Doel_White.MI_Fauna_Doel_White",
        f"{MAT_DIR}/MI_Fauna_Doel_Teal.MI_Fauna_Doel_Teal",
        f"{MAT_DIR}/MI_TSC_WhiteFascia.MI_TSC_WhiteFascia",
    ],
    # 6. Modern Skyline Glass Towers across Highway (Motijheel / Bijoy Nagar high-rises)
    "ModernTower_Glass": [
        f"{MAT_DIR}/MI_Modern_Glass_CurtainWall_Blue.MI_Modern_Glass_CurtainWall_Blue",
        f"{MAT_DIR}/MI_Modern_Alu_Titanium.MI_Modern_Alu_Titanium",
        f"{MAT_DIR}/MI_Modern_Spandrel_Dark.MI_Modern_Spandrel_Dark",
    ],
    # 7. Modern Commercial Skyline Buildings
    "ModernCommercial": [
        f"{MAT_DIR}/MI_Modern_Alu_Titanium.MI_Modern_Alu_Titanium",
        f"{MAT_DIR}/MI_Modern_Spandrel_Dark.MI_Modern_Spandrel_Dark",
        f"{MAT_DIR}/MI_Modern_Glass_CurtainWall_Blue.MI_Modern_Glass_CurtainWall_Blue",
    ],
    # 8. Modern Campus Skyline Mesh
    "SM_Campus_Skyline": [
        f"{MAT_DIR}/MI_Modern_Alu_Titanium.MI_Modern_Alu_Titanium",
        f"{MAT_DIR}/MI_Modern_Glass_CurtainWall_Blue.MI_Modern_Glass_CurtainWall_Blue",
        f"{MAT_DIR}/MI_Modern_Spandrel_Dark.MI_Modern_Spandrel_Dark",
    ],
    # 9. IBA Building (Institute of Business Administration)
    "Supporting_IBA_Building": [
        f"{MAT_DIR}/MI_Modern_ConcreteFin.MI_Modern_ConcreteFin",
        f"{MAT_DIR}/MI_Modern_Glass_GreenTint.MI_Modern_Glass_GreenTint",
        f"{MAT_DIR}/MI_Modern_Alu_Titanium.MI_Modern_Alu_Titanium",
    ],
    # 10. Admin / Registrar Building
    "Supporting_Admin_RegistrarBuilding": [
        f"{MAT_DIR}/MI_Modern_ConcreteFin.MI_Modern_ConcreteFin",
        f"{MAT_DIR}/MI_Modern_Concrete_Sand.MI_Modern_Concrete_Sand",
        f"{MAT_DIR}/MI_Modern_RibbonWindow.MI_Modern_RibbonWindow",
    ]
}

def apply_materials():
    print("=" * 70)
    print("APPLYING AUTHENTIC ARCHITECTURAL MATERIALS ACROSS ALL DISTRICTS")
    print("=" * 70)

    updated_count = 0

    # Query all scene actors
    all_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": []
    }).get("returnValue", [])

    print(f"Scanning {len(all_actors)} scene actors...")

    for a in all_actors:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
        if not lbl:
            continue

        matched_config = None
        for pattern, mats in DISTINCT_BUILDING_CONFIGS.items():
            if pattern.lower() in lbl.lower():
                matched_config = mats
                break

        if matched_config:
            comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
            for comp in comps:
                if "StaticMeshComponent" in comp.get("refPath", ""):
                    override_list = [{"refPath": m} for m in matched_config]
                    try:
                        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                            "instance": comp,
                            "values": json.dumps({"OverrideMaterials": override_list})
                        })
                        print(f"  ✓ [AUTHENTIC PBR] {lbl}: Applied {len(matched_config)} architectural materials")
                        updated_count += 1
                    except Exception as e:
                        print(f"  Notice updating {lbl}: {e}")

    # Save level
    try:
        invoke_tool("save_current_level", "editor_toolset.toolsets.scene.SceneTools", {})
        print("\n✅ Saved current level with authentic architectural materials!")
    except Exception as e:
        print(f"Notice saving level: {e}")

    print(f"\nCompleted! Upgraded {updated_count} architectural components.")

if __name__ == "__main__":
    apply_materials()
