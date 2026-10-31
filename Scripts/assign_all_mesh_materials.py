#!/usr/bin/env python3
import json
import subprocess

MATERIAL_MAP = {
    "M_Curzon_Brick": "/Game/SparkVision/Materials/MI_Curzon_Brick.MI_Curzon_Brick",
    "M_Curzon_WhiteTrim": "/Game/SparkVision/Materials/MI_Curzon_WhiteTrim.MI_Curzon_WhiteTrim",
    "M_Curzon_Sandstone": "/Game/SparkVision/Materials/MI_Curzon_Sandstone.MI_Curzon_Sandstone",
    "M_Curzon_Tiles": "/Game/SparkVision/Materials/MI_Curzon_Tiles.MI_Curzon_Tiles",
    "M_Curzon_Brass": "/Game/SparkVision/Materials/MI_Curzon_Brass.MI_Curzon_Brass",
    "M_Curzon_CastIron": "/Game/SparkVision/Materials/MI_Curzon_CastIron.MI_Curzon_CastIron",
    "M_Curzon_Accent": "/Game/SparkVision/Materials/MI_Curzon_CastIron.MI_Curzon_CastIron",
    "M_Bark_Banyan": "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
    "M_Foliage_Banyan_Leaf": "/Game/SparkVision/Materials/MI_Foliage_Banyan_Leaf.MI_Foliage_Banyan_Leaf",
    "M_Bark_Raintree": "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
    "M_Foliage_Raintree_Leaf": "/Game/SparkVision/Materials/MI_Foliage_Raintree_Leaf.MI_Foliage_Raintree_Leaf",
    "M_Bark_Krishnachura": "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
    "M_Foliage_Krishnachura_Red": "/Game/SparkVision/Materials/MI_Foliage_Krishnachura_Red.MI_Foliage_Krishnachura_Red",
    "M_Bark_Radhachura": "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
    "M_Foliage_Radhachura_Yellow": "/Game/SparkVision/Materials/MI_Foliage_Radhachura_Yellow.MI_Foliage_Radhachura_Yellow",
    "M_Bark_Jarul": "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
    "M_Foliage_Jarul_Lilac": "/Game/SparkVision/Materials/MI_Foliage_Jarul_Lilac.MI_Foliage_Jarul_Lilac",
    "M_Bark_Neem": "/Game/SparkVision/Materials/MI_Bark_Tree.MI_Bark_Tree",
    "M_Foliage_Neem_Green": "/Game/SparkVision/Materials/MI_Foliage_Neem_Green.MI_Foliage_Neem_Green",
    "M_Bark_PalmRinged": "/Game/SparkVision/Materials/MI_Bark_Palm.MI_Bark_Palm",
    "M_Foliage_PalmFrond": "/Game/SparkVision/Materials/MI_Foliage_PalmFrond.MI_Foliage_PalmFrond",
    "M_Bark_BetelGreen": "/Game/SparkVision/Materials/MI_Bark_Palm.MI_Bark_Palm",
    "M_Foliage_BetelCrown": "/Game/SparkVision/Materials/MI_Foliage_PalmFrond.MI_Foliage_PalmFrond",
    "M_Stem_BambooGold": "/Game/SparkVision/Materials/MI_Stem_BambooGold.MI_Stem_BambooGold",
    "M_Foliage_BambooLeaf": "/Game/SparkVision/Materials/MI_Foliage_BambooLeaf.MI_Foliage_BambooLeaf",
    "M_Foliage_LilyPad": "/Game/SparkVision/Materials/MI_Foliage_LilyPad.MI_Foliage_LilyPad",
    "M_Flower_Shapla": "/Game/SparkVision/Materials/MI_Flower_Shapla.MI_Flower_Shapla",
    "M_Stem_ReedGreen": "/Game/SparkVision/Materials/MI_Stem_ReedGreen.MI_Stem_ReedGreen",
    "M_Foliage_KashfulWhite": "/Game/SparkVision/Materials/MI_Foliage_KashfulWhite.MI_Foliage_KashfulWhite",
    "M_Decal_KrishnachuraPetals": "/Game/SparkVision/Materials/MI_Decal_KrishnachuraPetals.MI_Decal_KrishnachuraPetals",
}

