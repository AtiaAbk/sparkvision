#!/usr/bin/env python3
import http.server
import json
import urllib.request
import urllib.error
import sys

UNREAL_URL = "http://127.0.0.1:8000/mcp"
current_unreal_session = None

def get_valid_unreal_session():
    global current_unreal_session
    init_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "unreal-mcp-proxy", "version": "1.0"}
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
        current_unreal_session = sid
        init_body = resp.read()
        
    # Send notifications/initialized
    notif_payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }).encode("utf-8")
    notif_req = urllib.request.Request(
        UNREAL_URL,
        data=notif_payload,
        headers={"Content-Type": "application/json", "Mcp-Session-Id": current_unreal_session}
    )
    try:
        with urllib.request.urlopen(notif_req) as notif_resp:
            notif_resp.read()
    except Exception as e:
        pass
        
    print(f"[Proxy] Initialized new Unreal session: {current_unreal_session}", flush=True)
    return current_unreal_session, init_body

class MCPProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Unreal MCP Proxy Active")

    def do_POST(self):
        global current_unreal_session
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            req_json = json.loads(body.decode("utf-8"))
        except Exception:
            req_json = {}

        method = req_json.get("method", "")

        # If it's an initialize call, get fresh session
        if method == "initialize":
            sid, init_body = get_valid_unreal_session()
            self.send_response(200)
            self.send_header("Content-Type", "application/json;charset=utf-8")
            self.send_header("Mcp-Session-Id", sid)
            self.end_headers()
            self.wfile.write(init_body)
            return

        if not current_unreal_session:
            get_valid_unreal_session()

        # Forward request to Unreal
        for attempt in range(2):
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "Mcp-Session-Id": current_unreal_session
            }
            req = urllib.request.Request(UNREAL_URL, data=body, headers=headers)
            try:
                with urllib.request.urlopen(req) as resp:
                    resp_body = resp.read()
                    self.send_response(resp.status)
                    for k, v in resp.headers.items():
                        if k.lower() in ["content-type", "mcp-session-id"]:
                            self.send_header(k, v)
                    self.end_headers()
                    self.wfile.write(resp_body)
                    return
            except urllib.error.HTTPError as e:
                err_body = e.read()
                # Check if session expired
                if e.code == 404 and b"Unknown session id" in err_body and attempt == 0:
                    print(f"[Proxy] Session {current_unreal_session} expired. Re-initializing...", flush=True)
                    get_valid_unreal_session()
                    continue
                else:
                    self.send_response(e.code)
                    self.send_header("Content-Type", "application/json;charset=utf-8")
                    self.end_headers()
                    self.wfile.write(err_body)
                    return
            except Exception as ex:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(ex)}).encode("utf-8"))
                return

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    server = http.server.HTTPServer(("127.0.0.1", port), MCPProxyHandler)
    print(f"[Proxy] Running on http://127.0.0.1:{port}/mcp -> {UNREAL_URL}", flush=True)
    server.serve_forever()
