# 🚀 Déploiement - Application Chat IA Cascade T1→T2

## Mode Développement (Actuellement Actif)

L'application tourne en ce moment:

```bash
🌐 http://localhost:5000
🐳 Container: sovereign-chat
📦 Port: 5000
```

### Vérifier le Status
```bash
curl http://localhost:5000/api/status
```

### Arrêter
```bash
docker stop sovereign-chat
```

### Redémarrer
```bash
docker run --rm -d \
  --name sovereign-chat \
  --network host \
  -v $(pwd):/app \
  -w /app \
  python:3.11-slim \
  bash -c "pip install -q fastapi uvicorn && \
           python -m uvicorn api.chat_app:app --host 0.0.0.0 --port 5000"
```

---

## Production - Docker Compose

Créer `docker-compose.chat.yml`:

```yaml
version: '3.8'

services:
  chat:
    image: python:3.11-slim
    container_name: sovereign-chat-prod
    command: bash -c "pip install -q fastapi uvicorn && python -m uvicorn api.chat_app:app --host 0.0.0.0 --port 5000"
    volumes:
      - ./api:/app/api
      - ./static:/app/static
    ports:
      - "5000:5000"
    environment:
      - PYTHONUNBUFFERED=1
    depends_on:
      - ollama
    networks:
      - sovereign

networks:
  sovereign:
    driver: bridge
```

Lancer:
```bash
docker-compose -f docker-compose.chat.yml up -d
```

---

## Production - Linux Natif (Recommandé)

### 1. Installer Python
```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

### 2. Installer Dépendances
```bash
cd /opt/claude/sovereign-ai
pip3 install -r requirements_api.txt
```

### 3. Créer Service Systemd

Créer `/etc/systemd/system/sovereign-chat.service`:

```ini
[Unit]
Description=Sovereign AI Chat
After=network.target

[Service]
Type=simple
User=claude
WorkingDirectory=/opt/claude/sovereign-ai
ExecStart=/usr/bin/python3 -m uvicorn api.chat_app:app --host 0.0.0.0 --port 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Activer le Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable sovereign-chat
sudo systemctl start sovereign-chat
sudo systemctl status sovereign-chat
```

### 5. Logs
```bash
sudo journalctl -u sovereign-chat -f
```

---

## Production - Nginx Reverse Proxy

Créer `/etc/nginx/sites-available/sovereign-chat`:

```nginx
upstream sovereign_chat {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    # Redirection HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    client_max_body_size 10M;
    
    location / {
        proxy_pass http://sovereign_chat;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeout
        proxy_read_timeout 86400;
    }
}
```

Activer:
```bash
sudo ln -s /etc/nginx/sites-available/sovereign-chat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Production - Kubernetes

Créer `chat-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sovereign-chat
spec:
  replicas: 2
  selector:
    matchLabels:
      app: sovereign-chat
  template:
    metadata:
      labels:
        app: sovereign-chat
    spec:
      containers:
      - name: chat
        image: python:3.11-slim
        command: ["python", "-m", "uvicorn", "api.chat_app:app", "--host", "0.0.0.0", "--port", "5000"]
        ports:
        - containerPort: 5000
        volumeMounts:
        - name: app
          mountPath: /app
        env:
        - name: PYTHONUNBUFFERED
          value: "1"
        livenessProbe:
          httpGet:
            path: /api/status
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
      volumes:
      - name: app
        hostPath:
          path: /opt/claude/sovereign-ai

---
apiVersion: v1
kind: Service
metadata:
  name: sovereign-chat-service
spec:
  selector:
    app: sovereign-chat
  ports:
  - port: 5000
    targetPort: 5000
  type: LoadBalancer
```

Déployer:
```bash
kubectl apply -f chat-deployment.yaml
```

---

## Monitoring

### Prometheus Metrics

Ajouter à `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'sovereign-chat'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
```

### Logs

```bash
# Développement
docker logs -f sovereign-chat

# Production (Systemd)
journalctl -u sovereign-chat -f

# Kubernetes
kubectl logs -f deployment/sovereign-chat
```

---

## Optimisations Production

### 1. Uvicorn avec Gunicorn
```bash
pip install gunicorn
gunicorn api.chat_app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
```

### 2. Cache
Ajouter Redis pour les sessions chat:
```python
from redis import Redis
redis_client = Redis(host='localhost', port=6379, db=0)
```

### 3. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
@limiter.limit("30/minute")
async def chat(msg: ChatMessage):
    ...
```

### 4. CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Checklist Déploiement

- [ ] Tester localement ✅
- [ ] Configurer HTTPS
- [ ] Configurer firewall
- [ ] Installer monitoring (Prometheus/Grafana)
- [ ] Configurer backups
- [ ] Tester failover
- [ ] Configurer alertes
- [ ] Documentation d'équipe
- [ ] Plan de récupération

---

## Support Gouvernemental (DSI Polynésie)

**Conformité:**
- ✅ RGPD: Tous les chats restent locaux (pas d'envoi cloud)
- ✅ Souveraineté: Données gouvernementales jamais en cloud
- ✅ Audit: Logs complets disponibles
- ✅ Langues: Support français natif (T1)

**Configuration Recommandée:**
- Linux Ubuntu 24.04 LTS
- PostgreSQL pour persistance chats
- Nginx avec SSL/TLS
- Monitoring Prometheus + Grafana
- Backups quotidiens

---

## Troubleshooting

### Port Occupé
```bash
lsof -i :5000
kill -9 <PID>
```

### WebSocket Erreur
- Vérifier Nginx proxy headers (voir config ci-dessus)
- Vérifier firewall WebSocket (port 5000)

### Ollama Non Connecté
```bash
docker ps | grep ollama
curl http://localhost:11434/api/tags
```

### Performance Lente
- Vérifier GPU: `nvidia-smi`
- Vérifier RAM: `free -h`
- Profiler: `python -m cProfile api/chat_app.py`

---

## Questions?

Consulter:
1. `CHAT_GUIDE.md` - Utilisation utilisateur
2. `CLAUDE.md` - Configuration système
3. Logs serveur - Debugging
