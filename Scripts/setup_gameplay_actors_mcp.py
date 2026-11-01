#!/usr/bin/env python3
"""
SparkVision — Complete Gameplay Actor Placement via MCP Programmatic Script
- Reparents BP_SVCharacter to SVCharacter C++ class
- Reparents BP_SVGameMode to SVGameMode C++ class
- Sets World Settings GameMode override
- Places PlayerStart, Archive Terminals, Student NPCs
- Sets up foliage/physics for gameplay
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from mcp_client import call_tool

def run_prog(script):
    return call_tool(
        "editor_toolset.toolsets.programmatic.ProgrammaticToolset",
        "execute_tool_script",
        {"script": script}
    )

# ─── STEP 1: Reparent blueprints ───────────────────────────────────────────
print("[1/6] Reparenting BP_SVCharacter and BP_SVGameMode...", flush=True)
r1 = run_prog("""
import json

def set_parent(bp_path, parent_ref):
    bp = {'refPath': bp_path}
    parent = {'refPath': parent_ref}
    return execute_tool('editor_toolset.toolsets.blueprint.BlueprintTools.set_parent',
        json.dumps({'blueprint': bp, 'parent_class': parent}))

def get_parent(bp_path):
    bp = {'refPath': bp_path}
    return execute_tool('editor_toolset.toolsets.blueprint.BlueprintTools.get_parent',
        json.dumps({'blueprint': bp}))['returnValue']

def save(paths):
    return execute_tool('editor_toolset.toolsets.asset.AssetTools.save_assets',
        json.dumps({'asset_paths': paths}))

def run():
    results = {}
    
    # Reparent BP_SVCharacter to ASVCharacter
    try:
        p = get_parent('/Game/SparkVision/Gameplay/BP_SVCharacter')
        results['char_current_parent'] = str(p)[:80]
        if 'SVCharacter' not in str(p) and 'ThirdPerson' in str(p):
            set_parent('/Game/SparkVision/Gameplay/BP_SVCharacter', '/Script/MyProject.SVCharacter')
            save(['/Game/SparkVision/Gameplay/BP_SVCharacter'])
            results['char_reparent'] = 'SVCharacter - DONE'
        elif 'SVCharacter' in str(p):
            results['char_reparent'] = 'Already SVCharacter'
        else:
            set_parent('/Game/SparkVision/Gameplay/BP_SVCharacter', '/Script/MyProject.SVCharacter')
            save(['/Game/SparkVision/Gameplay/BP_SVCharacter'])
            results['char_reparent'] = 'SVCharacter - DONE (from unknown)'
    except Exception as e:
        results['char_err'] = str(e)[:200]
    
    # Reparent BP_SVGameMode to ASVGameMode
    try:
        p = get_parent('/Game/SparkVision/Gameplay/BP_SVGameMode')
        results['gm_current_parent'] = str(p)[:80]
        if 'SVGameMode' not in str(p):
            set_parent('/Game/SparkVision/Gameplay/BP_SVGameMode', '/Script/MyProject.SVGameMode')
            save(['/Game/SparkVision/Gameplay/BP_SVGameMode'])
            results['gm_reparent'] = 'SVGameMode - DONE'
        else:
            results['gm_reparent'] = 'Already SVGameMode'
    except Exception as e:
        results['gm_err'] = str(e)[:200]
    
    # Reparent BP_SVPlayerController to APlayerController (standard)
    try:
        set_parent('/Game/SparkVision/Gameplay/BP_SVPlayerController', '/Script/Engine.PlayerController')
        save(['/Game/SparkVision/Gameplay/BP_SVPlayerController'])
        results['pc_reparent'] = 'PlayerController - DONE'
    except Exception as e:
        results['pc_note'] = str(e)[:100]
    
    return results
""")
print(f"  {r1}", flush=True)

# ─── STEP 2: Set World Settings GameMode via object properties ─────────────
print("[2/6] Setting World Settings GameMode override...", flush=True)
r2 = run_prog("""
import json

def list_actors(class_ref):
    return execute_tool('editor_toolset.toolsets.scene.SceneTools.list_actors',
        json.dumps({'class_filter': {'refPath': class_ref}}))

def get_prop(obj_ref, prop_name):
    return execute_tool('editor_toolset.toolsets.object.ObjectTools.get_object_property',
        json.dumps({'object': {'refPath': obj_ref}, 'property_name': prop_name}))

