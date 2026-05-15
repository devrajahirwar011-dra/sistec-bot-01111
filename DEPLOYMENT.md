# DEPLOYMENT GUIDE - SISTec RAG Chatbot

## 📋 Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Setup](#production-setup)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🖥️ Local Development

### Requirements
- Python 3.8+
- 4GB RAM (minimum)
- 2GB disk space
- Google Gemini API key

### Setup Steps

```bash
# 1. Clone/navigate to project
cd sistec-rag-chatbot

# 2. Run setup script
python setup.py

# 3. Configure environment
# Edit .env and add your GEMINI_API_KEY

# 4. Add documents
# Place documents in ./documents/ folder

# 5. Start CLI
python main.py --cli
```

### Verification
```bash
python main.py --query "What is SISTec?"
```

---

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p documents vector_store logs

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run API
CMD ["python", "main.py", "--api", "--host", "0.0.0.0", "--port", "8000"]
```

### Build & Run
```bash
# Build image
docker build -t sistec-chatbot:latest .

# Run container
docker run -d \
  --name sistec-chatbot \
  -p 8000:8000 \
  -v $(pwd)/documents:/app/documents \
  -v $(pwd)/vector_store:/app/vector_store \
  -e GEMINI_API_KEY=your-key-here \
  sistec-chatbot:latest

# Check logs
docker logs -f sistec-chatbot

# Stop container
docker stop sistec-chatbot
```

### Docker Compose
```yaml
version: '3.8'

services:
  sistec-chatbot:
    build: .
    container_name: sistec-chatbot
    ports:
      - "8000:8000"
    environment:
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      VECTOR_DB_TYPE: chroma
      DOCUMENTS_PATH: /app/documents
    volumes:
      - ./documents:/app/documents
      - ./vector_store:/app/vector_store
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Start with: `docker-compose up -d`

---

## ☁️ Cloud Deployment

### AWS EC2

```bash
# 1. Launch EC2 instance
# - OS: Ubuntu 22.04 LTS
# - Type: t3.medium (minimum)
# - Storage: 50GB

# 2. SSH into instance
ssh -i key.pem ubuntu@instance-ip

# 3. Install Python & Git
sudo apt update
sudo apt install python3.11 python3.11-venv git -y

# 4. Clone repository
git clone https://github.com/yourusername/sistec-rag-chatbot.git
cd sistec-rag-chatbot

# 5. Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Configure environment
cp .env.example .env
# Edit .env with your settings
nano .env

# 8. Start with systemd
```

### Systemd Service (AWS/Linux)
Create `/etc/systemd/system/sistec-chatbot.service`:
```ini
[Unit]
Description=SISTec RAG Chatbot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/sistec-rag-chatbot
Environment="PATH=/home/ubuntu/sistec-rag-chatbot/venv/bin"
Environment="GEMINI_API_KEY=your-key"
ExecStart=/home/ubuntu/sistec-rag-chatbot/venv/bin/python main.py --api --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sistec-chatbot
sudo systemctl start sistec-chatbot
sudo systemctl status sistec-chatbot
```

### Google Cloud Run

```bash
# 1. Create .gcloudignore (similar to .gitignore)

# 2. Deploy
gcloud run deploy sistec-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars GEMINI_API_KEY=your-key

# Service URL will be provided
# Example: https://sistec-chatbot-xxxxx.run.app
```

### Heroku Deployment

```bash
# 1. Create Procfile
echo "web: python main.py --api --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Create requirements.txt (already done)

# 3. Deploy
heroku login
heroku create sistec-chatbot
heroku config:set GEMINI_API_KEY=your-key
git push heroku main

# Access at: https://sistec-chatbot.herokuapp.com
```

---

## 🏢 Production Setup

### Reverse Proxy (Nginx)

```nginx
upstream sistec_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name chatbot.sistec.ac.in;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name chatbot.sistec.ac.in;
    
    ssl_certificate /etc/letsencrypt/live/chatbot.sistec.ac.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/chatbot.sistec.ac.in/privkey.pem;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://sistec_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /static/ {
        alias /var/www/sistec-chatbot/static/;
    }
}
```

### SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d chatbot.sistec.ac.in
```

### Gunicorn (Production WSGI Server)

```bash
# Install gunicorn
pip install gunicorn

# Create wsgi.py
cat > wsgi.py << 'EOF'
from fastapi.asgi import ASGIApp
from chatbot_api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
EOF

# Run with gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 --worker-class uvicorn.workers.UvicornWorker chatbot_api:app
```

### Database Backup

```bash
# Backup vector store
tar -czf vector_store_backup_$(date +%Y%m%d).tar.gz vector_store/

# Backup documents
tar -czf documents_backup_$(date +%Y%m%d).tar.gz documents/

# Automated daily backup
0 2 * * * cd /app && tar -czf /backups/sistec_backup_$(date +\%Y\%m\%d).tar.gz vector_store/ documents/
```

---

## 📊 Monitoring & Maintenance

### Health Check Endpoint
```bash
curl http://localhost:8000/health
```

### Logging Setup

```python
# In your main.py
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'logs/chatbot.log',
            maxBytes=10485760,
            backupCount=5
        )
    ]
)
```

### Monitoring Tools

#### Prometheus Metrics
Add to `chatbot_api.py`:
```python
from prometheus_client import Counter, Histogram, make_wsgi_app
from fastapi.responses import PlainTextResponse

query_counter = Counter('queries_total', 'Total queries')
query_duration = Histogram('query_duration_seconds', 'Query duration')

@app.get("/metrics")
def metrics():
    return PlainTextResponse(content=generate_latest())
```

#### Log Monitoring
```bash
# Real-time logs
tail -f logs/chatbot.log

# Error logs only
grep ERROR logs/chatbot.log

# Performance stats
grep "query_duration" logs/chatbot.log | tail -100
```

### Performance Optimization

1. **Database Optimization**
   ```bash
   # Use FAISS for large documents (>10,000 chunks)
   python main.py --init ./documents --db-type faiss
   ```

2. **Caching**
   - Add Redis for query caching
   - Cache frequently asked questions

3. **Load Balancing**
   ```bash
   # Run multiple instances
   python main.py --api --port 8001 &
   python main.py --api --port 8002 &
   python main.py --api --port 8003 &
   ```

### Maintenance Tasks

**Daily**
- Monitor error logs
- Check API response times
- Verify health endpoint

**Weekly**
- Backup vector database
- Review query logs
- Update documents if needed

**Monthly**
- Review performance metrics
- Optimize chunk sizes if needed
- Update dependencies

---

## 🔐 Security Checklist

- [ ] API key stored in environment variables (not in code)
- [ ] HTTPS enabled (SSL/TLS)
- [ ] Rate limiting configured
- [ ] Input validation on all endpoints
- [ ] Access logs enabled
- [ ] Regular backups configured
- [ ] Error messages don't leak sensitive info
- [ ] CORS properly configured
- [ ] Authentication for admin endpoints (if any)
- [ ] Database encryption at rest

---

## 📞 Troubleshooting

### Issue: API not responding
```bash
# Check if service is running
ps aux | grep python

# Check port usage
lsof -i :8000

# Restart service
systemctl restart sistec-chatbot
```

### Issue: Out of memory
```bash
# Reduce chunk size
CHUNK_SIZE=500

# Use FAISS instead of Chroma
VECTOR_DB_TYPE=faiss

# Increase system RAM or swap
```

### Issue: Slow responses
```bash
# Reduce TOP_K_CHUNKS
TOP_K_CHUNKS=3

# Increase timeout in nginx
proxy_read_timeout 120s;

# Add caching layer (Redis)
```

---

## 📈 Scaling

### Horizontal Scaling (Multiple Servers)
```yaml
# Load Balancer Configuration (HAProxy)
global
    maxconn 4096

frontend sistec_frontend
    bind 0.0.0.0:80
    mode http
    default_backend sistec_backend

backend sistec_backend
    balance roundrobin
    server app1 10.0.0.1:8000
    server app2 10.0.0.2:8000
    server app3 10.0.0.3:8000
```

### Vertical Scaling
- Increase CPU/RAM
- Use GPU for embeddings (if available)
- Optimize code

---

**Last Updated**: May 2026
