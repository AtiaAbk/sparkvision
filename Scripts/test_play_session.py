import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcp_client

print("Attempting to connect to Unreal MCP...")
try:
    pie = mcp_client.invoke_tool("IsPIERunning", "EditorToolset.EditorAppToolset", {})
    print("Editor MCP is alive! IsPIERunning:", pie)
except Exception as e:
    print("Editor MCP is not reachable yet:", e)
