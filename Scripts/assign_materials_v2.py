#!/usr/bin/env python3
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

BARK_MAT = "/Game/SparkVision/Materials/MI_Bark_Natural_Gnarled.MI_Bark_Natural_Gnarled"
RAINTREE_MAT = "/Game/SparkVision/Materials/MI_Foliage_Raintree_Natural.MI_Foliage_Raintree_Natural"
BANYAN_MAT = "/Game/SparkVision/Materials/MI_Foliage_Banyan_Natural.MI_Foliage_Banyan_Natural"
KRISHNA_MAT = "/Game/SparkVision/Materials/MI_Foliage_Krishnachura_Natural.MI_Foliage_Krishnachura_Natural"
FERN_MAT = "/Game/SparkVision/Materials/MI_Foliage_Fern_Natural.MI_Foliage_Fern_Natural"

assignments = [
    ("/Game/SparkVision/Campus/Environment/SM_Natural_Raintree_Grand.SM_Natural_Raintree_Grand", [
        ("M_Bark_Natural_Gnarled", BARK_MAT),
        ("M_Foliage_Natural_Leaf", RAINTREE_MAT)
    ]),
    ("/Game/SparkVision/Campus/Environment/SM_Natural_Banyan_Heritage.SM_Natural_Banyan_Heritage", [
        ("M_Bark_Natural_Gnarled", BARK_MAT),
        ("M_Foliage_Banyan_Natural", BANYAN_MAT)
    ]),
    ("/Game/SparkVision/Campus/Environment/SM_Natural_Krishnachura_Bloom.SM_Natural_Krishnachura_Bloom", [
        ("M_Bark_Natural_Gnarled", BARK_MAT),
        ("M_Foliage_Krishnachura_Natural", KRISHNA_MAT)
    ]),
    ("/Game/SparkVision/Campus/Environment/SM_Natural_Fern_Cluster.SM_Natural_Fern_Cluster", [
        ("M_Foliage_Fern_Natural", FERN_MAT)
    ])
]

for mesh_ref, slots in assignments:
    mesh_name = mesh_ref.split(".")[-1]
    print(f"\nAssigning materials for {mesh_name}...")
    for slot_name, mat_ref in slots:
        try:
            res = invoke_tool("set_material", "editor_toolset.toolsets.static_mesh.StaticMeshTools", {
                "mesh": {"refPath": mesh_ref},
                "slot_name": slot_name,
                "material": {"refPath": mat_ref}
            })
            print(f"  ✓ {slot_name} -> {mat_ref.split('.')[-1]}")
        except Exception as e:
            print(f"  ✗ {slot_name} error: {e}")

    # Save
    asset_path = mesh_ref.split(".")[0]
    invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
        "asset_paths": [asset_path]
    })
    print(f"  ✓ Saved {mesh_name}")

print("\n✅ All static mesh material slots assigned!")
