#!/usr/bin/env python3
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

script = '''
import json

def run():
    # 1. Delete all CurzonPond_Jarul_* actors that are sitting at (0, 0, 0)
    jarul_acts = execute_tool('editor_toolset.toolsets.scene.SceneTools.find_actors', json.dumps({
        'name': 'CurzonPond_Jarul', 'tag': '', 'collision_channels': []
    }))['returnValue']
    
    deleted_jarul = 0
    for a in jarul_acts:
        execute_tool('editor_toolset.toolsets.scene.SceneTools.remove_from_scene', json.dumps({
            'actor': {'refPath': a['refPath']}
        }))
        deleted_jarul += 1

    # 2. Adjust DirectionalLight to illuminate the Curzon Hall facade directly
    # Curzon Hall faces +X. Light pointing with Yaw = -140 (or 220) shines toward -X, -Y,
    # striking Curzon Hall's front facade at a classic 40-degree architectural angle.
    dir_lights = execute_tool('editor_toolset.toolsets.scene.SceneTools.find_actors', json.dumps({
        'name': 'DirectionalLight', 'tag': '', 'collision_channels': []
    }))['returnValue']
    
    dir_updated = False
    for a in dir_lights:
        ref = a['refPath']
        execute_tool('editor_toolset.toolsets.actor.ActorTools.set_actor_transform', json.dumps({
            'actor': {'refPath': ref},
            'xform': {
                'rotation': {'pitch': -36.0, 'yaw': -140.0, 'roll': 0.0}
            }
        }))
        # Also adjust component properties
        comps = execute_tool('editor_toolset.toolsets.actor.ActorTools.get_components', json.dumps({
            'actor': {'refPath': ref}
        }))['returnValue']
        for c in comps:
            if 'DirectionalLightComponent' in c['refPath']:
                execute_tool('editor_toolset.toolsets.object.ObjectTools.set_properties', json.dumps({
                    'instance': {'refPath': c['refPath']},
                    'values': json.dumps({
                        'Intensity': 85000.0,
                        'bUseTemperature': True,
                        'Temperature': 5800.0,
                        'bAtmosphereSunLight': True,
                        'CastShadows': True
                    })
                }))
                dir_updated = True
                break

    # 3. Adjust SkyLight for vibrant ambient daylight fill
    sky_lights = execute_tool('editor_toolset.toolsets.scene.SceneTools.find_actors', json.dumps({
        'name': 'SkyLight', 'tag': '', 'collision_channels': []
    }))['returnValue']
    
    sky_updated = False
    for a in sky_lights:
        ref = a['refPath']
        comps = execute_tool('editor_toolset.toolsets.actor.ActorTools.get_components', json.dumps({
            'actor': {'refPath': ref}
        }))['returnValue']
        for c in comps:
            if 'SkyLightComponent' in c['refPath']:
                execute_tool('editor_toolset.toolsets.object.ObjectTools.set_properties', json.dumps({
                    'instance': {'refPath': c['refPath']},
                    'values': json.dumps({
                        'Intensity': 2.0,
                        'bRealTimeCapture': True
                    })
                }))
                sky_updated = True
                break

    # 4. Adjust Fog for crystal clear daylight
    fogs = execute_tool('editor_toolset.toolsets.scene.SceneTools.find_actors', json.dumps({
        'name': 'ExponentialHeightFog', 'tag': '', 'collision_channels': []
    }))['returnValue']
    
    fog_updated = False
    for a in fogs:
        ref = a['refPath']
        comps = execute_tool('editor_toolset.toolsets.actor.ActorTools.get_components', json.dumps({
            'actor': {'refPath': ref}
        }))['returnValue']
        for c in comps:
            if 'ExponentialHeightFogComponent' in c['refPath']:
                execute_tool('editor_toolset.toolsets.object.ObjectTools.set_properties', json.dumps({
                    'instance': {'refPath': c['refPath']},
                    'values': json.dumps({
                        'fogDensity': 0.00008,
                        'startDistance': 4000.0,
                        'bEnableVolumetricFog': False
                    })
                }))
                fog_updated = True
                break

    return {
        'deleted_jarul': deleted_jarul,
        'dir_updated': dir_updated,
        'sky_updated': sky_updated,
        'fog_updated': fog_updated
    }
'''

def main():
    print("Executing natural lighting and cleanup...")
    res = invoke_tool("execute_tool_script", "editor_toolset.toolsets.programmatic.ProgrammaticToolset", {
        "script": script
    })
    print("Result:", res.get("returnValue", ""))

if __name__ == "__main__":
    main()
