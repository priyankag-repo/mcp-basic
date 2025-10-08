# Dockerfile for MCP Server
FROM python:3.13-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY mcp_server_fastapi.py .

# Expose port for FastAPI
EXPOSE 8080

# Run MCP server via uvicorn
CMD ["uvicorn", "mcp_server_fastapi:app", "--host", "0.0.0.0", "--port", "8080"]