ALL_MESHES = [
    # Curzon Modular
    "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Veranda_Arch_Lower.SM_Curzon_Veranda_Arch_Lower",
    "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Veranda_Arch_Upper.SM_Curzon_Veranda_Arch_Upper",
    "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Entrance_Portal.SM_Curzon_Entrance_Portal",
    "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Tower_Octagon.SM_Curzon_Tower_Octagon",
    "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Parapet_Merlons.SM_Curzon_Parapet_Merlons",
    "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Chattri_Dome.SM_Curzon_Chattri_Dome",
    "/Game/SparkVision/Campus/CurzonModular/SM_Curzon_Lamp_Colonial.SM_Curzon_Lamp_Colonial",
    # Environment & Botanical
    "/Game/SparkVision/Campus/Environment/SM_Tree_Banyan_Mature.SM_Tree_Banyan_Mature",
    "/Game/SparkVision/Campus/Environment/SM_Tree_Raintree_Avenue.SM_Tree_Raintree_Avenue",
    "/Game/SparkVision/Campus/Environment/SM_Tree_Krishnachura_Bloom.SM_Tree_Krishnachura_Bloom",
    "/Game/SparkVision/Campus/Environment/SM_Tree_Radhachura_Yellow.SM_Tree_Radhachura_Yellow",
    "/Game/SparkVision/Campus/Environment/SM_Tree_Jarul_Purple.SM_Tree_Jarul_Purple",
    "/Game/SparkVision/Campus/Environment/SM_Tree_Neem_Delicate.SM_Tree_Neem_Delicate",
    "/Game/SparkVision/Campus/Environment/SM_Tree_Palm_Coconut.SM_Tree_Palm_Coconut",
    "/Game/SparkVision/Campus/Environment/SM_Tree_Palm_BetelNut.SM_Tree_Palm_BetelNut",
    "/Game/SparkVision/Campus/Environment/SM_Cluster_Bamboo_Thicket.SM_Cluster_Bamboo_Thicket",
    "/Game/SparkVision/Campus/Environment/SM_Pond_WaterLily_Cluster.SM_Pond_WaterLily_Cluster",
    "/Game/SparkVision/Campus/Environment/SM_Plant_Reeds_Kashful.SM_Plant_Reeds_Kashful",
    "/Game/SparkVision/Campus/Environment/SM_Curzon_Pond_Ghat.SM_Curzon_Pond_Ghat",
    "/Game/SparkVision/Campus/Environment/SM_Decal_Petal_Scatter.SM_Decal_Petal_Scatter",
]

def run_mcp(toolset, tool, args):
    res = subprocess.check_output([
        "/Users/atiaoishi/Downloads/sparkvision/Scripts/mcp_client.py",
        "call", toolset, tool, json.dumps(args)
    ])
    return json.loads(res) if res.strip() else {}

print("=== Setting Material Slots on All Reconstructed Assets ===")
for mesh_ref in ALL_MESHES:
    short_name = mesh_ref.split(".")[-1]
    try:
        slots_res = run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "get_material_slots", {
            "mesh": {"refPath": mesh_ref}
        })
        slots = slots_res.get("returnValue", [])
        print(f"\nProcessing {short_name} (Slots: {slots}):")
        
        for slot_name in slots:
            # Match directly or by prefix
            mat_ref = MATERIAL_MAP.get(slot_name)
            if not mat_ref:
                # Try finding closest match
                for k, v in MATERIAL_MAP.items():
                    if k.lower() in slot_name.lower() or slot_name.lower() in k.lower():
                        mat_ref = v
                        break
            
            if mat_ref:
                set_res = run_mcp("editor_toolset.toolsets.static_mesh.StaticMeshTools", "set_material", {
                    "mesh": {"refPath": mesh_ref},
                    "slot_name": slot_name,
                    "material": {"refPath": mat_ref}
                })
                print(f"  [OK] '{slot_name}' -> {mat_ref}")
            else:
                print(f"  [WARN] No material mapping for '{slot_name}'")
    except Exception as e:
        print(f"Error on {short_name}: {e}")

print("\n=== All Material Slots Successfully Assigned! ===")
