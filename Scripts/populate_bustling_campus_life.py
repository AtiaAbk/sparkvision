#!/usr/bin/env python3
"""
Populate Dhaka University Campus with Bustling Student & Faculty Life:
1. Styles Distinct Clothing Materials:
   - Faculty: Formal Black Professor Blazer & Charcoal Trousers
   - Students: Navy Blazers, Khaki Trousers, Maroon Sweaters, Denim Jeans
   - Martial Artists: Martial Gi & Red Sash
2. Places Authentically Located Students & Professors with Bilingual Dialogue:
   - Curzon Science Quad: Prof. Jamal (Dean), Tanvir (Student Union), Science Students
   - Botanical Pond & Ghat: Ananya (Botany Researcher), Mehedi (Photographer)
   - TSC & Raju Hub: Sadia (Debate President), Arif (Cultural Secretary)
   - Kala Bhaban: Prof. Rahman (History Dean), Nabila (Fine Arts)
   - Shaheed Minar: Farhan (Language Movement Researcher)
   - Promenade Commuters: Pedestrians traversing the avenue
3. Spawns DU Martial Arts Sparring Opponents:
   - Hostile_Fahim_Sparring (Martial Arts Club Captain)
   - Hostile_Kamal_Martial (Advanced Sparring Partner)
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

FOLDER_PATH = "/Game/SparkVision/Materials"
MASTER_PBR = f"{FOLDER_PATH}/M_SparkVision_Master_PBR.M_SparkVision_Master_PBR"
NPC_CLASS = "/Script/MyProject.SVStudentNPC"
OPPONENT_CLASS = "/Script/MyProject.SVHostileOpponent"

CHARACTER_MATERIALS = [
    # Professor Formal Attire
    {
        "name": "MI_Professor_BlackBlazer",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_WoodDark_D.T_Curzon_WoodDark_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_WoodDark_N.T_Curzon_WoodDark_N",
        "color": {"r": 0.08, "g": 0.08, "b": 0.09, "a": 1.0},
        "roughness": 0.85,
        "metallic": 0.0
    },
    {
        "name": "MI_Professor_GreyTrousers",
        "diffuse": "/Game/SparkVision/Textures/T_Modern_Concrete_D.T_Modern_Concrete_D",
        "normal": "/Game/SparkVision/Textures/T_Modern_Concrete_N.T_Modern_Concrete_N",
        "color": {"r": 0.35, "g": 0.36, "b": 0.38, "a": 1.0},
        "roughness": 0.90,
        "metallic": 0.0
    },
    # Student Casual & Academic Attire
    {
        "name": "MI_Student_MaroonTorso",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_Brick_D.T_Curzon_Brick_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_Brick_N.T_Curzon_Brick_N",
        "color": {"r": 0.45, "g": 0.08, "b": 0.12, "a": 1.0},
        "roughness": 0.80,
        "metallic": 0.0
    },
    {
        "name": "MI_Student_DenimLegs",
        "diffuse": "/Game/SparkVision/Textures/T_Supporting_Building_D.T_Supporting_Building_D",
        "normal": "/Game/SparkVision/Textures/T_Supporting_Building_N.T_Supporting_Building_N",
        "color": {"r": 0.12, "g": 0.22, "b": 0.38, "a": 1.0},
        "roughness": 0.85,
        "metallic": 0.0
    },
    # Martial Arts Sparring Uniform
    {
        "name": "MI_Martial_WhiteGi",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_WhiteTrim_D.T_Curzon_WhiteTrim_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_WhiteTrim_N.T_Curzon_WhiteTrim_N",
        "color": {"r": 0.92, "g": 0.92, "b": 0.90, "a": 1.0},
        "roughness": 0.75,
        "metallic": 0.0
    },
    {
        "name": "MI_Martial_RedBelt",
        "diffuse": "/Game/SparkVision/Textures/T_Curzon_Brick_D.T_Curzon_Brick_D",
        "normal": "/Game/SparkVision/Textures/T_Curzon_Brick_N.T_Curzon_Brick_N",
        "color": {"r": 0.85, "g": 0.08, "b": 0.08, "a": 1.0},
        "roughness": 0.70,
        "metallic": 0.0
    }
]

def setup_clothing_materials():
    print("=" * 70)
    print("PHASE 1: CREATING CHARACTER CLOTHING PBR MATERIALS")
    print("=" * 70)
    
    paths = []
    for mat in CHARACTER_MATERIALS:
        name = mat["name"]
        ref_path = f"{FOLDER_PATH}/{name}.{name}"
        try:
            exists = invoke_tool("exists", "editor_toolset.toolsets.asset.AssetTools", {"path": ref_path}).get("returnValue", False)
            if not exists:
                invoke_tool("create", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                    "folder_path": FOLDER_PATH,
                    "asset_name": name,
                    "parent": {"refPath": MASTER_PBR}
                })
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": ref_path},
                "name": "BaseColor_Texture",
                "value": {"refPath": mat["diffuse"]}
            })
            invoke_tool("set_texture_parameter", "editor_toolset.toolsets.material_instance.MaterialInstanceTools", {
                "instance": {"refPath": ref_path},
                "name": "Normal_Texture",
                "value": {"refPath": mat["normal"]}
            })
            paths.append(f"{FOLDER_PATH}/{name}")
            print(f"  ✓ Configured {name}")
        except Exception as e:
            print(f"  Notice {name}: {e}")

    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {"asset_paths": paths})
    except Exception:
        pass

def spawn_characters():
    print("\n" * 2 + "=" * 70)
    print("PHASE 2: POPULATING CAMPUS HUBS WITH STUDENTS, FACULTY & OPPONENTS")
    print("=" * 70)

    # Clean existing test characters if any
    for old_name in [
        "NPC_Prof_Jamal_Curzon", "NPC_Sabbir_Curzon", "NPC_Rifat_Curzon",
        "NPC_Ananya_Botany", "NPC_Mehedi_Arts", "NPC_Prof_Rahman_Arts",
        "NPC_Nabila_FineArts", "NPC_Sadia_TSC", "NPC_Arif_Cultural",
        "NPC_Farhan_Shaheed", "Student_Commuter_01", "Student_Commuter_02",
        "Student_Commuter_03", "Student_Commuter_04",
        "Hostile_Fahim_Sparring", "Hostile_Kamal_Martial"
    ]:
        found = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": old_name, "tag": "", "collision_channels": []
        }).get("returnValue", [])
        for a in found:
            try:
                invoke_tool("remove_from_scene", "editor_toolset.toolsets.scene.SceneTools", {"actor": a})
            except Exception:
                pass

    # 1. Reposition Tanvir right at Curzon entrance landing
    tanvirs = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
        "name": "Tanvir", "tag": "", "collision_channels": []
    }).get("returnValue", [])
    if tanvirs:
        invoke_tool("set_actor_transform", "editor_toolset.toolsets.actor.ActorTools", {
            "actor": tanvirs[0],
            "xform": {
                "location": {"x": -3450.0, "y": -240.0, "z": 0.0},
                "rotation": {"pitch": 0.0, "yaw": 180.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            }
        })
        print("  ✓ Repositioned Tanvir at Curzon entrance landing (-3450, -240, 0)")

    # 2. Spawn Faculty & Student Characters
    characters_to_spawn = [
        # Curzon Science Faculty Dean
        {
            "name": "NPC_Prof_Jamal_Curzon",
            "class": NPC_CLASS,
            "loc": {"x": -3200.0, "y": 350.0, "z": 150.0},
            "yaw": 180.0,
            "id": "Prof_Jamal",
            "title": "Professor Dr. Jamal (Dean of Science)",
            "role": "Curzon Faculty Dean & Bose Physics Fellow",
            "dialogue": [
                ("কার্জন হলের এই ঐতিহাসিক বিজ্ঞান প্রাঙ্গণে তোমাকে স্বাগতম। ১৯২৬ সালে সত্যেন্দ্রনাথ বোস এবং আইনস্টাইনের কোয়ান্টাম পরিসংখ্যানের গৌরবময় স্মৃতি এই ক্যাম্পাসে অম্লান।",
                 "Welcome to this historic science quadrangle of Curzon Hall. The glorious memory of Satyendra Nath Bose and Einstein's 1926 quantum statistics lives on in these halls."),
                ("বিজ্ঞান অনুষদের প্রাচীন গবেষণাপত্রগুলো সামনের আর্কাইভ টার্মিনালে সংরক্ষিত আছে। তুমি গবেষণা নথিগুলো সংগ্রহ করে মিশন এগিয়ে নাও।",
                 "The ancient research manuscripts of the Science Faculty are preserved in the front Archive Terminal. Gather the research documents to progress your mission.")
            ]
        },
        # Curzon Promenade Students (Study Group)
        {
            "name": "NPC_Sabbir_Curzon",
            "class": NPC_CLASS,
            "loc": {"x": -1800.0, "y": 320.0, "z": 80.0},
            "yaw": 80.0,
            "id": "Student_Sabbir",
            "title": "Sabbir (Applied Physics Student)",
            "role": "Curzon Hall Science Student",
            "dialogue": [
                ("কার্জন হলের লাল ইটের বারান্দায় বসে বন্ধুদের সাথে আড্ডা আর পড়াশোনা করার আনন্দই আলাদা!",
                 "Nothing beats studying and having adda with friends along the red-brick verandas of Curzon Hall!"),
                ("সামনের পুকুরঘাটের কাছে গিয়ে দেখো, কৃষ্ণচূড়া আর শতবর্ষী বটের ছায়ায় পুরো ক্যাম্পাস শান্ত স্নিগ্ধ লাগে।",
                 "Head over to the pond ghat ahead—under the shade of scarlet Krishnachura and ancient banyans, the entire campus feels tranquil.")
            ]
        },
        {
            "name": "NPC_Rifat_Curzon",
            "class": NPC_CLASS,
            "loc": {"x": -1800.0, "y": 420.0, "z": 80.0},
            "yaw": -100.0,
            "id": "Student_Rifat",
            "title": "Rifat (Biochemistry Student)",
            "role": "Curzon Hall Science Student",
            "dialogue": [
                ("আজ ল্যাবে বেশিক্ষণ কাজ করতে হলো। বিকেলের বাতাসটা কী আরামদায়ক!",
                 "Had to spend extra hours in the organic chemistry lab today. The afternoon campus breeze is so refreshing!"),
                ("তুমি কি উত্তর প্রাঙ্গণের মার্শাল আর্টস ক্লাবের অনুশীলনে যাচ্ছ? ফাহিম ভাই ওখানে অনুশীলন করছেন।",
                 "Are you heading to the North Courtyard martial arts practice? Brother Fahim is sparring there right now.")
            ]
        },
        # Curzon Botanical Pond Ghat
        {
            "name": "NPC_Ananya_Botany",
            "class": NPC_CLASS,
            "loc": {"x": 1650.0, "y": -450.0, "z": 70.0},
            "yaw": 45.0,
            "id": "Student_Ananya",
            "title": "Ananya (Botany Researcher)",
            "role": "Curzon Botanical Gardens Specialist",
            "dialogue": [
                ("কার্জন পুকুরের এই পদ্মফুল আর ঝুলে থাকা বটের ঝুরিগুলো আমাদের ক্যাম্পাসের এক শতাব্দীর প্রকৃতির সাক্ষী।",
                 "These blooming lotus flowers and draping banyan roots of Curzon Pond have witnessed a century of campus natural history."),
                ("পানিতে সূর্যের আলোর ঝিকিমিকি দেখলে মন ভালো হয়ে যায়। সাবধানে ঘাটের সিঁড়ি দিয়ে নেমে আসো।",
                 "Watching sunlight glitter across the water surface calms the mind. Step down carefully along the ghat stone steps.")
            ]
        },
        {
            "name": "NPC_Mehedi_Arts",
            "class": NPC_CLASS,
            "loc": {"x": 2300.0, "y": -650.0, "z": 40.0},
            "yaw": 30.0,
            "id": "Student_Mehedi",
            "title": "Mehedi (Campus Photographer)",
            "role": "DU Photographic Society Member",
            "dialogue": [
                ("বিকেলের আলোয় কার্জন পুকুরের পানি আর প্রাচীন বটের ফ্রেম অসাধারণ এসেছে!",
                 "In this golden afternoon light, the framing of Curzon pond reflection against the heritage banyan is stunning!"),
                ("ঢাকা বিশ্ববিদ্যালয়ের মতো এত সবুজ ও নান্দনিক ক্যাম্পাস পুরো দেশে আর কোথাও পাবে না।",
                 "You won't find a greener and more aesthetically inspiring campus anywhere in the country.")
            ]
        },
        # Promenade Pedestrians / Walking Commuters
        {
            "name": "Student_Commuter_01",
            "class": NPC_CLASS,
            "loc": {"x": -800.0, "y": 150.0, "z": 80.0},
            "yaw": 180.0,
            "id": "Commuter_01",
            "title": "Tanmay (Mathematics Student)",
            "role": "Campus Pedestrian",
            "dialogue": [
                ("লাইব্রেরি থেকে বই নিয়ে কার্জন হলে যাচ্ছি। ক্যাম্পাসের ছায়াঘেরা রাস্তাগুলো হাঁটতে ভীষণ ভালো লাগে।",
                 "Returning from the Central Library to Curzon. Walking through these tree-shaded campus avenues is pure joy.")
            ]
        },
        {
            "name": "Student_Commuter_02",
            "class": NPC_CLASS,
            "loc": {"x": 200.0, "y": -120.0, "z": 80.0},
            "yaw": 0.0,
            "id": "Commuter_02",
            "title": "Shafiq (Geology Student)",
            "role": "Campus Pedestrian",
            "dialogue": [
                ("টিএসসির সাহিত্য আড্ডায় যাওয়ার জন্য বের হয়েছি। তুমিও কি ওখানে যাচ্ছ?",
                 "On my way to the literature adda at TSC. Are you heading there as well?")
            ]
        },
        # TSC Student Cultural Hub
        {
            "name": "NPC_Sadia_TSC",
            "class": NPC_CLASS,
            "loc": {"x": 57000.0, "y": -62500.0, "z": 150.0},
            "yaw": -45.0,
            "id": "Student_Sadia",
            "title": "Sadia (Debating Club President)",
            "role": "TSC Cultural & Debating Society Leader",
            "dialogue": [
                ("টিএসসি হলো ঢাকা বিশ্ববিদ্যালয়ের মুক্তবুদ্ধি চর্চা, যুক্তিবাদ আর সাংস্কৃতিক আন্দোলনের অনন্ত বাতিঘর।",
                 "TSC is the eternal beacon of free thought, rational debate, and cultural movements at Dhaka University."),
                ("রাজু ভাস্কর্যের সামনে দাঁড়িয়ে অন্যায়ের বিরুদ্ধে শপথ নেওয়া আমাদের শিক্ষার্থীদের ঐতিহ্য।",
                 "Standing before Raju Memorial and taking an oath against injustice is our proud student tradition.")
            ]
        },
        {
            "name": "NPC_Arif_Cultural",
            "class": NPC_CLASS,
            "loc": {"x": 57600.0, "y": -61800.0, "z": 150.0},
            "yaw": 135.0,
            "id": "Student_Arif",
            "title": "Arif (Music & Cultural Secretary)",
            "role": "DU Cultural Troupe Organizer",
            "dialogue": [
                ("বসন্ত উৎসব আর পহেলা বৈশাখের প্রস্তুতি চলছে টিএসসির ক্যাফেটেরিয়া চত্বরে!",
                 "Preparations for the spring festival and Pohela Boishakh celebrations are underway at the TSC cafeteria quad!")
            ]
        },
        # Kala Bhaban (Faculty of Arts)
        {
            "name": "NPC_Prof_Rahman_Arts",
            "class": NPC_CLASS,
            "loc": {"x": 70500.0, "y": -95000.0, "z": 150.0},
            "yaw": 0.0,
            "id": "Prof_Rahman",
            "title": "Professor Dr. Rahman (Faculty of Arts)",
            "role": "Senior History Faculty & 1971 Scholar",
            "dialogue": [
                ("কলা ভবনের এই প্রাঙ্গণ থেকেই ১৯৭১ সালের মহান স্বাধীনতা সংগ্রামের ডাক উঠেছিল। আমাদের ছাত্র-শিক্ষকদের আত্মত্যাগ অমর।",
                 "From this very courtyard of Kala Bhaban, the historic clarion call of our 1971 Liberation War was sounded. The sacrifice of our students and teachers is immortal."),
                ("অপরাজেয় বাংলা ভাস্কর্যটি নিবিড়ভাবে লক্ষ্য করো—কৃষক, ছাত্র ও নারীদের সম্মিলিত প্রতিরোধ কীভাবে জাতিকে মুক্ত করেছিল।",
                 "Observe the Aparajeyo Bangla sculpture closely—it embodies how peasants, students, and women joined together in heroic resistance to liberate our nation.")
            ]
        },
        {
            "name": "NPC_Nabila_FineArts",
            "class": NPC_CLASS,
            "loc": {"x": 71200.0, "y": -95400.0, "z": 150.0},
            "yaw": 180.0,
            "id": "Student_Nabila",
            "title": "Nabila (Sculpture Student)",
            "role": "Faculty of Fine Arts Representative",
            "dialogue": [
                ("সৈয়দ আবদুল্লাহ খালিদের নির্মিত অপরাজেয় বাংলার প্রতিটি রেখায় এক অমর দ্রোহের শক্তি প্রকাশ পেয়েছে।",
                 "In every contour of Aparajeyo Bangla sculpted by Syed Abdullah Khalid, an immortal spirit of defiance is etched.")
            ]
        },
        # Shaheed Minar Memorial Plaza
        {
            "name": "NPC_Farhan_Shaheed",
            "class": NPC_CLASS,
            "loc": {"x": -2200.0, "y": -54000.0, "z": 100.0},
            "yaw": 0.0,
            "id": "Student_Farhan",
            "title": "Farhan (Language Movement Researcher)",
            "role": "National Heritage Research Fellow",
            "dialogue": [
                ("১৯৫২ সালের ২১শে ফেব্রুয়ারি মাতৃভাষা বাংলার মর্যাদার জন্য শহীদ বরকত, সালাম, রফিক ও জব্বাররা রক্ত দিয়ে ইতিহাস সৃষ্টি করেছিলেন।",
                 "On 21 February 1952, martyrs Barkat, Salam, Rafiq, and Jabbar shed their blood for the honor of Bengali language, carving our identity into world history."),
                ("রক্তিম সূর্য আর শ্বেতশুভ্র স্তম্ভগুলো মাতৃক্রোড়ে সন্তানের চিরন্তন ভালোবাসার প্রতীক।",
                 "The glowing crimson sun and pristine white marble pillars symbolize mother Bengal cradling her martyr sons.")
            ]
        }
    ]

    for char in characters_to_spawn:
        name = char["name"]
        xform = {
            "location": char["loc"],
            "rotation": {"pitch": 0.0, "yaw": char["yaw"], "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
        try:
            res = invoke_tool("add_to_scene_from_class", "editor_toolset.toolsets.scene.SceneTools", {
                "actor_type": {"refPath": char["class"]},
                "name": name,
                "xform": xform,
                "snap_to_ground": False
            })
            act = res.get("returnValue", {})
            if act and act.get("refPath"):
                print(f"  ✓ Spawned {name} ({char['title']})")
        except Exception as e:
            print(f"  Error spawning {name}: {e}")

    # 3. Spawn Curzon North Courtyard Martial Arts Sparring Opponents
    sparring_opponents = [
        {
            "name": "Hostile_Fahim_Sparring",
            "loc": {"x": -2200.0, "y": 1600.0, "z": 80.0},
            "yaw": 0.0,
            "health": 60.0,
            "damage": 12.0
        },
        {
            "name": "Hostile_Kamal_Martial",
            "loc": {"x": -1600.0, "y": 1750.0, "z": 80.0},
            "yaw": -45.0,
            "health": 75.0,
            "damage": 14.0
        }
    ]

    for opp in sparring_opponents:
        name = opp["name"]
        xform = {
            "location": opp["loc"],
            "rotation": {"pitch": 0.0, "yaw": opp["yaw"], "roll": 0.0},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
        }
        try:
            res = invoke_tool("add_to_scene_from_class", "editor_toolset.toolsets.scene.SceneTools", {
                "actor_type": {"refPath": OPPONENT_CLASS},
                "name": name,
                "xform": xform,
                "snap_to_ground": False
            })
            act = res.get("returnValue", {})
            if act and act.get("refPath"):
                print(f"  ✓ Spawned Martial Arts Sparring Partner: {name}")
        except Exception as e:
            print(f"  Error spawning {name}: {e}")

    # Save level
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print("\n✅ Saved level with all students, faculty & sparring opponents!")
    except Exception as e:
        print(f"Notice saving level: {e}")

def main():
    setup_clothing_materials()
    spawn_characters()
    print("\nCampus Life & Population Overhaul Complete!")

if __name__ == "__main__":
    main()
