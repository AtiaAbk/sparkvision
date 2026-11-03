#!/bin/bash
set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPROJECT="$PROJECT_ROOT/MyProject.uproject"
UBT="/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/Mac/Build.sh"

echo "Building MyProjectEditor Mac Development..."
"$UBT" MyProjectEditor Mac Development -Project="$UPROJECT"
echo "Build succeeded!"
