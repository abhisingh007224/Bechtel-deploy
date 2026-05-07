from mcp.server.fastmcp import FastMCP
import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "community.db")

# Create MCP server
mcp = FastMCP("bechtel Chatters")

@mcp.tool()
def get_top_chatters():
    """Retrieve the top chatters sorted by number of messages."""

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, messages
            FROM chatters
            ORDER BY messages DESC
        """)

        results = cursor.fetchall()
        conn.close()

        return [
            {"name": name, "messages": messages}
            for name, messages in results
        ]

    except Exception as e:
        return {"error": str(e)}

# MCP app as ASGI app
app = mcp.streamable_http_app()