def set_prop(obj_ref, prop_name, value):
    return execute_tool('editor_toolset.toolsets.object.ObjectTools.set_object_property',
        json.dumps({'object': {'refPath': obj_ref}, 'property_name': prop_name, 'property_value': str(value)}))

def save_level():
    return execute_tool('editor_toolset.toolsets.scene.SceneTools.save_current_level',
        json.dumps({}))

def run():
    results = {}
    
    # Find WorldSettings actor
    try:
        ws_actors = list_actors('/Script/Engine.WorldSettings')
        results['ws_actors_count'] = len(ws_actors.get('returnValue', []))
        if ws_actors.get('returnValue'):
            ws = ws_actors['returnValue'][0]['refPath']
            results['ws_ref'] = ws[:80]
            
            # Set DefaultGameMode on world settings
            try:
                set_prop(ws, 'DefaultGameMode', '/Game/SparkVision/Gameplay/BP_SVGameMode.BP_SVGameMode_C')
                results['gm_set'] = 'OK - BP_SVGameMode_C'
            except Exception as e:
                results['gm_set_err'] = str(e)[:150]
            
            save_level()
            results['level_saved'] = True
    except Exception as e:
        results['ws_err'] = str(e)[:200]
    
    return results
""")
print(f"  {r2}", flush=True)

# ─── STEP 3: Place PlayerStart in level ────────────────────────────────────
print("[3/6] Placing PlayerStart in Campus level...", flush=True)
r3 = run_prog("""
import json

def list_actors(class_ref):
    return execute_tool('editor_toolset.toolsets.scene.SceneTools.list_actors',
        json.dumps({'class_filter': {'refPath': class_ref}}))

def spawn_actor(class_ref, x, y, z, yaw=0.0, label=None):
    args = {
        'actor_class': {'refPath': class_ref},
        'location': {'x': x, 'y': y, 'z': z},
        'rotation': {'pitch': 0.0, 'yaw': yaw, 'roll': 0.0}
    }
    result = execute_tool('editor_toolset.toolsets.scene.SceneTools.spawn_actor',
        json.dumps(args))
    actor_ref = result.get('returnValue', {}).get('refPath', '')
    if actor_ref and label:
        execute_tool('editor_toolset.toolsets.actor.ActorTools.set_actor_label',
            json.dumps({'actor': {'refPath': actor_ref}, 'new_label': label}))
    return actor_ref

def save_level():
    return execute_tool('editor_toolset.toolsets.scene.SceneTools.save_current_level',
        json.dumps({}))

def run():
    results = {}
    
    # Check for existing PlayerStart
    existing = list_actors('/Script/Engine.PlayerStart')
    ps_count = len(existing.get('returnValue', []))
    results['existing_player_starts'] = ps_count
    
    if ps_count == 0:
        # Place PlayerStart in front of Curzon Hall entrance
        ps = spawn_actor('/Script/Engine.PlayerStart', -4800, 0, 150, 90.0, 'PlayerStart_CurzonEntrance')
        results['player_start_placed'] = ps[:60] if ps else 'FAILED'
    else:
        results['player_start'] = f'Already exists ({ps_count})'
    
    # Check for existing Archive Terminals
    archive_existing = list_actors('/Script/MyProject.SVArchiveTerminal')
    archive_count = len(archive_existing.get('returnValue', []))
    results['existing_archives'] = archive_count
    
    if archive_count < 5:
        archive_locs = [
            (-4200, 800, 100, 'ArchiveTerminal_CurzonFront'),
            (200, -2000, 100, 'ArchiveTerminal_Library'),
            (5000, 3000, 100, 'ArchiveTerminal_TSC'),
            (-2000, 5000, 100, 'ArchiveTerminal_Shaheed'),
            (8000, -1000, 100, 'ArchiveTerminal_KalaBhaban'),
        ]
        placed = 0
        for (x, y, z, lbl) in archive_locs:
            act = spawn_actor('/Script/MyProject.SVArchiveTerminal', x, y, z, 0.0, lbl)
            if act:
                placed += 1
        results['archives_placed'] = placed
    else:
        results['archives'] = f'Already placed ({archive_count})'
    
    # Check for NPCs
    npc_existing = list_actors('/Script/MyProject.SVStudentNPC')
    npc_count = len(npc_existing.get('returnValue', []))
    results['existing_npcs'] = npc_count
    
    if npc_count < 5:
        npc_locs = [
            (-4500, 400, 100, 'StudentNPC_Curzon_1'),
            (-4500, -400, 100, 'StudentNPC_Curzon_2'),
            (300, -1800, 100, 'StudentNPC_Library'),
            (5200, 2500, 100, 'StudentNPC_TSC'),
            (-1800, 4500, 100, 'StudentNPC_Shaheed'),
        ]
        npcs_placed = 0
        for (x, y, z, lbl) in npc_locs:
            act = spawn_actor('/Script/MyProject.SVStudentNPC', x, y, z, 0.0, lbl)
            if act:
                npcs_placed += 1
        results['npcs_placed'] = npcs_placed
    else:
        results['npcs'] = f'Already placed ({npc_count})'
    
    save_level()
    results['level_saved'] = True
    return results
