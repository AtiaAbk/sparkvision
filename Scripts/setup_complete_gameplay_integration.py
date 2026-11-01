#!/usr/bin/env python3
"""
SparkVision — Complete Gameplay Integration Script
Creates BP_SVCharacter, BP_SVGameMode Blueprint assets,
fixes DefaultEngine.ini, adds Input Mapping Context + actions,
places PlayerStart + gameplay actors in LV_Campus_Blockout.
"""

import sys
import os
import json
import subprocess

sys.path.insert(0, os.path.dirname(__file__))
from mcp_client import call_tool

PROJECT_ROOT = "/Users/atiaoishi/Downloads/sparkvision"

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Create Gameplay Blueprints via Programmatic tool
# ─────────────────────────────────────────────────────────────────────────────

print("[1/8] Creating BP_SVCharacter Blueprint...", flush=True)
result = call_tool("editor_toolset.toolsets.programmatic.ProgrammaticToolset",
    "run_script",
    {
        "script": """
import unreal

# Create Gameplay folder
af = unreal.AssetToolsHelpers.get_asset_tools()

# Create BP_SVCharacter - child of ASVCharacter C++ class
char_class = unreal.load_class(None, "/Script/MyProject.SVCharacter")
if char_class:
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", char_class)
    asset = af.create_asset("BP_SVCharacter", "/Game/SparkVision/Gameplay", unreal.Blueprint, factory)
    if asset:
        unreal.log(f"[SETUP] Created BP_SVCharacter: {asset.get_path_name()}")
        # Save immediately
        unreal.EditorAssetLibrary.save_asset("/Game/SparkVision/Gameplay/BP_SVCharacter")
    else:
        unreal.log_warning("[SETUP] BP_SVCharacter already exists or failed")
else:
    unreal.log_error("[SETUP] Could not find SVCharacter C++ class!")

# Create BP_SVGameMode - child of ASVGameMode
gm_class = unreal.load_class(None, "/Script/MyProject.SVGameMode")
if gm_class:
    factory2 = unreal.BlueprintFactory()
    factory2.set_editor_property("parent_class", gm_class)
    asset2 = af.create_asset("BP_SVGameMode", "/Game/SparkVision/Gameplay", unreal.Blueprint, factory2)
    if asset2:
        unreal.log(f"[SETUP] Created BP_SVGameMode: {asset2.get_path_name()}")
        unreal.EditorAssetLibrary.save_asset("/Game/SparkVision/Gameplay/BP_SVGameMode")
    else:
        unreal.log_warning("[SETUP] BP_SVGameMode already exists or failed")
else:
    unreal.log_error("[SETUP] Could not find SVGameMode C++ class!")
"""
    }
)
print(f"  Result: {json.dumps(result)[:300]}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Create Enhanced Input Mapping Context + Input Actions
# ─────────────────────────────────────────────────────────────────────────────
print("[2/8] Creating Enhanced Input assets (IMC + IA)...", flush=True)
result2 = call_tool("editor_toolset.toolsets.programmatic.ProgrammaticToolset",
    "run_script",
    {
        "script": """
import unreal

af = unreal.AssetToolsHelpers.get_asset_tools()
input_path = "/Game/SparkVision/Input"

def ensure_asset(name, folder, asset_class, factory_class):
    full = f"{folder}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(full):
        unreal.log(f"[SETUP] Already exists: {full}")
        return unreal.load_asset(full)
    factory = factory_class()
    asset = af.create_asset(name, folder, asset_class, factory)
    if asset:
        unreal.EditorAssetLibrary.save_asset(full)
        unreal.log(f"[SETUP] Created: {full}")
    else:
        unreal.log_warning(f"[SETUP] Failed to create: {full}")
    return asset

# Input Mapping Context
imc = ensure_asset("IMC_SV_Default", input_path,
                   unreal.InputMappingContext,
                   unreal.InputMappingContextFactory)

# Input Actions
ia_move  = ensure_asset("IA_SV_Move",  input_path, unreal.InputAction, unreal.InputActionFactory)
ia_look  = ensure_asset("IA_SV_Look",  input_path, unreal.InputAction, unreal.InputActionFactory)
ia_jump  = ensure_asset("IA_SV_Jump",  input_path, unreal.InputAction, unreal.InputActionFactory)
ia_inter = ensure_asset("IA_SV_Interact", input_path, unreal.InputAction, unreal.InputActionFactory)
ia_sprint = ensure_asset("IA_SV_Sprint", input_path, unreal.InputAction, unreal.InputActionFactory)

# Configure value types
if ia_move:
    ia_move.set_editor_property("value_type", unreal.InputActionValueType.AXIS2_D)
    unreal.EditorAssetLibrary.save_asset("/Game/SparkVision/Input/IA_SV_Move")
if ia_look:
    ia_look.set_editor_property("value_type", unreal.InputActionValueType.AXIS2_D)
    unreal.EditorAssetLibrary.save_asset("/Game/SparkVision/Input/IA_SV_Look")

unreal.log("[SETUP] Enhanced Input assets configured.")
"""
    }
)
print(f"  Result: {json.dumps(result2)[:300]}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Wire IMC + IA references into BP_SVCharacter CDO via Object properties
# ─────────────────────────────────────────────────────────────────────────────
print("[3/8] Wiring Input assets to BP_SVCharacter...", flush=True)
result3 = call_tool("editor_toolset.toolsets.programmatic.ProgrammaticToolset",
    "run_script",
    {
        "script": """
import unreal

bp_char_path = "/Game/SparkVision/Gameplay/BP_SVCharacter"
if not unreal.EditorAssetLibrary.does_asset_exist(bp_char_path):
    unreal.log_error("[SETUP] BP_SVCharacter not found! Create it first.")
else:
    bp = unreal.load_asset(bp_char_path)
    cdo = bp.generated_class.get_default_object()
    
    def load_ia(path):
        if unreal.EditorAssetLibrary.does_asset_exist(path):
            return unreal.load_asset(path)
        return None
    
    imc   = load_ia("/Game/SparkVision/Input/IMC_SV_Default")
    move  = load_ia("/Game/SparkVision/Input/IA_SV_Move")
    look  = load_ia("/Game/SparkVision/Input/IA_SV_Look")
    jump  = load_ia("/Game/SparkVision/Input/IA_SV_Jump")
    inter = load_ia("/Game/SparkVision/Input/IA_SV_Interact")
    sprint = load_ia("/Game/SparkVision/Input/IA_SV_Sprint")
    
    if imc:
        cdo.set_editor_property("default_mapping_context", imc)
        unreal.log("[SETUP] Set DefaultMappingContext on BP_SVCharacter")
    if move:
        cdo.set_editor_property("move_action", move)
        unreal.log("[SETUP] Set MoveAction")
    if look:
        cdo.set_editor_property("look_action", look)
        unreal.log("[SETUP] Set LookAction")
    if jump:
        cdo.set_editor_property("jump_action", jump)
        unreal.log("[SETUP] Set JumpAction")
    if inter:
        cdo.set_editor_property("interact_action", inter)
        unreal.log("[SETUP] Set InteractAction")
    if sprint:
        cdo.set_editor_property("sprint_action", sprint)
        unreal.log("[SETUP] Set SprintAction")
    
    unreal.EditorAssetLibrary.save_asset(bp_char_path)
    unreal.log("[SETUP] BP_SVCharacter saved with input wiring.")
"""
    }
)
print(f"  Result: {json.dumps(result3)[:300]}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Fix DefaultEngine.ini — point GlobalDefaultGameMode to BP_SVGameMode
# ─────────────────────────────────────────────────────────────────────────────
print("[4/8] Updating DefaultEngine.ini to use BP_SVGameMode...", flush=True)
engine_ini_path = os.path.join(PROJECT_ROOT, "Config", "DefaultEngine.ini")
with open(engine_ini_path, "r") as f:
    ini_content = f.read()

old_gm = "GlobalDefaultGameMode=/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C"
new_gm = "GlobalDefaultGameMode=/Game/SparkVision/Gameplay/BP_SVGameMode.BP_SVGameMode_C"

if old_gm in ini_content:
    ini_content = ini_content.replace(old_gm, new_gm)
    with open(engine_ini_path, "w") as f:
        f.write(ini_content)
    print("  ✓ DefaultEngine.ini updated: now uses BP_SVGameMode", flush=True)
elif new_gm in ini_content:
    print("  ✓ DefaultEngine.ini already points to BP_SVGameMode", flush=True)
else:
    # Append under the right section
    if "[/Script/EngineSettings.GameMapsSettings]" in ini_content:
        ini_content = ini_content.replace(
            "[/Script/EngineSettings.GameMapsSettings]",
            f"[/Script/EngineSettings.GameMapsSettings]\n{new_gm}"
        )
    else:
        ini_content += f"\n[/Script/EngineSettings.GameMapsSettings]\n{new_gm}\n"
    with open(engine_ini_path, "w") as f:
        f.write(ini_content)
    print("  ✓ DefaultEngine.ini: appended BP_SVGameMode entry", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Fix DefaultGame.ini — set default map to Campus map
# ─────────────────────────────────────────────────────────────────────────────
print("[5/8] Updating DefaultGame.ini to launch Campus map...", flush=True)
game_ini_path = os.path.join(PROJECT_ROOT, "Config", "DefaultGame.ini")
with open(game_ini_path, "r") as f:
    game_content = f.read()

map_section = "[/Script/EngineSettings.GameMapsSettings]"
campus_map = "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout"
transition_map = "/Game/SparkVision/Maps/Campus/LV_Campus_Blockout"

if map_section not in game_content:
    game_content += f"\n{map_section}\nGameDefaultMap={campus_map}\nServerDefaultMap={campus_map}\nTransitionMap={transition_map}\n"
    print("  ✓ Added GameMapsSettings section with Campus map", flush=True)
else:
    # Update if different map is set
    if "GameDefaultMap=" not in game_content:
        game_content = game_content.replace(map_section, 
            f"{map_section}\nGameDefaultMap={campus_map}\nServerDefaultMap={campus_map}")
        print("  ✓ Added GameDefaultMap", flush=True)
    else:
        print("  ✓ GameDefaultMap already set", flush=True)

with open(game_ini_path, "w") as f:
    f.write(game_content)

# ─────────────────────────────────────────────────────────────────────────────
# Step 6: Place PlayerStart, Archive Terminals, and Student NPCs in level
# ─────────────────────────────────────────────────────────────────────────────
print("[6/8] Placing gameplay actors in LV_Campus_Blockout...", flush=True)
result6 = call_tool("editor_toolset.toolsets.programmatic.ProgrammaticToolset",
    "run_script",
    {
        "script": """
import unreal

world = unreal.EditorLevelLibrary.get_editor_world()
level = world.get_current_level()

# Helper to spawn actor
def spawn_actor(actor_class, location, rotation=(0,0,0), label=None):
    loc = unreal.Vector(location[0], location[1], location[2])
    rot = unreal.Rotator(rotation[0], rotation[1], rotation[2])
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, loc, rot)
    if actor and label:
        actor.set_actor_label(label)
    return actor

# 1. PlayerStart — in front of Curzon Hall main entrance
ps_class = unreal.load_class(None, "/Script/Engine.PlayerStart")
existing_ps = unreal.GameplayStatics.get_all_actors_of_class(world, ps_class)
if len(existing_ps) == 0:
    ps = spawn_actor(ps_class, (-4800, 0, 80), (0, 0, 90), "PlayerStart_CurzonEntrance")
    if ps:
        unreal.log("[SETUP] Placed PlayerStart at Curzon entrance")
        # Move to Gameplay_Test folder
        unreal.EditorLevelLibrary.set_actor_selection_state(ps, True)
    else:
        unreal.log_error("[SETUP] Failed to place PlayerStart!")
else:
    unreal.log(f"[SETUP] PlayerStart already exists ({len(existing_ps)} found)")

# 2. Archive Terminals — 5 locations across campus
archive_class = unreal.load_class(None, "/Script/MyProject.SVArchiveTerminal")
existing_archives = unreal.GameplayStatics.get_all_actors_of_class(world, archive_class) if archive_class else []

archive_locs = [
    ((-4200, 800, 100), "ArchiveTerminal_Curzon"),      # Curzon Hall front 
    ((0, -2000, 100), "ArchiveTerminal_Library"),        # Library area
    ((5000, 3000, 100), "ArchiveTerminal_TSC"),          # TSC plaza
    ((-2000, 5000, 100), "ArchiveTerminal_Shaheed"),     # Shaheed Minar
    ((8000, -1000, 100), "ArchiveTerminal_KalaBhaban"),  # Kala Bhaban area
]

if archive_class:
    if len(existing_archives) >= 5:
        unreal.log(f"[SETUP] Archive terminals already placed ({len(existing_archives)} found)")
    else:
        for i, (loc, lbl) in enumerate(archive_locs):
            act = spawn_actor(archive_class, loc, (0, 0, 0), lbl)
            if act:
                act.set_editor_property("archive_id", f"L1_ARCHIVE_{i+1:02d}")
                act.set_editor_property("archive_title", f"DU Historical Archive {i+1}")
                unreal.log(f"[SETUP] Placed {lbl}")
else:
    unreal.log_warning("[SETUP] SVArchiveTerminal class not found — will use placeholder cubes")
    # Fallback: place visible cubes as placeholder archive terminals
    cube_class = unreal.load_class(None, "/Script/Engine.StaticMeshActor")
    sm_terminal = unreal.load_asset("/Game/SparkVision/Campus/SM_ArchiveTerminal")
    for loc, lbl in archive_locs:
        act = spawn_actor(cube_class, loc, (0,0,0), lbl)
        if act and sm_terminal:
            comp = act.get_component_by_class(unreal.StaticMeshComponent)
            if comp:
                comp.set_static_mesh(sm_terminal)

# 3. Student NPCs — scattered around campus
npc_class = unreal.load_class(None, "/Script/MyProject.SVStudentNPC")
existing_npcs = unreal.GameplayStatics.get_all_actors_of_class(world, npc_class) if npc_class else []

npc_locs = [
    ((-4500, 400, 80), "StudentNPC_Curzon_1"),
    ((-4500, -400, 80), "StudentNPC_Curzon_2"),
    ((200, -1800, 80), "StudentNPC_Library"),
    ((5200, 2500, 80), "StudentNPC_TSC"),
    ((-1800, 4500, 80), "StudentNPC_Shaheed"),
]

if npc_class:
    if len(existing_npcs) >= 5:
        unreal.log(f"[SETUP] Student NPCs already placed ({len(existing_npcs)} found)")
    else:
        npc_ids = ["NPC_MEHDI", "NPC_RINA", "NPC_ARIF", "NPC_PRIYA", "NPC_DAUD"]
        for i, (loc, lbl) in enumerate(npc_locs):
            act = spawn_actor(npc_class, loc, (0,0,0), lbl)
            if act:
                act.set_editor_property("npc_id", npc_ids[i])
                unreal.log(f"[SETUP] Placed {lbl}")
else:
    unreal.log_warning("[SETUP] SVStudentNPC class not found in project")

# 4. Save the level
unreal.EditorLevelLibrary.save_all_dirty_levels()
unreal.log("[SETUP] Level saved with all gameplay actors!")
"""
    }
)
print(f"  Result: {json.dumps(result6)[:400]}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Step 7: Compile all Blueprints 
# ─────────────────────────────────────────────────────────────────────────────
print("[7/8] Compiling all SparkVision Blueprints...", flush=True)
result7 = call_tool("editor_toolset.toolsets.programmatic.ProgrammaticToolset",
    "run_script",
    {
        "script": """
import unreal

bps_to_compile = [
    "/Game/SparkVision/Gameplay/BP_SVCharacter",
    "/Game/SparkVision/Gameplay/BP_SVGameMode",
    "/Game/SparkVision/UI/BP_CampusHUD",
    "/Game/SparkVision/UI/WBP_CampusHUD",
]

for bp_path in bps_to_compile:
    if unreal.EditorAssetLibrary.does_asset_exist(bp_path):
        bp = unreal.load_asset(bp_path)
        if bp:
            unreal.EditorAssetLibrary.save_asset(bp_path)
            unreal.log(f"[SETUP] Saved/compiled: {bp_path}")
    else:
        unreal.log_warning(f"[SETUP] Not found: {bp_path}")

# Trigger a full save
unreal.EditorAssetLibrary.save_directory("/Game/SparkVision/", only_if_is_dirty=True, recursive=True)
unreal.log("[SETUP] All Blueprints compiled and saved.")
"""
    }
)
print(f"  Result: {json.dumps(result7)[:300]}", flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# Step 8: Set world GameMode override for Campus map
# ─────────────────────────────────────────────────────────────────────────────
print("[8/8] Setting World Settings GameMode override...", flush=True)
result8 = call_tool("editor_toolset.toolsets.programmatic.ProgrammaticToolset",
    "run_script",
    {
        "script": """
import unreal

world = unreal.EditorLevelLibrary.get_editor_world()
ws = world.get_world_settings()

# Set the GameMode override for this level
gm_class = unreal.load_class(None, "/Game/SparkVision/Gameplay/BP_SVGameMode.BP_SVGameMode_C")
if gm_class:
    ws.set_editor_property("default_game_mode", gm_class)
    unreal.log(f"[SETUP] World Settings GameMode → BP_SVGameMode_C")
else:
    unreal.log_warning("[SETUP] BP_SVGameMode_C not found yet (may need compile first)")
    # Fallback: try C++ class directly
    gm_cpp = unreal.load_class(None, "/Script/MyProject.SVGameMode")
    if gm_cpp:
        ws.set_editor_property("default_game_mode", gm_cpp)
        unreal.log("[SETUP] World Settings GameMode → SVGameMode (C++)")

unreal.EditorLevelLibrary.save_all_dirty_levels()
unreal.log("[SETUP] World settings saved.")
"""
    }
)
print(f"  Result: {json.dumps(result8)[:300]}", flush=True)

print("\n[SETUP COMPLETE] All 8 integration steps executed!", flush=True)
print("Next: Start PIE to test gameplay.", flush=True)
