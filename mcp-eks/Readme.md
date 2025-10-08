Perfect! Let’s create a **complete project README** that includes:

* Docker build and run commands
* Kubernetes service setup
* DNS steps for remote access

---

# **README.md**

```markdown
# MCP Calculator Server (Docker + Kubernetes)

This project demonstrates a **Model Context Protocol (MCP) server** wrapped with **FastAPI**, containerized with Docker, and ready for Kubernetes deployment with DNS setup.

---

## **Project Structure**

```

mcp-invoice-project/
├─ mcp_server_fastapi.py    # MCP server + FastAPI endpoints
├─ requirements.txt         # Python dependencies
├─ Dockerfile               # Dockerfile for MCP server
├─ README.md

````

---

## **1️⃣ MCP Server Overview**

- MCP server exposes **tools** (like `calculate_sum`) via HTTP.
- Health endpoint `/healthz` for monitoring.
- Tool endpoint `/tools/calculate_sum` for agent calls.

---

## **2️⃣ Docker Commands**

### Build Docker Image

```bash
docker build -t your-dockerhub-username/mcp-server:latest .
````

### Run Locally (optional)

```bash
docker run -p 8080:8080 your-dockerhub-username/mcp-server:latest
```

* Health check:

```bash
curl http://localhost:8080/healthz
# {"status": "ok"}
```

* Test calculate_sum tool:

```bash
curl -X POST http://localhost:8080/tools/calculate_sum \
-H "Content-Type: application/json" \
-d '{"items": "2 x 10, 3 x 20"}'
# {"result":"80.00"}
```

### Push Docker Image to Registry

```bash
docker push your-dockerhub-username/mcp-server:latest
```

---

## **3️⃣ Kubernetes Deployment**

### Deployment Manifest (example)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
        - name: mcp-server
          image: your-dockerhub-username/mcp-server:latest
          ports:
            - containerPort: 8080
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

### Service Manifest (LoadBalancer for external access)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mcp-service
spec:
  type: LoadBalancer
  selector:
    app: mcp-server
  ports:
    - protocol: TCP
      port: 80        # external port
      targetPort: 8080  # container port
```

* Apply manifests:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

* Get external LB DNS:

```bash
kubectl get svc mcp-service
# EXTERNAL-IP or DNS
```

---

## **4️⃣ DNS Setup (Route 53 / AWS)**

1. In **Route 53**, create a **CNAME** or **A record**:

   * Name: `mcp.example.com`
   * Type: CNAME
   * Value: `<EXTERNAL-LB-DNS>`

2. Test the endpoint:

```bash
curl http://mcp.example.com/healthz
# {"status": "ok"}
```

3. Call tool remotely:

```bash
curl -X POST http://mcp.example.com/tools/calculate_sum \
-H "Content-Type: application/json" \
-d '{"items": "2 x 10, 3 x 20"}'
```

---

## **5️⃣ Notes**

* MCP tool logic is **decoupled** from HTTP transport.
* Health endpoint ensures **K8s pods are monitored and traffic is routed correctly**.
* You can scale MCP server pods independently and update tools without affecting agents.
* Ready for multi-tool extension or LLM agent integration.

```

---

This README provides a **full local + EKS deployment guide**, including **Docker commands, health checks, service manifest, and DNS steps**.  

If you want, I can **also include a `docker-compose.yml` for local multi-container testing** with the agent calling MCP server — it’s super useful before moving to EKS.  

Do you want me to do that?
```
