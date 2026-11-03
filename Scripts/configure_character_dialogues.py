#!/usr/bin/env python3
"""
Configure Exactly 3 Rich Bilingual Dialogues (Bengali + English Subtitles) on Campus NPCs
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

CHARACTER_DATA = [
    {
        "search_name": "Prof_Jamal",
        "dialogues": [
            ("কার্জন হলের শতবর্ষের ঐতিহ্য শুধু লাল ইটে নয়, সত্যেন বোসের বোস-আইনস্টাইন কোয়ান্টাম সংখ্যাতত্ত্বের সূতিকাগার এই গবেষণাগারে। বিজ্ঞানের এই মুক্তচিন্তা যেন কখনও রুদ্ধ না হয়।",
             "The century-old heritage of Curzon Hall lies not merely in its red bricks, but in these laboratories where Satyendra Nath Bose pioneered Bose-Einstein quantum statistics. Keep the spirit of scientific enquiry alive."),
            ("বিজ্ঞান অনুষদের প্রাচীন গবেষণাপত্রগুলো সামনের আর্কাইভ টার্মিনালে সংরক্ষিত আছে। তুমি গবেষণা নথিগুলো সংগ্রহ করে মিশন এগিয়ে নাও।",
             "The ancient research manuscripts of the Science Faculty are preserved in the front Archive Terminal. Gather the research documents to progress your mission."),
            ("তোমাদের আন্দোলন সত্য ও ন্যায়ের পক্ষে। গ্রন্থাগার ও গবেষণাগারের পবিত্রতা রক্ষা করে ক্যাম্পাসে শান্তিপূর্ণভাবে অগ্রসর হও।",
             "Your assembly stands for truth and justice. Preserve the sanctity of our libraries and laboratories as you move peacefully across campus.")
        ]
    },
    {
        "search_name": "NPC_Sabbir",
        "dialogues": [
            ("কার্জন হলের লাল ইটের বারান্দায় বসে বন্ধুদের সাথে আড্ডা আর পড়াশোনা করার আনন্দই আলাদা!",
             "Nothing beats studying and having adda with friends along the red-brick verandas of Curzon Hall!"),
            ("সামনের পুকুরঘাটের কাছে গিয়ে দেখো, কৃষ্ণচূড়া আর শতবর্ষী বটের ছায়ায় পুরো ক্যাম্পাস শান্ত স্নিগ্ধ লাগে।",
             "Head over to the pond ghat ahead—under the shade of scarlet Krishnachura and ancient banyans, the entire campus feels tranquil."),
            ("আন্দোলনের মধ্যেও আমরা পড়াশোনা থামাইনি। জ্ঞান ও একতাই শিক্ষার্থীদের আসল শক্তি।",
             "Even amidst our movement, studies never stop. Knowledge and solidarity are our truest strength.")
        ]
    },
    {
        "search_name": "NPC_Rifat",
        "dialogues": [
            ("আজ ল্যাবে বেশিক্ষণ কাজ করতে হলো। বিকেলের বাতাসটা কী আরামদায়ক!",
             "Had to spend extra hours in the organic chemistry lab today. The afternoon campus breeze is so refreshing!"),
            ("তুমি কি উত্তর প্রাঙ্গণের মার্শাল আর্টস ক্লাবের অনুশীলনে যাচ্ছ? ফাহিম ভাই ওখানে অনুশীলন করছেন।",
             "Are you heading to the North Courtyard martial arts practice? Brother Fahim is sparring there right now."),
            ("আজকের সমাবেশ অনেক বড় হতে চলেছে। আমরা সবাইকে শান্ত থাকার এবং উসকানি এড়িয়ে চলার পরামর্শ দিচ্ছি।",
             "Today's assembly is growing massive. We're urging everyone to remain peaceful and avoid any provocations.")
        ]
    },
    {
        "search_name": "NPC_Ananya",
        "dialogues": [
            ("কার্জন পুকুরের এই পদ্মফুল আর ঝুলে থাকা বটের ঝুরিগুলো আমাদের ক্যাম্পাসের এক শতাব্দীর প্রকৃতির সাক্ষী।",
             "These blooming lotus flowers and draping banyan roots of Curzon Pond have witnessed a century of campus natural history."),
            ("পানিতে সূর্যের আলোর ঝিকিমিকি দেখলে মন ভালো হয়ে যায়। সাবধানে ঘাটের সিঁড়ি দিয়ে নেমে আসো।",
             "Watching sunlight glitter across the water surface calms the mind. Step down carefully along the ghat stone steps."),
            ("বটগাছের ছায়ায় বসে গবেষণার নোট তৈরি করছিলাম। পুকুরের জলে কার্জনের রক্তিম প্রতিবিম্ব দেখলে মন ভরে যায়।",
             "I was taking field research notes beneath the banyan canopy. The reflection of Curzon's red domes upon the water is breathtaking.")
        ]
    },
    {
        "search_name": "NPC_Mehedi",
        "dialogues": [
            ("বিকেলের আলোয় কার্জন পুকুরের পানি আর প্রাচীন বটের ফ্রেম অসাধারণ এসেছে!",
             "In this golden afternoon light, the framing of Curzon pond reflection against the heritage banyan is stunning!"),
            ("ঢাকা বিশ্ববিদ্যালয়ের মতো এত সবুজ ও নান্দনিক ক্যাম্পাস পুরো দেশে আর কোথাও পাবে না।",
             "You won't find a greener and more aesthetically inspiring campus anywhere in the country."),
            ("সোনালী গোধূলিতে ছাত্রসমাজের এই ঐতিহাসিক মুহূর্তগুলো ক্যামেরাবন্দী করছি।",
             "In this golden dusk, I am documenting these historic moments of our student body through the lens.")
        ]
    },
    {
        "search_name": "Student_Commuter_01",
        "dialogues": [
            ("লাইব্রেরি থেকে বই নিয়ে কার্জন হলে যাচ্ছি। ক্যাম্পাসের ছায়াঘেরা রাস্তাগুলো হাঁটতে ভীষণ ভালো লাগে।",
             "Returning from the Central Library to Curzon. Walking through these tree-shaded campus avenues is pure joy."),
            ("ক্যাম্পাসের প্রতিটি কোণায় নতুন উদ্দীপনা। শিক্ষার্থীরা দলবেঁধে আলোচনা করছে।",
             "A vibrant spirit fills every corner of campus today. Students are gathering in lively discussions."),
            ("আর্কাইভ টার্মিনালের তথ্যগুলো সংগ্রহ করেছ তো? ওগুলো আমাদের ইতিহাস সংরক্ষণের চাবিকাঠি।",
             "Have you gathered the records from the archive terminal? They are the key to preserving our history.")
        ]
    },
    {
        "search_name": "Student_Commuter_02",
        "dialogues": [
            ("টিএসসির সাহিত্য আড্ডায় যাওয়ার জন্য বের হয়েছি। তুমিও কি ওখানে যাচ্ছ?",
             "On my way to the literature adda at TSC. Are you heading there as well?"),
            ("ক্যাম্পাসের চারপাশের আধুনিক বহুতল টাওয়ারগুলোর সাথে কার্জনের ঐতিহ্যের মেলবন্ধন দারুণ।",
             "The visual harmony between modern skyline towers and Curzon's heritage is breathtaking."),
            ("চলো হেঁটে যাই, ক্যাম্পাসের বিকেলের হাওয়া সবসময়ই অন্যরকম প্রশান্তি দেয়।",
             "Let's walk together; the university's late afternoon breeze always brings unmatched tranquility.")
        ]
    },
    {
        "search_name": "NPC_Sadia",
        "dialogues": [
            ("টিএসসি হলো ঢাকা বিশ্ববিদ্যালয়ের মুক্তবুদ্ধি চর্চা, যুক্তিবাদ আর সাংস্কৃতিক আন্দোলনের অনন্ত বাতিঘর।",
             "TSC is the eternal beacon of free thought, rational debate, and cultural movements at Dhaka University."),
            ("রাজু ভাস্কর্যের সামনে দাঁড়িয়ে অন্যায়ের বিরুদ্ধে শপথ নেওয়া আমাদের শিক্ষার্থীদের ঐতিহ্য।",
             "Standing before Raju Memorial and taking an oath against injustice is our proud student tradition."),
            ("যুক্তি আর আলোচনা দিয়েই আমরা সংকট সমাধান করব। কোনো সংঘাতের পথ নয়।",
             "Through logic and reasoned debate we resolve every crisis—not through destructive conflict.")
        ]
    },
    {
        "search_name": "NPC_Arif",
        "dialogues": [
            ("বসন্ত উৎসব আর পহেলা বৈশাখের প্রস্তুতি চলছে টিএসসির ক্যাফেটেরিয়া চত্বরে!",
             "Preparations for the spring festival and Pohela Boishakh celebrations are underway at the TSC cafeteria quad!"),
            ("টিএসসির চত্বরে আমরা গণসংগীত ও পথনাটকের মহড়া করছি। সুর আর সংস্কৃতির শক্তি সবচাইতে বড় প্রতিরোধ।",
             "We are rehearsing mass resistance songs and street theater at TSC. Culture and melody are our greatest peaceful power."),
            ("সংস্কৃতির মাধ্যমেই মানুষের মনের জড়তা কাটে, ঐক্য দৃঢ় হয়।",
             "Through artistic expression, human hearts awaken and our communal unity grows unshakeable.")
        ]
    },
    {
        "search_name": "Prof_Rahman",
        "dialogues": [
            ("কলা ভবনের এই প্রাঙ্গণ থেকেই ১৯৭১ সালের মহান স্বাধীনতা সংগ্রামের ডাক উঠেছিল। আমাদের ছাত্র-শিক্ষকদের আত্মত্যাগ অমর।",
             "From this very courtyard of Kala Bhaban, the historic clarion call of our 1971 Liberation War was sounded. The sacrifice of our students and teachers is immortal."),
            ("অপরাজেয় বাংলা ভাস্কর্যটি নিবিড়ভাবে লক্ষ্য করো—কৃষক, ছাত্র ও নারীদের সম্মিলিত প্রতিরোধ কীভাবে জাতিকে মুক্ত করেছিল।",
             "Observe the Aparajeyo Bangla sculpture closely—it embodies how peasants, students, and women joined together in heroic resistance to liberate our nation."),
            ("কলা ভবনের এই আধুনিক নকশাটি আমাদের ভাষা আন্দোলন ও স্বাধীনতা-পরবর্তী আধুনিক স্থাপত্যের উজ্জ্বল নিদর্শন।",
             "This modern architectural design of Kala Bhaban stands as a brilliant testament to post-independence modernist architecture.")
        ]
    },
    {
        "search_name": "NPC_Nabila",
        "dialogues": [
            ("সৈয়দ আবদুল্লাহ খালিদের নির্মিত অপরাজেয় বাংলার প্রতিটি রেখায় এক অমর দ্রোহের শক্তি প্রকাশ পেয়েছে।",
             "In every contour of Aparajeyo Bangla sculpted by Syed Abdullah Khalid, an immortal spirit of defiance is etched."),
            ("চারুকলা ও কলা ভবনের এই স্যান্ডস্টোন আধুনিক দেওয়ালগুলো আমাদের নিজস্ব স্থাপত্য ধারণ করে। আমরা নতুন পোস্টার আঁকছি।",
             "These sandstone-toned modern louvers of Kala Bhaban reflect our indigenous modernism. We are painting commemorative posters."),
            ("শিল্পের কাজই হলো সত্যকে সবার সামনে নির্ভীকভাবে তুলে ধরা।",
             "The true purpose of art is to portray truth before everyone without fear.")
        ]
    },
    {
        "search_name": "NPC_Farhan",
        "dialogues": [
            ("১৯৫২ সালের ২১শে ফেব্রুয়ারি মাতৃভাষা বাংলার মর্যাদার জন্য শহীদ বরকত, সালাম, রফিক ও জব্বাররা রক্ত দিয়ে ইতিহাস সৃষ্টি করেছিলেন।",
             "On 21 February 1952, martyrs Barkat, Salam, Rafiq, and Jabbar shed their blood for the honor of Bengali language, carving our identity into world history."),
            ("রক্তিম সূর্য আর শ্বেতশুভ্র স্তম্ভগুলো মাতৃক্রোড়ে সন্তানের চিরন্তন ভালোবাসার প্রতীক।",
             "The glowing crimson sun and pristine white marble pillars symbolize mother Bengal cradling her martyr sons."),
            ("এই পবিত্র বেদীতে দাঁড়ালে প্রতিটি বাঙালির মাথা শ্রদ্ধায় অবনত হয়ে যায়।",
             "Standing upon this sacred altar, every Bengali's head bows in solemn reverence.")
        ]
    }
]

def main():
    print("=" * 70)
    print("CONFIGURING EXACT 3-ENTRY BILINGUAL DIALOGUES ON CAMPUS NPCS")
    print("=" * 70)

    success_count = 0
    for item in CHARACTER_DATA:
        s_name = item["search_name"]
        actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {
            "name": s_name, "tag": "", "collision_channels": []
        }).get("returnValue", [])

        if not actors:
            print(f"  ⚠️ Could not find actor matching '{s_name}'")
            continue

        actor = actors[0]
        entries = []
        for ben, eng in item["dialogues"]:
            entries.append({
                "bengaliText": ben,
                "englishSubtitle": eng
            })

        try:
            res = invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
                "instance": actor,
                "values": json.dumps({
                    "DialogueEntries": entries
                })
            })
            if res.get("returnValue") is True:
                print(f"  ✓ Successfully set 3 dialogues on {s_name}")
                success_count += 1
            else:
                print(f"  Notice setting dialogues on {s_name}: {res}")
        except Exception as e:
            print(f"  Error setting dialogues on {s_name}: {e}")

    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print(f"\n✅ Successfully updated dialogues on {success_count}/{len(CHARACTER_DATA)} NPCs and saved level!")
    except Exception as e:
        print(f"Notice saving level: {e}")

if __name__ == "__main__":
    main()
