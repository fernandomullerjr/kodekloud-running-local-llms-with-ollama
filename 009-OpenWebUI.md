

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


