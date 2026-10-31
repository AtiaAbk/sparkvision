#!/bin/bash
# Start SparkVision Java Mission Control Server
export JAVA_HOME="/opt/homebrew/Cellar/openjdk@21/21.0.12.1/libexec/openjdk.jdk/Contents/Home"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR/JavaMissionControl"
echo "[MissionControl] Starting Java Mission Control on port 8080..."
./gradlew run --console=plain
