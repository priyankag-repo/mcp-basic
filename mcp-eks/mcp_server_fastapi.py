# mcp_server_fastapi.py
from fastapi import FastAPI
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Calculator")

# MCP tool: calculate_sum
@mcp.tool()
def calculate_sum(items: str) -> str:
    """
    Calculate total from a string like '2 x 10, 3 x 20'
    """
    try:
        total = sum(
            float(q.strip()) * float(p.strip())
            for part in items.split(",") if "x" in part
            for q, p in [part.split("x")]
        )
        return f"{total:.2f}"
    except Exception as e:
        return f"ERROR: {e}"

# FastAPI app
app = FastAPI(title="MCP Calculator Server")

# Health check endpoint
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# Endpoint for calculate_sum tool
class CalculateRequest(BaseModel):
    items: str

@app.post("/tools/calculate_sum")
def calculate_sum_endpoint(req: CalculateRequest):
    return {"result": calculate_sum(req.items)}
