#!/bin/bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPROJECT="$PROJECT_ROOT/MyProject.uproject"
UE_BIN="/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"

echo "Launching SparkVision standalone gameplay (Out-of-Editor / Game Mode)..."
"$UE_BIN" "$UPROJECT" -game -windowed -ResX=1280 -ResY=720 -log -NoZen -NoZenAutoLaunch
