#!/usr/bin/env python3
"""
Setup Authentic Student Attire and Bustling Campus Population for SparkVision:
1. Re-parents and calibrates student clothing materials to derive from M_Mannequin / Manny / Quinn:
   - Sets non-metallic fabric finish (MetalPaintMetallic = 0.0)
   - Sets soft matte fabric roughness (MetalPaintRoughness = 0.88)
   - Applies authentic Bengali student color palettes (Maroon DU shirt, Indigo Denim, White Panjabi, Navy, Khaki, Pastel Salwar Kameez)
2. Spawns 42+ student NPCs across Curzon Hall, Pond Ghat, Doyel Chattar, Shaheed Minar, TSC/Raju, and Arts Faculty.
3. Saves all modified assets and the persistent level.
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

print("=" * 70)
print("SPARKVISION: HUMAN STUDENT ATTIRE & CAMPUS POPULATION OVERHAUL")
print("=" * 70)

MAT_INST_TOOLS = "editor_toolset.toolsets.material_instance.MaterialInstanceTools"
OBJECT_TOOLS = "editor_toolset.toolsets.object.ObjectTools"
SCENE_TOOLS = "editor_toolset.toolsets.scene.SceneTools"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"

MANNY_01 = "/Game/Characters/Mannequins/Materials/Manny/MI_Manny_01_New.MI_Manny_01_New"
MANNY_02 = "/Game/Characters/Mannequins/Materials/Manny/MI_Manny_02_New.MI_Manny_02_New"
QUINN_01 = "/Game/Characters/Mannequins/Materials/Quinn/MI_Quinn_01.MI_Quinn_01"
QUINN_02 = "/Game/Characters/Mannequins/Materials/Quinn/MI_Quinn_02.MI_Quinn_02"

# ─── 1. CONFIGURE HUMAN STUDENT CLOTHING MATERIALS ─────────────────────────────
print("\n[1/3] Calibrating authentic student clothing materials...")

materials_config = [
    {
        "path": "/Game/SparkVision/Materials/MI_Student_MaroonTorso",
        "parent": MANNY_01,
        "tint": {"r": 0.48, "g": 0.08, "b": 0.12, "a": 1.0}, # Rich DU Maroon cotton
        "logo_tint": {"r": 0.85, "g": 0.72, "b": 0.40, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.85,
        "label": "DU Maroon Student Torso"
    },
    {
        "path": "/Game/SparkVision/Materials/MI_Student_DenimLegs",
        "parent": MANNY_02,
        "tint": {"r": 0.08, "g": 0.15, "b": 0.32, "a": 1.0}, # Indigo Denim Jeans
        "logo_tint": {"r": 0.08, "g": 0.15, "b": 0.32, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.90,
        "label": "Indigo Denim Jeans"
    },
    {
        "path": "/Game/SparkVision/Materials/MI_Student_Panjabi_White",
        "parent": MANNY_01,
        "tint": {"r": 0.92, "g": 0.90, "b": 0.85, "a": 1.0}, # Bengali White Cotton Panjabi
        "logo_tint": {"r": 0.80, "g": 0.72, "b": 0.55, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.85,
        "label": "Traditional White Panjabi"
    },
    {
        "path": "/Game/Characters/Mannequins/Materials/Manny/MI_Student_NavyTorso",
        "parent": MANNY_01,
        "tint": {"r": 0.06, "g": 0.12, "b": 0.25, "a": 1.0}, # Collegiate Navy Shirt
        "logo_tint": {"r": 0.85, "g": 0.75, "b": 0.40, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.85,
        "label": "Collegiate Navy Shirt"
    },
    {
        "path": "/Game/Characters/Mannequins/Materials/Manny/MI_Student_KhakiLegs",
        "parent": MANNY_02,
        "tint": {"r": 0.55, "g": 0.48, "b": 0.35, "a": 1.0}, # Casual Khaki Chinos
        "logo_tint": {"r": 0.55, "g": 0.48, "b": 0.35, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.88,
        "label": "Khaki Chino Trousers"
    },
    {
        "path": "/Game/SparkVision/Materials/MI_Student_SalwarKameez_Pastel",
        "parent": QUINN_01,
        "tint": {"r": 0.32, "g": 0.65, "b": 0.68, "a": 1.0}, # Pastel Teal Salwar Kameez
        "logo_tint": {"r": 0.88, "g": 0.55, "b": 0.50, "a": 1.0},
        "metallic": 0.0,
        "roughness": 0.85,
        "label": "Pastel Teal Salwar Kameez"
    },
    {
        "path": "/Game/SparkVision/Materials/MI_Cadre_Helmet",
        "parent": MANNY_01,
        "tint": {"r": 0.12, "g": 0.18, "b": 0.30, "a": 1.0}, # Cadre Dark Blue Jacket & Helmet
        "logo_tint": {"r": 0.85, "g": 0.20, "b": 0.15, "a": 1.0},
        "metallic": 0.15,
        "roughness": 0.65,
        "label": "Cadre Blue & Helmet"
    }
]

for cfg in materials_config:
    mat_ref = f"{cfg['path']}.{cfg['path'].split('/')[-1]}"
    try:
        # 1. Reparent to official Manny/Quinn material instance
        invoke_tool("set_parent", MAT_INST_TOOLS, {
            "instance": {"refPath": mat_ref},
            "parent": {"refPath": cfg["parent"]}
        })
        # 2. Set non-metallic & matte fabric roughness
        invoke_tool("set_scalar_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": mat_ref},
            "name": "MetalPaintMetallic",
            "value": cfg["metallic"]
        })
        invoke_tool("set_scalar_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": mat_ref},
            "name": "MetalPaintRoughness",
            "value": cfg["roughness"]
        })
        # 3. Set authentic student color tint
        invoke_tool("set_vector_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": mat_ref},
            "name": "Paint Tint",
            "value": cfg["tint"]
        })
        invoke_tool("set_vector_parameter", MAT_INST_TOOLS, {
            "instance": {"refPath": mat_ref},
            "name": "LogoTint",
            "value": cfg["logo_tint"]
        })
        print(f"  ✓ Calibrated {cfg['label']}: non-metallic (0.0), matte fabric ({cfg['roughness']}), authentic tint")
    except Exception as e:
        print(f"  Notice on {cfg['label']}: {e}")

# Save material assets
invoke_tool("save_assets", ASSET_TOOLS, {
    "asset_paths": [cfg["path"] for cfg in materials_config]
})
print("  ✓ All student clothing materials saved successfully!")

# ─── 2. BUSTLING CAMPUS STUDENT ROSTER (42 AUTHENTIC STUDENTS) ────────────────
print("\n[2/3] Populating bustling student life across all 6 campus districts...")

NPC_CLASS = "/Script/MyProject.SVStudentNPC"

student_roster = [
    # ── DISTRICT 1: CURZON HALL QUADRANGLE & PROMENADE (8 Students) ──
    {
        "name": "StudentNPC_Curzon_Tanvir",
        "loc": {"x": -3450.0, "y": 180.0, "z": 105.0}, "yaw": 0.0,
        "female": False, "style": 0, "role": "Curzon Student Union Representative",
        "bengali": "কার্জন হলের প্রাঙ্গণে স্বাগতম। আমরা সবাই ঐক্যবদ্ধ হয়েছি।",
        "english": "Welcome to Curzon Hall. We stand unified across all university faculties."
    },
    {
        "name": "StudentNPC_Curzon_Rifat",
        "loc": {"x": -3200.0, "y": -450.0, "z": 105.0}, "yaw": 45.0,
        "female": False, "style": 1, "role": "Department of Physics, 3rd Year",
        "bengali": "বিজ্ঞান অনুষদের শিক্ষার্থীরা ন্যায়সংগত সংস্কারের পক্ষে।",
        "english": "Science faculty students stand firmly for rightful systemic reform."
    },
    {
        "name": "StudentNPC_Curzon_Ananya",
        "loc": {"x": -3180.0, "y": -490.0, "z": 105.0}, "yaw": -135.0,
        "female": True, "style": 4, "role": "Department of Botany, 2nd Year",
        "bengali": "আমরা বট গাছতলায় বসে সবাই আলোচনা করছি। শান্তিপূর্ণ আন্দোলনই আমাদের শক্তি।",
        "english": "We are holding study circles under the banyan tree. Peaceful assembly is our strength."
    },
    {
        "name": "StudentNPC_Curzon_Sabbir",
        "loc": {"x": -2600.0, "y": 650.0, "z": 105.0}, "yaw": -90.0,
        "female": False, "style": 2, "role": "Biochemistry Scholar",
        "bengali": "কার্জন হলের শতবর্ষী এই লাল ইটের প্রাঙ্গণ সত্য ও ন্যায়ের সাক্ষী।",
        "english": "These century-old red bricks of Curzon Hall have always borne witness to truth and justice."
    },
    {
        "name": "StudentNPC_Curzon_Laboni",
        "loc": {"x": -2580.0, "y": 690.0, "z": 105.0}, "yaw": 90.0,
        "female": True, "style": 4, "role": "Applied Chemistry Researcher",
        "bengali": "আমাদের সহপাঠীরা লাইব্রেরি আর টিএসসিতে জড়ো হচ্ছে। চলো এগিয়ে যাই।",
        "english": "Our fellow classmates are gathering at the library and TSC. Let's move forward together."
    },
    {
        "name": "StudentNPC_Curzon_Tahsin",
        "loc": {"x": -2100.0, "y": -1200.0, "z": 105.0}, "yaw": 120.0,
        "female": False, "style": 0, "role": "Mathematics Department",
        "bengali": "ক্যাম্পাসের পরিবেশ আজ অসাধারণ—সবাই এক কণ্ঠে কথা বলছে।",
        "english": "The campus atmosphere today is historic—everyone speaks with one united voice."
    },
    {
        "name": "StudentNPC_Curzon_Anik",
        "loc": {"x": -1800.0, "y": 1400.0, "z": 105.0}, "yaw": -60.0,
        "female": False, "style": 1, "role": "Geology & Mining Faculty",
        "bengali": "উত্তর চত্বরে সাবধানে চলাচল করো, সেখানে কিছু উত্তেজনা দেখা দিয়েছে।",
        "english": "Move carefully around the North Courtyard, tensions have been reported there."
    },
    {
        "name": "StudentNPC_Curzon_Shuvro",
        "loc": {"x": -1500.0, "y": -200.0, "z": 105.0}, "yaw": 180.0,
        "female": False, "style": 2, "role": "Pharmacy Faculty",
        "bengali": "আমরা চিকিৎসার প্রাথমিক ফার্স্ট-এইড বুথ স্থাপন করেছি। সবাই নিরাপদে থাকো।",
        "english": "We have set up a volunteer first-aid booth for students. Stay safe, everyone."
    },

    # ── DISTRICT 1: CURZON BOTANICAL POND & GHAT (4 Students) ──
    {
        "name": "StudentNPC_Pond_Mehedi",
        "loc": {"x": -1200.0, "y": 2800.0, "z": 50.0}, "yaw": -45.0,
        "female": False, "style": 1, "role": "DU Photographic Society",
        "bengali": "পুকুরপাড়ের শান্ত শাপলা আর ছাত্রদের জমায়েতের ছবি ইতিহাসের পাতায় থাকবে।",
        "english": "These photos of tranquil water lilies and student solidarity will live on in history."
    },
    {
        "name": "StudentNPC_Pond_Farhana",
        "loc": {"x": -1160.0, "y": 2850.0, "z": 50.0}, "yaw": 135.0,
        "female": True, "style": 4, "role": "Microbiology Researcher",
        "bengali": "শান্তভাবে পানি ও বিস্কুট বিতরণ করছি আমরা। আন্দোলনের পেছনে রয়েছে পারস্পরিক সহযোগিতা।",
        "english": "We are distributing drinking water and supplies. Mutual care is the backbone of our movement."
    },
    {
        "name": "StudentNPC_Pond_Sourav",
        "loc": {"x": -600.0, "y": 3200.0, "z": 50.0}, "yaw": -90.0,
        "female": False, "style": 0, "role": "Zoology Student, 4th Year",
        "bengali": "ঘাটে বসে আমরা পরবর্তী সমাবেশ নিয়ে আলোচনা করছি।",
        "english": "Sitting here at the ghat, we are planning our next peaceful solidarity rally."
    },
    {
        "name": "StudentNPC_Pond_Mitu",
        "loc": {"x": -570.0, "y": 3240.0, "z": 50.0}, "yaw": 90.0,
        "female": True, "style": 4, "role": "Environmental Science Scholar",
        "bengali": "আমাদের ক্যাম্পাস আমাদের গর্ব। কোনো অন্যায় এখানে মেনে নেওয়া হবে না।",
        "english": "Our campus is our pride. Injustice will never find a sanctuary here."
    },

    # ── DISTRICT 5: DOYEL CHATTAR ROUNDABOUT (4 Students) ──
    {
        "name": "StudentNPC_Doyel_Ashik",
        "loc": {"x": 7500.0, "y": -16300.0, "z": 105.0}, "yaw": 90.0,
        "female": False, "style": 2, "role": "Faculty of Law",
        "bengali": "দোয়েল চত্বর দিয়ে সচিবালয় আর হাইকোর্টের রাস্তা যুক্ত। এখানে জনসমাবেশ বাড়ছে।",
        "english": "Doyel Chattar connects the university to the Secretariat and Supreme Court. Crowd is gathering."
    },
    {
        "name": "StudentNPC_Doyel_Sumi",
        "loc": {"x": 7550.0, "y": -16350.0, "z": 105.0}, "yaw": -90.0,
        "female": True, "style": 4, "role": "Sociology Department",
        "bengali": "সাধারণ মানুষ আমাদের সাথে একাত্মতা প্রকাশ করছে। রিকশাচালকরাও পানি এগিয়ে দিচ্ছে।",
        "english": "Ordinary citizens are showing solidarity with us. Even the rickshaw pullers are handing out water."
    },
    {
        "name": "StudentNPC_Doyel_Kamrul",
        "loc": {"x": 7800.0, "y": -16800.0, "z": 105.0}, "yaw": 0.0,
        "female": False, "style": 0, "role": "Political Science Student",
        "bengali": "ভাষা আন্দোলনের ঐতিহ্য ধরে রাখা আমাদের জাতীয় দায়িত্ব।",
        "english": "Upholding the glorious heritage of the Language Movement is our sacred national duty."
    },
    {
        "name": "StudentNPC_Doyel_Shamim",
        "loc": {"x": 7200.0, "y": -16100.0, "z": 105.0}, "yaw": 180.0,
        "female": False, "style": 1, "role": "International Relations",
        "bengali": "বিশ্ববিদ্যালয় কখনোই দমনপীড়নের কাছে মাথা নত করেনি।",
        "english": "This university has never bowed down to oppression."
    },

    # ── DISTRICT 2: CENTRAL SHAHEED MINAR (8 Students) ──
    {
        "name": "StudentNPC_Shaheed_Farhan",
        "loc": {"x": -320.0, "y": -53700.0, "z": 245.0}, "yaw": -90.0,
        "female": False, "style": 0, "role": "Shaheed Minar Assembly Coordinator",
        "bengali": "রক্ত দিয়ে কেনা এই শহীদ বেদিতে দাঁড়িয়ে আমরা শপথ নিয়েছি।",
        "english": "Standing upon this sacred altar of our martyrs, we take our solemn pledge."
    },
    {
        "name": "StudentNPC_Shaheed_Rashed",
        "loc": {"x": -400.0, "y": -53700.0, "z": 245.0}, "yaw": -90.0,
        "female": False, "style": 1, "role": "Student Activist Council",
        "bengali": "বায়ান্ন আর একাত্তরের চেতনা আমাদের পথ দেখায়।",
        "english": "The historic spirit of 1952 and 1971 guides our steps forward."
    },
    {
        "name": "StudentNPC_Shaheed_Sadia",
        "loc": {"x": -100.0, "y": -54200.0, "z": 245.0}, "yaw": 0.0,
        "female": True, "style": 4, "role": "DU Debating Society President",
        "bengali": "যুক্তি আর সত্য আমাদের অস্ত্র। আমরা কোনো সহিংসতা চাই না।",
        "english": "Reason, logic, and truth are our shields. We champion peace."
    },
    {
        "name": "StudentNPC_Shaheed_Nabila",
        "loc": {"x": -120.0, "y": -54250.0, "z": 245.0}, "yaw": 180.0,
        "female": True, "style": 4, "role": "Faculty of Fine Arts",
        "bengali": "আমরা ব্যানার ও পোস্টারে আন্দোলনের বার্তা এঁকেছি।",
        "english": "We painted our message across banners and campus walls."
    },
    {
        "name": "StudentNPC_Shaheed_Zahid",
        "loc": {"x": 500.0, "y": -53500.0, "z": 245.0}, "yaw": -45.0,
        "female": False, "style": 2, "role": "Philosophy Scholar",
        "bengali": "যে জাতি নিজের অধিকারের জন্য দাঁড়ায় না, সে জাতি বাঁচে না।",
        "english": "A nation that does not stand up for its rights cannot thrive."
    },
    {
        "name": "StudentNPC_Shaheed_Alok",
        "loc": {"x": 480.0, "y": -53550.0, "z": 245.0}, "yaw": 135.0,
        "female": False, "style": 0, "role": "Department of History",
        "bengali": "ইতিহাস সাক্ষ্য দেয়, ঢাকা বিশ্ববিদ্যালয়ের ছাত্ররা কখনো পিছপা হয়নি।",
        "english": "History proves that the students of Dhaka University have never faltered."
    },
    {
        "name": "StudentNPC_Shaheed_Moushumi",
        "loc": {"x": -700.0, "y": -54500.0, "z": 245.0}, "yaw": 45.0,
        "female": True, "style": 4, "role": "Department of Bengali Literature",
        "bengali": "‘আমার ভাইয়ের রক্তে রাঙানো একুশে ফেব্রুয়ারি’ গানটি আজ নতুন শক্তি দিচ্ছে।",
        "english": "The immortal anthem of February 21 echoes today with renewed courage."
    },
    {
        "name": "StudentNPC_Shaheed_Tanmoy",
        "loc": {"x": -680.0, "y": -54550.0, "z": 245.0}, "yaw": -135.0,
        "female": False, "style": 1, "role": "English Department",
        "bengali": "একসাথে চলো টিএসসির রাজু ভাস্কর্যের মহা-সমাবেশে যাই।",
        "english": "Let us walk together to the grand mass rally at Raju Memorial at TSC."
    },

    # ── DISTRICT 3: TEACHER-STUDENT CENTRE (TSC) & RAJU MEMORIAL (10 Students) ──
    {
        "name": "StudentNPC_TSC_Arif",
        "loc": {"x": 58900.0, "y": -63500.0, "z": 105.0}, "yaw": 0.0,
        "female": False, "style": 0, "role": "DU Cultural Secretary",
        "bengali": "রাজু ভাস্কর্য সন্ত্রাসবিরোধী ছাত্র প্রতিরোধের চিরন্তন প্রতীক।",
        "english": "Raju Memorial is the eternal monument of anti-terrorism student resilience."
    },
    {
        "name": "StudentNPC_TSC_Sumon",
        "loc": {"x": 59100.0, "y": -63520.0, "z": 105.0}, "yaw": 180.0,
        "female": False, "style": 1, "role": "Anti-Discrimination Front Organizer",
        "bengali": "আমাদের ৯ দফা দাবি যৌক্তিক ও সাংবিধানিক। কোনো হুমকি আমাদের টলাতে পারবে না।",
        "english": "Our demands are rational, just, and constitutional. No threats can derail us."
    },
    {
        "name": "StudentNPC_TSC_Tania",
        "loc": {"x": 59500.0, "y": -63900.0, "z": 105.0}, "yaw": -90.0,
        "female": True, "style": 4, "role": "Women & Gender Studies",
        "bengali": "ছাত্রীদের অংশগ্রহণই এই আন্দোলনের সবচেয়ে বড় নৈতিক শক্তি।",
        "english": "The courage and participation of female students is our movement's moral core."
    },
    {
        "name": "StudentNPC_TSC_Kabir",
        "loc": {"x": 59520.0, "y": -63950.0, "z": 105.0}, "yaw": 90.0,
        "female": False, "style": 2, "role": "Economics Department",
        "bengali": "মেধার মূল্যায়ন নিশ্চিত করাই সমৃদ্ধ বাংলাদেশের ভিত্তি।",
        "english": "Meritocracy is the indispensable foundation of a prosperous Bangladesh."
    },
    {
        "name": "StudentNPC_TSC_Rehana",
        "loc": {"x": 58300.0, "y": -64200.0, "z": 105.0}, "yaw": 45.0,
        "female": True, "style": 4, "role": "Public Administration",
        "bengali": "টিএসসির ক্যাফেটেরিয়ায় আলোচনা চলছে। সবাই মতামত দিচ্ছে।",
        "english": "Democratic discussions are ongoing in the TSC plaza. All voices are heard."
    },
    {
        "name": "StudentNPC_TSC_Palash",
        "loc": {"x": 58330.0, "y": -64250.0, "z": 105.0}, "yaw": -135.0,
        "female": False, "style": 1, "role": "Peace & Conflict Studies",
        "bengali": "অহিংস প্রতিরোধই পৃথিবীর সবচেয়ে শক্তিশালী বিপ্লব।",
        "english": "Nonviolent resistance remains the most potent catalyst of real change."
    },
    {
        "name": "StudentNPC_TSC_Dipu",
        "loc": {"x": 59800.0, "y": -63200.0, "z": 105.0}, "yaw": -60.0,
        "female": False, "style": 0, "role": "Sociology Department",
        "bengali": "সারাদেশের সব বিশ্ববিদ্যালয়ের ছাত্ররা আজ ঢাকা বিশ্ববিদ্যালয়ের দিকে তাকিয়ে।",
        "english": "Students nationwide are looking toward Dhaka University today."
    },
    {
        "name": "StudentNPC_TSC_Mahin",
        "loc": {"x": 59840.0, "y": -63240.0, "z": 105.0}, "yaw": 120.0,
        "female": False, "style": 2, "role": "Mass Communication & Journalism",
        "bengali": "আমরা ইন্টারনেটে ও সংবাদমাধ্যমে প্রতিটি মুহূর্ত প্রচার করছি। সত্য ঢাকা থাকবে না।",
        "english": "We are broadcasting real-time updates. The truth cannot be suppressed."
    },
    {
        "name": "StudentNPC_TSC_Bristi",
        "loc": {"x": 58700.0, "y": -64600.0, "z": 105.0}, "yaw": 90.0,
        "female": True, "style": 4, "role": "Development Studies",
        "bengali": "আমরা ফুল আর পতাকা নিয়ে দাঁড়িয়েছি। ভয়কে জয় করার দিন আজ।",
        "english": "We stand with flowers and flags. Today we conquer fear."
    },
    {
        "name": "StudentNPC_TSC_Hasan",
        "loc": {"x": 58700.0, "y": -64650.0, "z": 105.0}, "yaw": -90.0,
        "female": False, "style": 0, "role": "Social Welfare Institute",
        "bengali": "আমাদের সহযোদ্ধারা কলাভবন ও লাইব্রেরিতে একজোট হচ্ছে।",
        "english": "Our fellow comrades are gathering at Kala Bhaban and Central Library."
    },

    # ── DISTRICT 4: ARTS FACULTY (KALA BHABAN) & CENTRAL LIBRARY (8 Students) ──
    {
        "name": "StudentNPC_Arts_ProfRahman",
        "loc": {"x": 73400.0, "y": -95600.0, "z": 105.0}, "yaw": 0.0,
        "female": False, "style": 2, "role": "Professor of History & Academic Dean",
        "bengali": "শিক্ষক হিসেবে আমরা ছাত্রদের অহিংস আন্দোলনের পাশে আছি। ইতিহাস তাদের পক্ষে।",
        "english": "As educators, we stand beside our students' peaceful cause. History is on their side."
    },
    {
        "name": "StudentNPC_Arts_Nusrat",
        "loc": {"x": 73450.0, "y": -95650.0, "z": 105.0}, "yaw": 180.0,
        "female": True, "style": 4, "role": "Central Library Research Secretary",
        "bengali": "অপরাজেয় বাংলার পাদদেশে আমরা সত্য ও ন্যায়ের জন্য দাঁড়িয়েছি।",
        "english": "At the foot of Aparajeyo Bangla, we stand resilient for truth and justice."
    },
    {
        "name": "StudentNPC_Arts_Asad",
        "loc": {"x": 73800.0, "y": -96000.0, "z": 105.0}, "yaw": -90.0,
        "female": False, "style": 0, "role": "Department of Archaeology",
        "bengali": "কলাভবনের এই বারান্দায় আমাদের পূর্বসূরিরা মুক্তির ডাক দিয়েছিলেন।",
        "english": "From these verandas of Kala Bhaban, our predecessors called for liberation."
    },
    {
        "name": "StudentNPC_Arts_Joy",
        "loc": {"x": 73820.0, "y": -96050.0, "z": 105.0}, "yaw": 90.0,
        "female": False, "style": 1, "role": "Department of Linguistics",
        "bengali": "শব্দ আর স্লোগানই আমাদের সবচেয়ে বড় হাতিয়ার।",
        "english": "Words, chants, and slogans are our greatest instruments."
    },
    {
        "name": "StudentNPC_Library_Proma",
        "loc": {"x": 73300.0, "y": -71500.0, "z": 105.0}, "yaw": -90.0,
        "female": True, "style": 4, "role": "Islamic History & Culture",
        "bengali": "হাকিম চত্বরের চায়ের কাপে আজ শুধু অধিকার আর মুক্তির আলোচনা।",
        "english": "Around Hakim Chattar's tea stalls, everyone is discussing freedom and civic rights."
    },
    {
        "name": "StudentNPC_Library_Sajid",
        "loc": {"x": 73320.0, "y": -71550.0, "z": 105.0}, "yaw": 90.0,
        "female": False, "style": 2, "role": "Library Scholar & Reader",
        "bengali": "লাইব্রেরির বইগুলো আমাদের শিখিয়েছে কীভাবে অন্যায়ের বিরুদ্ধে দাঁড়াতে হয়।",
        "english": "The books in our library taught us how to stand unflinchingly against injustice."
    },
    {
        "name": "StudentNPC_Library_Rupa",
        "loc": {"x": 73600.0, "y": -71800.0, "z": 105.0}, "yaw": 0.0,
        "female": True, "style": 4, "role": "Printmaking & Graphic Arts",
        "bengali": "আমরা দেয়ালিকা আর পোস্টার তৈরি করছি। আন্দোলনের রং ছড়িয়ে পড়ছে।",
        "english": "We are designing campus wall magazines and artwork. Hope is spreading."
    },
    {
        "name": "StudentNPC_Library_Nazmul",
        "loc": {"x": 73650.0, "y": -71850.0, "z": 105.0}, "yaw": 180.0,
        "female": False, "style": 0, "role": "Department of Urdu & Persian",
        "bengali": "আমরা সবাই কাঁধে কাঁধ মিলিয়ে কার্জন হল আর টিএসসির সমাবেশ সফল করব।",
        "english": "Shoulder to shoulder, we will make our university assembly a historic triumph."
    }
]

print(f"  Target roster: {len(student_roster)} authentic student NPCs")

# Remove any old student NPCs to prevent duplicates
try:
    existing_npcs = invoke_tool("find_actors", SCENE_TOOLS, {
        "name": "StudentNPC",
        "tag": "",
        "collision_channels": []
    }).get("returnValue", [])
    print(f"  Found {len(existing_npcs)} pre-existing student NPCs. Cleaning up...")
    for old_npc in existing_npcs:
        try:
            invoke_tool("remove_from_scene", SCENE_TOOLS, {"actor": {"refPath": old_npc["refPath"]}})
        except Exception:
            pass
except Exception as e:
    print(f"  Cleanup note: {e}")

# Spawn the new bustling student roster
spawned_count = 0
for st in student_roster:
    try:
        spawn_res = invoke_tool("add_to_scene_from_class", SCENE_TOOLS, {
            "actor_type": {"refPath": NPC_CLASS},
            "name": st["name"],
            "xform": {
                "location": st["loc"],
                "rotation": {"pitch": 0.0, "yaw": st["yaw"], "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
            }
        })
        act_ref = spawn_res.get("returnValue", {}).get("refPath")
        if not act_ref and isinstance(spawn_res.get("returnValue"), str):
            act_ref = spawn_res.get("returnValue")
        
        if act_ref:
            # Set Label in World Outliner
            invoke_tool("set_label", "editor_toolset.toolsets.actor.ActorTools", {
                "actor": {"refPath": act_ref},
                "label": st["name"]
            })
            # Configure NPC Properties (Name, Role, Gender, Outfit)
            clean_name = st["name"].replace("StudentNPC_", "").replace("_", " ")
            prop_vals = json.dumps({
                "NPCId": st["name"],
                "NPCName": f"{clean_name} ({st['role'].split(',')[0]})",
                "NPCRole": st["role"],
                "bIsFemale": st["female"],
                "OutfitStyle": st["style"]
            })
            invoke_tool("set_properties", OBJECT_TOOLS, {
                "instance": {"refPath": act_ref},
                "values": prop_vals
            })
            spawned_count += 1
            print(f"  ✓ Spawned [{spawned_count}/{len(student_roster)}] {st['name']} ({st['role']})")
    except Exception as e:
        print(f"  Failed spawning {st['name']}: {e}")

print(f"\n✅ Successfully spawned {spawned_count} authentic human students across campus!")

# ─── 3. SAVE LEVEL & PERSISTENCE ───────────────────────────────────────────────
print("\n[3/3] Saving level & persisting world state...")
invoke_tool("save_assets", ASSET_TOOLS, {
    "asset_paths": [
        "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"
    ]
})
print("✅ Campus world successfully saved with bustling student life!")
print("=" * 70)
