#!/bin/bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPROJECT="$PROJECT_ROOT/MyProject.uproject"
UE_BIN="/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"

echo "=== LAUNCHING SPARKVISION IN STANDALONE GAME MODE (-game) ==="
"$UE_BIN" "$UPROJECT" -game -windowed -ResX=1280 -ResY=720 -log -NoZen -NoZenAutoLaunch > /tmp/sparkvision_game.log 2>&1 &
GAME_PID=$!
echo "Game started with PID: $GAME_PID"

echo "Monitoring for 15 seconds..."
for i in {1..15}; do
    if ! ps -p $GAME_PID > /dev/null; then
        echo "Game process exited unexpectedly at second $i!"
        break
    fi
    sleep 1
done

echo "Process status:"
ps -o pid,rss,%mem,%cpu,command -p $GAME_PID || echo "Process not running"

echo "Log tail:"
tail -n 25 /tmp/sparkvision_game.log

echo "Killing test game instance..."
kill -9 $GAME_PID 2>/dev/null || true
echo "Done."
