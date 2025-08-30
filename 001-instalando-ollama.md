Um **guia completo** para você instalar e configurar o **Ollama** no **Ubuntu 22.04 rodando dentro do WSL2**, cobrindo desde o básico até a possibilidade de usar uma interface gráfica com **Open WebUI** — tudo passo a passo:

---

## 1. Preparando o WSL2

1. Assegure-se de que o Ubuntu 22.04 está instalado no seu WSL2.
2. Para habilitar o `systemd`, edite `/etc/wsl.conf` assim:

   ```
   [boot]
   systemd=true
   ```

   Depois, salve, feche e execute no PowerShell do Windows:

   ```
   wsl.exe --shutdown
   ```

   Reinicie o WSL e entre novamente no Ubuntu.([Home | Valchan][1])

---

## 2. Instalando o Ollama

1. No terminal Ubuntu (dentro do WSL), execute:

   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

   Isso baixa e instala o Ollama automaticamente.([It's FOSS][2])

2. Teste a instalação abrindo no navegador (Windows ou WSL):

   ```
   http://localhost:11434/
   ```

   Se estiver funcionando, verá a interface inicial do Ollama.([aleksandarhaber.com][3], [It's FOSS][2])

---

## 3. Comandos essenciais do Ollama

* **Listar modelos disponíveis**:

  ```bash
  ollama list
  ```

* **Baixar um modelo** (por exemplo, llama2):

  ```bash
  ollama pull llama2
  ```

* **Executar o modelo**:

  ```bash
  ollama run llama2 "Seu prompt aqui"
  ```

* Sair da interação com o modelo via:

  * `Ctrl + D` ou
  * Digite `/bye`([It's FOSS][2], [QuickCreator][4], [baxin.pages.dev][5])

* **Para listar modelos baixados**, use `ollama list`; para remover, `ollama rm <modelo>`.([linuxvox][6])

---

## 4. (Opcional) Configurar como serviço systemd

Se quiser que o Ollama rode automaticamente como serviço:

1. Baixe manualmente o binário:

   ```bash
   sudo curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama
   sudo chmod +x /usr/bin/ollama
   ```

2. Crie usuário dedicado:

   ```bash
   sudo useradd -r -s /bin/false -m -d /usr/share/ollama ollama
   ```

3. Crie o arquivo `/etc/systemd/system/ollama.service` com o seguinte conteúdo:

   ```
   [Unit]
   Description=Ollama Service
   After=network-online.target

   [Service]
   ExecStart=/usr/bin/ollama serve
   User=ollama
   Group=ollama
   Restart=always
   RestartSec=3

   [Install]
   WantedBy=default.target
   ```

4. Após salvar, execute:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ollama
   sudo systemctl start ollama
   ```

5. Para verificar logs:

   ```bash
   journalctl -e -u ollama
   ```

6. Para atualizar, basta rodar novamente o script de instalação ou baixar o binário como acima.([d2wozrt205r2fu.cloudfront.net][7], [Home | Valchan][1])

---

## 5. (Opcional) Acesso via interface gráfica — Open WebUI

Se quiser uma interface estilo ChatGPT:

1. instale o Docker no Ubuntu (WSL2) se ainda não tiver.

2. Execute o Open WebUI apontando para o Ollama com Docker:

   ```bash
   docker run -d --network=host \
      -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
      -v open-webui:/app/backend/data \
      --name open-webui --restart always \
      ghcr.io/open-webui/open-webui:main
   ```

   Depois, acesse em: `http://localhost:8080`([Home | Valchan][1], [It's FOSS][2])

3. Alternativamente, é possível usar o OpenWebUI via Snap no Ubuntu:

   ```bash
   sudo apt-get install snap
   sudo snap install open-webui --beta
   ```

   Após executar o Ollama, abra no navegador a interface (ex: `localhost:8080`).([maple-street.net][8])

---

## 6. Resumão rápido

| Etapa                     | Comando / Ação                                        |      |
| ------------------------- | ----------------------------------------------------- | ---- |
| Habilitar systemd         | Editar `/etc/wsl.conf`, reiniciar WSL                 |      |
| Instalar Ollama           | ````curl -fsSL https://ollama.com/install.sh | sh```` |      |
| Verificar se está rodando | Acessar `localhost:11434`                             |      |
| Gerenciar modelos         | `ollama pull/run/list/rm`                             |      |
| Rodar como serviço        | Criar service, `systemctl enable/start`               |      |
| GUI (opcional)            | Rodar Docker com Open WebUI, acessar `localhost:8080` |      |

---

Se você quiser, posso te ajudar também a configurar aceleração GPU (CUDA ou ROCm), otimizar desempenho ou automatizar isso com scripts, ou até integrar APIs — é só avisar!

[1]: https://valchan.com.br/wsl2-ollama-deepseek-openwebui/?utm_source=chatgpt.com "WSL2 + Ollama + DeepSeek + Open WebUI | Valchan"
[2]: https://itsfoss.com/ollama-setup-linux/?utm_source=chatgpt.com "Running AI Locally Using Ollama on Ubuntu Linux - It's FOSS"
[3]: https://aleksandarhaber.com/correctly-install-and-run-large-language-models-and-ollama-by-using-windows-subsystem-for-linux/?utm_source=chatgpt.com "Correctly Install and Run Large Language Models and Ollama by Using ..."
[4]: https://quickcreator.io/quthor_blog/setting-up-ollama-windows-wsl-step-by-step-guide/?utm_source=chatgpt.com "Install Ollama Python Chatbot: Step By Step Guide - QuickCreator"
[5]: https://baxin.pages.dev/ollama-llm-install-wsl/?utm_source=chatgpt.com "Guide to Installing and Running Ollama LLM with GPU on WSL"
[6]: https://linuxvox.com/blog/install-ollama-ubuntu/?utm_source=chatgpt.com "Installing Ollama on Ubuntu: A Comprehensive Guide"
[7]: https://d2wozrt205r2fu.cloudfront.net/p/ollama-knowledge-ubuntu-22-04-setup-cat-ai?utm_source=chatgpt.com "Ollama Ubuntu 22.04 Setup Guide | Restackio"
[8]: https://maple-street.net/host-your-own-local-ai-server-ollama-open-ui-ubuntu-22-04/?utm_source=chatgpt.com "Host your own Local AI Server | ollama | open-ui [snap] | Ubuntu 22.04"








- Efetuando
curl -fsSL https://ollama.com/install.sh | sh


> curl -fsSL https://ollama.com/install.sh | sh
>>> Installing ollama to /usr/local
>>> Downloading Linux amd64 bundle
##################################################                        69.7%



> curl -fsSL https://ollama.com/install.sh | sh
>>> Installing ollama to /usr/local
>>> Downloading Linux amd64 bundle
######################################################################## 100.0%
>>> Creating ollama user...
>>> Adding ollama user to render group...
>>> Adding ollama user to video group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
>>> Enabling and starting ollama service...
Created symlink /etc/systemd/system/default.target.wants/ollama.service → /etc/systemd/system/ollama.service.
>>> Nvidia GPU detected.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
> OLLMA
> ollama ps
NAME    ID    SIZE    PROCESSOR    UNTIL
> date
Sat Aug 30 19:37:51 -03 2025