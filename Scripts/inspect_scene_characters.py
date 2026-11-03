import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_client import invoke_tool

all_actors = invoke_tool("find_actors", "editor_toolset.toolsets.scene.SceneTools", {"name": "", "tag": "", "collision_channels": []}).get("returnValue", [])
print(f"Total scene actors: {len(all_actors)}")

categories = {"Student": [], "Hostile": [], "Police": [], "Security": [], "Teacher": [], "Staff": [], "Character": []}

for a in all_actors:
    lbl = invoke_tool("get_label", "editor_toolset.toolsets.actor.ActorTools", {"actor": a}).get("returnValue", "")
    for cat in categories:
        if cat.lower() in lbl.lower():
            categories[cat].append((lbl, a["refPath"]))
            break

for cat, actors in categories.items():
    print(f"\n[{cat}] ({len(actors)} actors):")
    for lbl, ref in actors[:5]:
        print(f"  - {lbl}")
    if len(actors) > 5:
        print(f"  ... and {len(actors) - 5} more")
