#!/bin/bash
nohup "/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor" "/Users/atiaoishi/Downloads/sparkvision/MyProject.uproject" > /tmp/unreal_editor.log 2>&1 &
echo "PID: $!"
