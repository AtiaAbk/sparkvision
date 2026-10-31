#!/usr/bin/env python3
import sys
import os
import json
import urllib.request
import urllib.error

UNREAL_URL = "http://127.0.0.1:8000/mcp"
SESSION_FILE = "/tmp/unreal_mcp_session.txt"

def get_session_id(force_new=False):
    if not force_new and os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                sid = f.read().strip()
                if sid:
                    return sid
        except Exception:
            pass

    init_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "sparkvision-direct-mcp", "version": "1.0"}
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        UNREAL_URL,
        data=init_payload,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    )
    with urllib.request.urlopen(req) as resp:
        sid = None
        for k, v in resp.headers.items():
            if k.lower() == "mcp-session-id":
                sid = v
                break
        if not sid:
            raise RuntimeError("No Mcp-Session-Id received from Unreal MCP server")

    # Send notifications/initialized
    notif_payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }).encode("utf-8")
    notif_req = urllib.request.Request(
        UNREAL_URL,
        data=notif_payload,
        headers={"Content-Type": "application/json", "Mcp-Session-Id": sid}
    )
    try:
        with urllib.request.urlopen(notif_req) as notif_resp:
            notif_resp.read()
    except Exception:
        pass

    with open(SESSION_FILE, "w") as f:
        f.write(sid)
    return sid

def post_mcp(method, params, id_val=1):
    for attempt in range(2):
        sid = get_session_id(force_new=(attempt > 0))
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": id_val,
            "method": method,
            "params": params
        }).encode("utf-8")
        req = urllib.request.Request(
            UNREAL_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Session-Id": sid
            }
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "error" in data:
                    err_msg = str(data["error"])
                    if "Unknown session id" in err_msg and attempt == 0:
                        continue
                    raise RuntimeError(f"MCP RPC Error: {err_msg}")
                return data.get("result", {})
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            if e.code == 404 and "Unknown session id" in err_body and attempt == 0:
                continue
            raise RuntimeError(f"HTTP {e.code}: {err_body}")

def call_tool(tool_name, toolset_name=None, arguments=None):
    if arguments is None:
        arguments = {}
    params = {
        "name": "call_tool",
        "arguments": {
            "tool_name": tool_name,
            "arguments": arguments
        }
    }
    if toolset_name:
        params["arguments"]["toolset_name"] = toolset_name

    res = post_mcp("tools/call", params)
    if res.get("isError"):
        msg = res.get("content", [{}])[0].get("text", "Unknown tool error")
        print(f"TOOL_ERROR: {msg}", file=sys.stderr)
        sys.exit(1)
    content = res.get("content", [])
    if content:
        print(content[0].get("text", ""))

def list_toolsets():
    res = post_mcp("tools/call", {"name": "list_toolsets", "arguments": {}})
    content = res.get("content", [])
    if content:
        print(content[0].get("text", ""))

def describe_toolset(name):
    res = post_mcp("tools/call", {"name": "describe_toolset", "arguments": {"toolset_name": name}})
    content = res.get("content", [])
    if content:
        print(content[0].get("text", ""))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mcp_client.py <command> [args...]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "list_toolsets":
        list_toolsets()
    elif cmd == "describe_toolset":
        describe_toolset(sys.argv[2])
    elif cmd == "call":
        toolset = sys.argv[2]
        tool = sys.argv[3]
        args = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
        call_tool(tool, toolset, args)