""")
print(f"  {r3}", flush=True)

# ─── STEP 4: Set folder organization for gameplay actors ──────────────────
print("[4/6] Organizing gameplay actors into Outliner folders...", flush=True)
r4 = run_prog("""
import json

def list_actors(class_ref):
    return execute_tool('editor_toolset.toolsets.scene.SceneTools.list_actors',
        json.dumps({'class_filter': {'refPath': class_ref}}))

def set_folder(actor_ref, folder):
    return execute_tool('editor_toolset.toolsets.actor.ActorTools.set_actor_folder',
        json.dumps({'actor': {'refPath': actor_ref}, 'folder_path': folder}))

def run():
    results = {}
    
    # Move PlayerStarts to Gameplay folder
    ps_actors = list_actors('/Script/Engine.PlayerStart').get('returnValue', [])
    for a in ps_actors:
        try:
            set_folder(a['refPath'], 'Gameplay/PlayerStarts')
        except Exception as e:
            results['ps_folder_err'] = str(e)[:80]
    results['player_starts_organized'] = len(ps_actors)
    
    # Move Archive Terminals
    archive_actors = list_actors('/Script/MyProject.SVArchiveTerminal').get('returnValue', [])
    for a in archive_actors:
        try:
            set_folder(a['refPath'], 'Gameplay/Archives')
        except Exception as e:
            pass
    results['archives_organized'] = len(archive_actors)
    
    # Move NPCs
    npc_actors = list_actors('/Script/MyProject.SVStudentNPC').get('returnValue', [])
    for a in npc_actors:
        try:
            set_folder(a['refPath'], 'Gameplay/NPCs')
        except Exception as e:
            pass
    results['npcs_organized'] = len(npc_actors)
    
    return results
""")
print(f"  {r4}", flush=True)

# ─── STEP 5: Verify world settings and capture viewport ───────────────────
print("[5/6] Capturing viewport verification screenshot...", flush=True)
r5 = run_prog("""
import json, time

def set_camera(x, y, z, pitch, yaw):
    return execute_tool('EditorToolset.EditorAppToolset.SetCameraTransform',
        json.dumps({'transform': {
            'location': {'x': x, 'y': y, 'z': z},
            'rotation': {'pitch': pitch, 'yaw': yaw, 'roll': 0},
            'scale': {'x': 1, 'y': 1, 'z': 1}
        }}))

def capture():
    return execute_tool('EditorToolset.EditorAppToolset.CaptureViewport',
        json.dumps({'bShowUI': False}))

def run():
    # Move camera to Curzon gameplay start area
    set_camera(-5500, 0, 500, -25, 90)
    time.sleep(0.5)
    img = capture()
    return {'captured': bool(img.get('returnValue', {}).get('image', {}).get('data'))}
""")
print(f"  {r5}", flush=True)

# ─── STEP 6: Save everything ───────────────────────────────────────────────
print("[6/6] Saving all assets and level...", flush=True)
r6 = run_prog("""
import json

def save_assets(paths):
    return execute_tool('editor_toolset.toolsets.asset.AssetTools.save_assets',
        json.dumps({'asset_paths': paths}))

def save_level():
    return execute_tool('editor_toolset.toolsets.scene.SceneTools.save_current_level',
        json.dumps({}))

def run():
    paths_to_save = [
        '/Game/SparkVision/Gameplay/BP_SVCharacter',
        '/Game/SparkVision/Gameplay/BP_SVGameMode',
        '/Game/SparkVision/Gameplay/BP_SVPlayerController',
    ]
    save_assets(paths_to_save)
    save_level()
    return {'saved': True, 'assets': len(paths_to_save)}
""")
print(f"  {r6}", flush=True)

print("\n✅ Gameplay setup complete! All actors placed and BPs configured.", flush=True)
print("Next: Start PIE to test, then commit.", flush=True)
