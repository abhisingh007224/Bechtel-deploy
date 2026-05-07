from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
import sqlite3
import os

# FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "MCP Server Running"}

# Health endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "community.db")

# MCP server
mcp = FastMCP("bechtel Chatters")

# MCP Tool
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

# Run MCP server
if __name__ == '__main__':
    print(f"Using database at: {DB_PATH}")

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )
