
# Community Integrations for Ollama


---

# 📚 Open WebUI & Ollama Chatbot UI

## Interfaces gráficas para interagir com LLMs localmente

---

## 1. O que são?

### **Open WebUI**

* Interface web **open-source** para conversar com LLMs (Large Language Models) de forma amigável.
* Compatível com **Ollama**, **OpenAI API**, **LM Studio** e outros backends.
* Possui recursos como histórico de conversas, múltiplos perfis de chat e upload de arquivos.
* Pode ser instalada via **Docker**, **pip** ou **snap**.

### **Ollama Chatbot UI**

* Interface gráfica simples criada especificamente para **Ollama**.
* Baseada no **Chatbot UI** (projeto popular no GitHub).
* Menos complexa que o Open WebUI, mas leve e direta.
* Ideal para quem quer apenas uma experiência semelhante ao ChatGPT com modelos locais.

---

## 2. Vantagens de usar uma UI com o Ollama

* **Interação visual**: não é preciso digitar comandos no terminal.
* **Histórico de conversas**: retome onde parou.
* **Parâmetros ajustáveis**: altere temperatura, contexto e outros sem editar arquivos.
* **Suporte a múltiplos modelos**: troque de LLM com um clique.
* **Upload de arquivos**: analise PDFs, textos e mais (principalmente no Open WebUI).

---

## 3. Como instalar e usar

### **Instalando o Open WebUI com Docker**

```bash
docker run -d --network=host \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

* Depois, abra no navegador:
  **[http://localhost:8080](http://localhost:8080)**

---

### **Instalando via Snap (Ubuntu)**

```bash
sudo apt install snapd
sudo snap install open-webui --beta
```

* Execute e acesse pelo navegador.

---

### **Rodando Ollama Chatbot UI**

1. Baixe o projeto do GitHub:

```bash
git clone https://github.com/mckaywrigley/ollama-chatbot-ui.git
cd ollama-chatbot-ui
```

2. Instale dependências:

```bash
npm install
```

3. Configure o `.env` com:

```
OLLAMA_API_URL=http://localhost:11434
```

4. Inicie:

```bash
npm run dev
```

5. Acesse no navegador (geralmente em `http://localhost:3000`).

---

## 4. Comparativo rápido

| Recurso                     | Open WebUI             | Ollama Chatbot UI   |
| --------------------------- | ---------------------- | ------------------- |
| Configuração de modelos     | ✅ Avançada             | 🔹 Básica           |
| Histórico de conversas      | ✅                      | ✅                   |
| Upload de arquivos          | ✅                      | ❌                   |
| Personalização de interface | ✅                      | 🔹 Limitada         |
| Facilidade de instalação    | 🔹 Média (Docker/Snap) | ✅ Simples (Node.js) |
| Foco                        | Multiplataforma        | Ollama puro         |

---

## 5. Boas práticas de uso

* **Sempre inicie o Ollama antes da UI** (`ollama serve` se não estiver rodando como serviço).
* **Ajuste o `context length` e a temperatura** na interface para melhor desempenho.
* **Use quantização leve** (ex.: `Q4_0`, `Q5_K_M`) se tiver pouca RAM.
* **Organize chats por projeto** no Open WebUI para manter contexto.

---
