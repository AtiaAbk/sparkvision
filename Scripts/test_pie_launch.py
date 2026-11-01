#!/usr/bin/env python3
"""
SparkVision — PIE Launch Test + Screenshot Capture
Runs Play-In-Editor, captures verification screenshots, stops PIE.
"""

import sys, os, json, time, base64
sys.path.insert(0, os.path.dirname(__file__))
from mcp_client import call_tool

ARTIFACT_DIR = "/Users/atiaoishi/.gemini/antigravity/brain/e20fce03-5cdc-4c76-8f10-f79efc005a90"
SCREENSHOTS_DIR = "/Users/atiaoishi/Downloads/sparkvision/Documentation/WorldEnvironment/Screenshots/Gameplay"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def run_prog(script):
    return call_tool(
        "editor_toolset.toolsets.programmatic.ProgrammaticToolset",
        "execute_tool_script",
        {"script": script}
    )

def save_image(b64_data, filename):
    data = base64.b64decode(b64_data)
    path = os.path.join(SCREENSHOTS_DIR, filename)
    with open(path, "wb") as f:
        f.write(data)
    # Also save to artifact dir
    art_path = os.path.join(ARTIFACT_DIR, filename)
    with open(art_path, "wb") as f:
        f.write(data)
    return path

# ─── Check PIE not already running ─────────────────────────────────────────
print("[1/5] Checking PIE state...", flush=True)
pie_check = run_prog("""
import json
def is_pie():
    return execute_tool('EditorToolset.EditorAppToolset.IsPIERunning', json.dumps({}))['returnValue']
def run():
    return {'pie_running': is_pie()}
""")
print(f"  PIE state: {pie_check}", flush=True)

pie_val = json.loads(pie_check.get('returnValue', '{"pie_running": false}'))
if pie_val.get('pie_running'):
    print("  Stopping existing PIE session...", flush=True)
    run_prog("""
import json
def run():
    execute_tool('EditorToolset.EditorAppToolset.StopPIE', json.dumps({}))
    return {'stopped': True}
""")
    time.sleep(2)

# ─── Start PIE ─────────────────────────────────────────────────────────────
print("[2/5] Starting Play-In-Editor session...", flush=True)
pie_result = run_prog("""
import json

def run():
    options = {
        'bSimulate': False,
        'playMode': 'PlayMode_InViewPort',
        'warmupSeconds': 3.0
    }
    try:
        execute_tool('EditorToolset.EditorAppToolset.StartPIE',
            json.dumps({'options': options}))
        return {'pie_started': True}
    except Exception as e:
        return {'pie_started': False, 'error': str(e)[:200]}
""")
print(f"  PIE start: {pie_result}", flush=True)

time.sleep(4)

# ─── Capture gameplay screenshots ─────────────────────────────────────────
print("[3/5] Capturing gameplay verification screenshots...", flush=True)
cap_result = run_prog("""
import json, time

def capture():
    return execute_tool('EditorToolset.EditorAppToolset.CaptureViewport',
        json.dumps({'bShowUI': True}))

def run():
    time.sleep(1)
    img_data = capture()
    img = img_data.get('returnValue', {})
    has_image = bool(img.get('image', {}).get('data'))
    cam = img.get('cameraLocation', {})
    return {
        'has_image': has_image,
        'image_data': img.get('image', {}).get('data', '')[:50] + '...' if has_image else '',
        'camera': f"({cam.get('x',0):.0f}, {cam.get('y',0):.0f}, {cam.get('z',0):.0f})",
        'full_data': img.get('image', {}).get('data', '') if has_image else ''
    }
""")

cap_val = json.loads(cap_result.get('returnValue', '{}'))
if cap_val.get('full_data'):
    save_image(cap_val['full_data'], "PIE_GAMEPLAY_LAUNCH_TEST.png")
    print(f"  ✓ Screenshot saved — camera at {cap_val.get('camera')}", flush=True)
else:
    print(f"  Screenshot capture: {cap_result}", flush=True)

time.sleep(3)

# ─── Verify gameplay systems in PIE ────────────────────────────────────────
print("[4/5] Verifying gameplay systems in PIE...", flush=True)
verify_result = run_prog("""
import json

def list_actors(class_ref):
    return execute_tool('editor_toolset.toolsets.scene.SceneTools.list_actors',
        json.dumps({'class_filter': {'refPath': class_ref}}))

def is_pie():
    return execute_tool('EditorToolset.EditorAppToolset.IsPIERunning', json.dumps({}))['returnValue']

def run():
    results = {}
    results['pie_active'] = is_pie()
    
    # Check for Character in world
    chars = list_actors('/Script/MyProject.SVCharacter')
    results['sv_characters'] = len(chars.get('returnValue', []))
    
    # Check for Archive Terminals
    archives = list_actors('/Script/MyProject.SVArchiveTerminal')
    results['archive_terminals'] = len(archives.get('returnValue', []))
    
    # Check for Student NPCs
    npcs = list_actors('/Script/MyProject.SVStudentNPC')
    results['student_npcs'] = len(npcs.get('returnValue', []))
    
    # Check for GameMode
    gm = list_actors('/Script/MyProject.SVGameMode')
    results['sv_game_mode'] = len(gm.get('returnValue', []))
    
    return results
""")
print(f"  Verification: {verify_result}", flush=True)

# ─── Stop PIE ─────────────────────────────────────────────────────────────
print("[5/5] Stopping PIE session...", flush=True)
stop_result = run_prog("""
import json
def run():
    try:
        execute_tool('EditorToolset.EditorAppToolset.StopPIE', json.dumps({}))
        return {'stopped': True}
    except Exception as e:
        return {'stopped': False, 'note': str(e)[:100]}
""")
print(f"  PIE stopped: {stop_result}", flush=True)

print("\n✅ PIE gameplay test complete!", flush=True)
