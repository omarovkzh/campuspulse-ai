"""Same tools exposed as an MCP server (FastMCP).

Run locally:   python mcp_server/server.py
Cloud Run:     see README (container start command is the same).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP

from campuspulse.tools import calc_priority, check_repo_activity, get_deadlines

mcp = FastMCP("campuspulse-tools")
mcp.tool(get_deadlines)
mcp.tool(calc_priority)
mcp.tool(check_repo_activity)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
