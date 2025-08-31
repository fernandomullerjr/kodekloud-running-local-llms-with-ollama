

Comando **completo** para rodar o **Open WebUI** com **Docker** integrado ao Ollama.

---

## 🐳 Comando completo

```bash
docker run -d \
  --name open-webui \
  --network=host \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  -v open-webui:/app/backend/data \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

---

## 📌 Explicação dos parâmetros

* `-d` → Roda em **modo detach** (em segundo plano).
* `--name open-webui` → Nome do container.
* `--network=host` → Usa a rede do host, permitindo acessar `localhost:11434` diretamente.
* `-e OLLAMA_BASE_URL=http://127.0.0.1:11434` → Define o endpoint do Ollama.
* `-v open-webui:/app/backend/data` → Volume persistente para salvar histórico e configurações.
* `--restart always` → Reinicia automaticamente caso o container pare.
* `ghcr.io/open-webui/open-webui:main` → Imagem oficial do Open WebUI no GitHub Container Registry.

---

## 🚀 Passos antes de rodar

1. **Certifique-se de que o Ollama está rodando**:

```bash
ollama serve
```

ou, se estiver como serviço systemd:

```bash
systemctl status ollama
```

2. **Verifique se o modelo desejado está instalado**:

```bash
ollama list
ollama pull deepseek-r1
```

3. **Execute o comando Docker** (acima).

4. **Acesse no navegador**:

```
http://localhost:8080
```

---




O comando que aparece na sua captura de tela(comando mostrado no curso da KodeKloud):

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

é indicado quando você **não está usando `--network=host`** (como no Linux) e quer rodar o **Open WebUI** mapeando portas explicitamente para acessar via navegador.

### 📌 Quando usar esse comando

* Quando **o Docker não está em modo host network** (ex.: no Windows ou macOS, ou em WSL2).
* Quando você quer **acessar a UI do Open WebUI** em uma porta específica (`localhost:3000` no exemplo).
* Quando precisa que o Open WebUI consiga se comunicar com o Ollama que está fora do container — por isso existe o `--add-host=host.docker.internal:host-gateway`.
* Quando quer **persistir dados** (histórico, configurações) no volume `open-webui`.

### ⚠️ Diferença para `--network=host`

* `--network=host` (comum no Linux) não exige `-p` nem `--add-host`.
* Em WSL2 ou macOS, o mapeamento explícito de porta (`-p 3000:8080`) e o `--add-host` são necessários para a UI encontrar o servidor do Ollama.

Se quiser, posso te passar **o comando equivalente para WSL2 integrando diretamente com o Ollama** para evitar problemas de conexão. Quer que eu te envie?




Beleza — aqui vai o comando completo para rodar o **Open WebUI** no **WSL2** integrado ao **Ollama**, evitando problemas de conexão.

---

## 🐳 Comando para WSL2 (Docker)

```bash
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

---

## 📌 Explicação

* `-p 3000:8080` → expõe a porta **3000** do host para a porta interna **8080** do Open WebUI (acesso via `http://localhost:3000`).
* `--add-host=host.docker.internal:host-gateway` → cria um atalho dentro do container para acessar o Ollama que roda no WSL2.
* `-e OLLAMA_BASE_URL=http://host.docker.internal:11434` → indica para o Open WebUI onde está a API do Ollama.
* `-v open-webui:/app/backend/data` → volume para salvar chats e configurações.
* `--restart always` → reinicia automaticamente o container se ele parar.

---

## 🚀 Passos antes de rodar

1. **Inicie o Ollama no WSL2**:

```bash
ollama serve
```

*(ou verifique se já está rodando como serviço)*

2. **Certifique-se que o modelo está instalado**:

```bash
ollama pull deepseek-r1
```

3. **Execute o comando Docker** acima.

4. **Acesse no navegador**:

```
http://localhost:3000
```

---





- Testando


> docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
Unable to find image 'ghcr.io/open-webui/open-webui:main' locally
main: Pulling from open-webui/open-webui
b1badc6e5066: Pull complete
38b81130a831: Pull complete
f68adc1d13a4: Pull complete
6892a96cf1e5: Pull complete
e86b2d39364b: Pull complete
4f4fb700ef54: Pull complete
a9ffb5fb24a2: Pull complete
1c423dc9638d: Pull complete
bca1513d9cbb: Pull complete
e0eb15a3664a: Pull complete
0b49074fb6b8: Pull complete
c9e940e66251: Pull complete
8bc2257a6815: Pull complete
614185f46ad5: Pull complete
c498f7b0d55a: Pull complete
cebb18a26bcc: Pull complete
Digest: sha256:06f4cae7f8873ebcee7952d9993e457c1b083c6bea67b10bc356db7ac71c28e2
Status: Downloaded newer image for ghcr.io/open-webui/open-webui:main
673cad0b20a644859968e15695c7cf2fc90cd243506071c1445fb32afbc42adc
> docker ps
CONTAINER ID   IMAGE                                COMMAND           CREATED         STATUS                   PORTS                    NAMES
673cad0b20a6   ghcr.io/open-webui/open-webui:main   "bash start.sh"   4 minutes ago   Up 4 minutes (healthy)   0.0.0.0:3000->8080/tcp   open-webui

 ~        


> ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 5e:bb:f6:9e:ee:fa brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.62/24 brd 192.168.1.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet 192.168.0.107/24 brd 192.168.0.255 scope global eth0
       valid_lft forever preferred_lft forever

ip
192.168.1.62
<http://192.168.1.62:3000/auth?redirect=%2F>


