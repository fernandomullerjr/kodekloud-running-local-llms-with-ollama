

# OpenWebUi
## 🐳 Comando para WSL2 (Docker), para subir o OpenWebUi:
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main

# Acesso via ip 192.168.1.62:
http://192.168.1.62:3000/auth?redirect=%2F
ou no WSL:
http://localhost:3000



# Ollama via CURL

curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1:latest",
    "prompt": "Explique o que é aprendizado de máquina.",
    "stream": false
  }'



curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1:latest",
    "prompt": "Explique COMO FAZER UMA PESQUISA NO GOOGLE.",
    "stream": false
  }' | jq .
  