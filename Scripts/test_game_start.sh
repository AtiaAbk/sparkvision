#!/bin/bash
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPROJECT="$PROJECT_ROOT/MyProject.uproject"
UE_BIN="/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"

echo "=== LAUNCHING SPARKVISION IN STANDALONE GAME MODE (-game) FOR 40 SECONDS ==="
"$UE_BIN" "$UPROJECT" -game -windowed -ResX=1280 -ResY=720 -log -NoZen -NoZenAutoLaunch > /tmp/sparkvision_game.log 2>&1 &
GAME_PID=$!
echo "Game started with PID: $GAME_PID"

for i in {1..40}; do
    if ! ps -p $GAME_PID > /dev/null; then
        echo "Process exited at second $i"
        break
    fi
    sleep 1
    if [ $((i % 10)) -eq 0 ]; then
        ps -o pid,rss,%mem,%cpu -p $GAME_PID
    fi
done

echo "Final Process status:"
ps -o pid,rss,%mem,%cpu,command -p $GAME_PID || echo "Process not running"

echo "Log tail:"
tail -n 30 /tmp/sparkvision_game.log

kill -9 $GAME_PID 2>/dev/null || true