- Acesso via ip 192.168.1.62:
<http://192.168.1.62:3000/auth?redirect=%2F>




- TSHOOT: OpenWebUi não mostra modelo algum, mesmo com Ollama rodando. Revisar o comando Docker e analisar o que pode estar ocorrendo.


- Teste a API a partir do container do Open WebUI:
> docker exec -it open-webui sh -c \
"apk add --no-cache curl >/dev/null 2>&1 || true; curl -sS http://host.docker.internal:11434/api/tags"

curl: (7) Failed to connect to host.docker.internal port 11434 after 0 ms: Couldn't connect to server

 ~                        



- ANTES
> ss -ltnp | grep 11434
LISTEN 0      4096       127.0.0.1:11434      0.0.0.0:*

 ~        




Valeu pelo teste — o erro confirma que o container **não consegue** alcançar o servidor do Ollama no host. Na prática, isso quase sempre é porque o Ollama está ouvindo **só em 127.0.0.1** (loopback). De dentro do container, “localhost” é o container, não o host.

Vamos corrigir em 3 passos rápidos:

---

## 1) Faça o Ollama ouvir em todas as interfaces

No WSL2, pare o Ollama (se estiver rodando) e suba ouvindo em `0.0.0.0`:

```bash
# se estiver rodando em primeiro plano:
pkill -f "ollama serve" 2>/dev/null || true

# iniciar ouvindo em todas as interfaces
OLLAMA_HOST=0.0.0.0 ollama serve
```

Se você usa systemd:

```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d
printf "[Service]\nEnvironment=OLLAMA_HOST=0.0.0.0\n" | \
  sudo tee /etc/systemd/system/ollama.service.d/override.conf

sudo systemctl daemon-reload
sudo systemctl restart ollama
```

✅ Verifique:

```bash
ss -ltnp | grep 11434     # deve aparecer 0.0.0.0:11434 LISTEN
curl -s http://localhost:11434/api/tags
```

---

## 2) Garanta o atalho do host no container

Recrie o Open WebUI com o mapeamento do “host-gateway” e a URL certa:

```bash
docker rm -f open-webui 2>/dev/null

docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

> Na UI (Settings → Connections), confirme que o **Base URL** do Ollama está em
> `http://host.docker.internal:11434`.

---

## 3) Teste de dentro do container

Agora deve responder:

```bash
docker exec -it open-webui sh -c \
"apk add --no-cache curl >/dev/null 2>&1 || true; curl -sS http://host.docker.internal:11434/api/tags"
```

Se devolver JSON com os modelos, a UI passa a listá-los imediatamente.

---

### Plano B (se ainda falhar)

Use o IP do WSL (em vez de `host.docker.internal`):

1. Descubra o IP do WSL:

```bash
ip -4 addr show eth0 | awk '/inet /{print $2}' | cut -d/ -f1
# exemplo: 172.27.208.1
```

2. Recrie o WebUI apontando para esse IP:

```bash
docker rm -f open-webui 2>/dev/null
docker run -d \
  -p 3000:8080 \
  -e OLLAMA_BASE_URL=http://<IP_DO_WSL>:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

---

Se quiser, me manda a saída de:

* `ss -ltnp | grep 11434`
* o resultado do **teste no container** (curl)

que eu ajusto exatamente no seu ambiente.





- Ajustando:

> sudo mkdir -p /etc/systemd/system/ollama.service.d
> printf "[Service]\nEnvironment=OLLAMA_HOST=0.0.0.0\n" | \
  sudo tee /etc/systemd/system/ollama.service.d/override.conf
[Service]
Environment=OLLAMA_HOST=0.0.0.0
> sudo systemctl daemon-reload
> sudo systemctl restart ollama
> ss -ltnp | grep 11434
LISTEN 0      4096               *:11434            *:*
>
> curl -s http://localhost:11434/api/tags
{"models":[{"name":"deepseek-r1:latest","model":"deepseek-r1:latest","modified_at":"2025-08-30T19:51:59.925509075-03:00","size":5225376047,"digest":"6995872bfe4c521a67b32da386cd21d5c6e819b6e0d62f79f64ec83be99f5763","details":{"parent_model":"","format":"gguf","family":"qwen3","families":["qwen3"],"parameter_size":"8.2B","quantization_level":"Q4_K_M"}}]}%    > docker rm -f open-webui 2>/dev/null
open-webui
> docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
dde7a808085163a0680de9bcf9495927334728320258c66faf0f5fb018a919f1
> docker exec -it open-webui sh -c \
"apk add --no-cache curl >/dev/null 2>&1 || true; curl -sS http://host.docker.internal:11434/api/tags"

{"models":[{"name":"deepseek-r1:latest","model":"deepseek-r1:latest","modified_at":"2025-08-30T19:51:59.925509075-03:00","size":5225376047,"digest":"6995872bfe4c521a67b32da386cd21d5c6e819b6e0d62f79f64ec83be99f5763","details":{"parent_model":"","format":"gguf","family":"qwen3","families":["qwen3"],"parameter_size":"8.2B","quantization_level":"Q4_K_M"}}]}%    >
> DATE
zsh: command not found: DATE
> date
Sun Aug 31 15:39:11 -03 2025

 ~                                                                                                        ok  15:39:11






## PENDENTE
- TSHOOT: OpenWebUi não mostra modelo algum, mesmo com Ollama rodando. Revisar o comando Docker e analisar o que pode estar ocorrendo.


## RESUMO

## 🐳 Comando para WSL2 (Docker)

```bash
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

- Acesso via ip 192.168.1.62:
<http://192.168.1.62:3000/auth?redirect=%2F>


