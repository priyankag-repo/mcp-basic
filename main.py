# main.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")  # Tool container / server

@mcp.tool()
def calculate_sum(items: str) -> str:
    total = 0
    for part in items.split(","):
        if "x" in part:
            q, p = part.split("x")
            total += float(q.strip()) * float(p.strip())
    return f"{total:.2f}"

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    print("Starting MCP Calculator Server...")
    mcp.run()  # <-- this is the correct method in v1.16.0
