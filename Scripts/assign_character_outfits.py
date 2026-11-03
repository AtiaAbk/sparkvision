#!/usr/bin/env python3
"""
Assign Authentic Outfits, Titles, Roles & Material Instances to Campus Characters
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

MAT_DIR = "/Game/SparkVision/Materials"
MANNY_MAT_DIR = "/Game/Characters/Mannequins/Materials/Manny"

OUTFIT_CONFIGS = {
    # Professors - Formal Black Blazer & Grey Trousers
    "Prof_Jamal": {
        "materials": [f"{MAT_DIR}/MI_Professor_GreyTrousers.MI_Professor_GreyTrousers", f"{MAT_DIR}/MI_Professor_BlackBlazer.MI_Professor_BlackBlazer"],
        "name": "Professor Dr. Jamal (Dean of Science)",
        "role": "Curzon Faculty Dean & Bose Physics Fellow",
        "id": "Prof_Jamal"
    },
    "Prof_Rahman": {
        "materials": [f"{MAT_DIR}/MI_Professor_GreyTrousers.MI_Professor_GreyTrousers", f"{MAT_DIR}/MI_Professor_BlackBlazer.MI_Professor_BlackBlazer"],
        "name": "Professor Dr. Rahman (Faculty of Arts)",
        "role": "Senior History Faculty & 1971 Scholar",
        "id": "Prof_Rahman"
    },
    # Students - Maroon Sweaters & Denim Jeans
    "Sabbir": {
        "materials": [f"{MAT_DIR}/MI_Student_DenimLegs.MI_Student_DenimLegs", f"{MAT_DIR}/MI_Student_MaroonTorso.MI_Student_MaroonTorso"],
        "name": "Sabbir (Applied Physics Student)",
        "role": "Curzon Hall Science Student",
        "id": "Student_Sabbir"
    },
    "Ananya": {
        "materials": [f"{MAT_DIR}/MI_Student_DenimLegs.MI_Student_DenimLegs", f"{MAT_DIR}/MI_Student_MaroonTorso.MI_Student_MaroonTorso"],
        "name": "Ananya (Botany Researcher)",
        "role": "Curzon Botanical Gardens Specialist",
        "id": "Student_Ananya"
    },
    "Sadia": {
        "materials": [f"{MAT_DIR}/MI_Student_DenimLegs.MI_Student_DenimLegs", f"{MAT_DIR}/MI_Student_MaroonTorso.MI_Student_MaroonTorso"],
        "name": "Sadia (Debating Club President)",
        "role": "TSC Cultural & Debating Society Leader",
        "id": "Student_Sadia"
    },
    "Commuter_01": {
        "materials": [f"{MAT_DIR}/MI_Student_DenimLegs.MI_Student_DenimLegs", f"{MAT_DIR}/MI_Student_MaroonTorso.MI_Student_MaroonTorso"],
        "name": "Tanmay (Mathematics Student)",
        "role": "Campus Pedestrian",
        "id": "Commuter_01"
    },
    # Students - Navy Blazers & Khaki Trousers
    "Tanvir": {
        "materials": [f"{MANNY_MAT_DIR}/MI_Student_KhakiLegs.MI_Student_KhakiLegs", f"{MANNY_MAT_DIR}/MI_Student_NavyTorso.MI_Student_NavyTorso"],
        "name": "Tanvir (Student Organizer)",
        "role": "Curzon Science Faculty Representative",
        "id": "NPC_Tanvir"
    },
    "Rifat": {
        "materials": [f"{MANNY_MAT_DIR}/MI_Student_KhakiLegs.MI_Student_KhakiLegs", f"{MANNY_MAT_DIR}/MI_Student_NavyTorso.MI_Student_NavyTorso"],
        "name": "Rifat (Biochemistry Student)",
        "role": "Curzon Hall Science Student",
        "id": "Student_Rifat"
    },
    "Mehedi": {
        "materials": [f"{MANNY_MAT_DIR}/MI_Student_KhakiLegs.MI_Student_KhakiLegs", f"{MANNY_MAT_DIR}/MI_Student_NavyTorso.MI_Student_NavyTorso"],
        "name": "Mehedi (Campus Photographer)",
        "role": "DU Photographic Society Member",
        "id": "Student_Mehedi"
    },
    "Commuter_02": {
        "materials": [f"{MANNY_MAT_DIR}/MI_Student_KhakiLegs.MI_Student_KhakiLegs", f"{MANNY_MAT_DIR}/MI_Student_NavyTorso.MI_Student_NavyTorso"],
        "name": "Shafiq (Geology Student)",
        "role": "Campus Pedestrian",
        "id": "Commuter_02"
    },
    "Arif": {
        "materials": [f"{MANNY_MAT_DIR}/MI_Student_KhakiLegs.MI_Student_KhakiLegs", f"{MANNY_MAT_DIR}/MI_Student_NavyTorso.MI_Student_NavyTorso"],
        "name": "Arif (Music & Cultural Secretary)",
        "role": "DU Cultural Troupe Organizer",
        "id": "Student_Arif"
    },
    "Nabila": {
        "materials": [f"{MAT_DIR}/MI_Student_DenimLegs.MI_Student_DenimLegs", f"{MAT_DIR}/MI_Student_MaroonTorso.MI_Student_MaroonTorso"],
        "name": "Nabila (Sculpture Student)",
        "role": "Faculty of Fine Arts Representative",
        "id": "Student_Nabila"
    },
    "Farhan": {
        "materials": [f"{MANNY_MAT_DIR}/MI_Student_KhakiLegs.MI_Student_KhakiLegs", f"{MANNY_MAT_DIR}/MI_Student_NavyTorso.MI_Student_NavyTorso"],
        "name": "Farhan (Language Movement Researcher)",
        "role": "National Heritage Research Fellow",
        "id": "Student_Farhan"
    },
    # Martial Arts Sparring Opponents
    "Fahim": {
        "materials": [f"{MAT_DIR}/MI_Martial_WhiteGi.MI_Martial_WhiteGi", f"{MAT_DIR}/MI_Martial_RedBelt.MI_Martial_RedBelt"],
        "name": "Fahim (Martial Arts Club Captain)",
        "role": "Curzon Sparring Partner",
        "id": "Opponent_Fahim"
    },
    "Kamal": {
        "materials": [f"{MAT_DIR}/MI_Martial_WhiteGi.MI_Martial_WhiteGi", f"{MAT_DIR}/MI_Martial_RedBelt.MI_Martial_RedBelt"],
        "name": "Kamal (Advanced Sparring Partner)",
        "role": "DU Martial Arts Contender",
        "id": "Opponent_Kamal"
    }
}

def main():
    print("=" * 70)
    print("ASSIGNING CHARACTER OUTFITS AND TITLES")
    print("=" * 70)

    all_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "", "tag": "", "collision_channels": []
    }).get("returnValue", [])

    updated = 0
    for a in all_actors:
        lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
        if not lbl:
            continue

        matched_key = None
        for key in OUTFIT_CONFIGS:
            if key.lower() in lbl.lower():
                matched_key = key
                break

        if matched_key:
            cfg = OUTFIT_CONFIGS[matched_key]
            # Set properties on actor
            try:
                invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                    "instance": a,
                    "values": json.dumps({
                        "NPCId": cfg["id"],
                        "NPCName": cfg["name"],
                        "NPCRole": cfg["role"]
                    })
                })
            except Exception:
                pass

            # Set clothing override materials on Mesh
            comps = invoke_tool("get_components", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", [])
            for c in comps:
                c_ref = c.get("refPath", "")
                if "Mesh" in c_ref or "CharacterMesh0" in c_ref:
                    override_list = [{"refPath": m} for m in cfg["materials"]]
                    try:
                        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                            "instance": c,
                            "values": json.dumps({"OverrideMaterials": override_list})
                        })
                        print(f"  ✓ Styled {lbl} -> {cfg['name']} ({len(cfg['materials'])} clothing materials)")
                        updated += 1
                    except Exception as e:
                        print(f"  Notice styling {lbl}: {e}")

    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print(f"\n✅ Successfully styled {updated} characters and saved level!")
    except Exception as e:
        print(f"Notice saving: {e}")

if __name__ == "__main__":
    main()
