#!/usr/bin/env python3
"""
Polish Cinematic Lighting and PostProcess Volume for Where Winds Meet standard:
- SkyLight: Warm bounce ambient fill (intensity 2.2) to eliminate black shadows under verandas
- DirectionalLight: Golden sunlight rays (intensity 5.0, volumetric scattering 2.5)
- ExponentialHeightFog: Volumetric golden haze & god rays
- PostProcessVolume: Cinematic bloom, vignette, warm contrast, and screen-space AO
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

def main():
    print("=" * 60)
    print("POLISHING CINEMATIC LIGHTING & POSTPROCESS FOR WWM")
    print("=" * 60)

    # 1. SkyLight
    print("\nTuning SkyLight...")
    sl_comp = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.SkyLight_UAID_F4A475FF15A3736A02_1961943709.SkyLightComponent0"
    try:
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": sl_comp},
            "values": json.dumps({
                "Intensity": 2.2,
                "LightColor": {"r": 1.0, "g": 0.96, "b": 0.90, "a": 1.0},
                "bRealTimeCapture": True
            })
        })
        print("  ✓ SkyLight set to warm ambient fill (2.2 intensity)")
    except Exception as e:
        print(f"  ✗ Error on SkyLight: {e}")

    # 2. DirectionalLight
    print("\nTuning DirectionalLight...")
    dl_comp = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.DirectionalLight_UAID_F4A475FF15A3736A02_1961932697.LightComponent0"
    try:
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": dl_comp},
            "values": json.dumps({
                "Intensity": 5.0,
                "LightColor": {"r": 1.0, "g": 0.94, "b": 0.86, "a": 1.0},
                "VolumetricScatteringIntensity": 2.5,
                "bAtmosphereSunLight": True,
                "AtmosphereSunLightIndex": 0
            })
        })
        print("  ✓ DirectionalLight set to warm golden sun (5.0 intensity, 2.5 volumetric)")
    except Exception as e:
        print(f"  ✗ Error on DirectionalLight: {e}")

    # 3. ExponentialHeightFog
    print("\nTuning ExponentialHeightFog...")
    fog_comp = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.ExponentialHeightFog_UAID_F4A475FF15A3736A02_1961936700.HeightFogComponent0"
    try:
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": fog_comp},
            "values": json.dumps({
                "bEnableVolumetricFog": True,
                "VolumetricFogScatteringDistribution": 0.68,
                "FogDensity": 0.012,
                "FogHeightFalloff": 0.005,
                "VolumetricFogDistance": 35000.0,
                "FogInscatteringColor": {"r": 1.0, "g": 0.92, "b": 0.80, "a": 1.0}
            })
        })
        print("  ✓ ExponentialHeightFog configured for volumetric god rays")
    except Exception as e:
        print(f"  ✗ Error on Fog: {e}")

    # 4. PostProcessVolume Settings
    print("\nTuning PostProcessVolume...")
    pp_actor = "/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus.LV_Level01_Compact_Campus:PersistentLevel.PostProcessVolume_UAID_F4A475FF15A3736A02_1961895679"
    try:
        pp_values = {
            "bUnbound": True,
            "settings": {
                "bOverride_BloomIntensity": True,
                "BloomIntensity": 0.75,
                "bOverride_BloomThreshold": True,
                "BloomThreshold": 0.85,
                "bOverride_VignetteIntensity": True,
                "VignetteIntensity": 0.25,
                "bOverride_AutoExposureBias": True,
                "AutoExposureBias": 0.30,
                "bOverride_ColorContrast": True,
                "ColorContrast": {"x": 1.05, "y": 1.05, "z": 1.05, "w": 1.0},
                "bOverride_ColorSaturation": True,
                "ColorSaturation": {"x": 1.08, "y": 1.08, "z": 1.05, "w": 1.0},
                "bOverride_WhiteTemp": True,
                "WhiteTemp": 6200.0,
                "bOverride_AmbientOcclusionIntensity": True,
                "AmbientOcclusionIntensity": 0.85,
                "bOverride_AmbientOcclusionRadius": True,
                "AmbientOcclusionRadius": 220.0
            }
        }
        invoke_tool("set_properties", "editor_toolset.toolsets.object.ObjectTools", {
            "instance": {"refPath": pp_actor},
            "values": json.dumps(pp_values)
        })
        print("  ✓ PostProcessVolume tuned for warm cinematic filmic look")
    except Exception as e:
        print(f"  ✗ Error on PostProcess: {e}")

    # 5. Save Level
    print("\nSaving level...")
    try:
        invoke_tool("save_assets", "editor_toolset.toolsets.asset.AssetTools", {
            "asset_paths": ["/Game/SparkVision/Maps/Level01/LV_Level01_Compact_Campus"]
        })
        print("  ✓ Level saved successfully!")
    except Exception as e:
        print(f"  Notice saving: {e}")

    print("\n✅ Cinematic lighting & post-processing complete!")

if __name__ == "__main__":
    main()
