"""Minimal client for the BeamNG in-game MCP server (Streamable HTTP, JSON-RPC 2.0).

Only wraps the protocol; every capability used here is an existing server tool
(see docs/BEAMNG_MCP_CAPABILITIES.md). Standard library only.
"""
import json
import time
import urllib.request

DEFAULT_URL = "http://127.0.0.1:29292/mcp"


class MCPError(RuntimeError):
    pass


class BeamNGMCP:
    def __init__(self, url=DEFAULT_URL, timeout=120):
        self.url = url
        self.timeout = timeout
        self.session_id = None
        self._next_id = 1
        self._rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                 "clientInfo": {"name": "qa_runner", "version": "1"}})
        self._rpc("notifications/initialized", notify=True)

    def _rpc(self, method, params=None, notify=False):
        body = {"jsonrpc": "2.0", "method": method}
        if not notify:
            body["id"] = self._next_id
            self._next_id += 1
        if params is not None:
            body["params"] = params
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        req = urllib.request.Request(self.url, json.dumps(body).encode(), headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            self.session_id = r.headers.get("Mcp-Session-Id") or self.session_id
            text = r.read().decode("utf-8", "replace")
        if not text:
            return None
        if text.startswith(("event:", "data:")):
            text = [l[5:] for l in text.splitlines() if l.startswith("data:")][-1]
        msg = json.loads(text, strict=False)  # game logs may carry raw control characters
        if "error" in msg:
            raise MCPError(f"{method}: {msg['error']}")
        return msg.get("result")

    def call(self, tool, **args):
        """Call a server tool and return its text content (str)."""
        result = self._rpc("tools/call", {"name": tool, "arguments": args})
        parts = [c.get("text", "") for c in (result or {}).get("content", []) if c.get("type") == "text"]
        text = "\n".join(parts)
        if (result or {}).get("isError"):
            raise MCPError(f"{tool}: {text}")
        return text

    def call_json(self, tool, **args):
        return json.loads(self.call(tool, **args))

    def lua(self, code):
        """Run GE Lua; returns tostring() of the result. Raises on compile/runtime errors."""
        out = self.call("run_lua", code=code)
        if out.startswith(("compile error", "runtime error", "error")):
            raise MCPError(f"run_lua: {out}")
        return out

    def list_tools(self):
        return self._rpc("tools/list", {})["tools"]


def wait_for_file(path, timeout=30, stable_for=0.5):
    """The screenshot tool returns the path before the file is written: wait until it exists and stops growing."""
    import os
    deadline = time.time() + timeout
    last = -1
    while time.time() < deadline:
        if os.path.exists(path):
            size = os.path.getsize(path)
            if size > 0 and size == last:
                return size
            last = size
        time.sleep(stable_for)
    raise TimeoutError(f"screenshot not written: {path}")
