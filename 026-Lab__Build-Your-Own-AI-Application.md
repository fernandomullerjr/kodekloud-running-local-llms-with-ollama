
# Lab: Build Your Own AI Application

1 / 2
info

Ollama Labs

The Ollama service is running on the ollama-server.

To access the server, use the following SSH command:

ssh ai-engineer@$IP_ADDRESS



2 / 2
info

Ollama Labs

Develop an application which interacts that the Ollama API running at http://localhost:11434/v1 in ollama-server. Use the previous video as a reference for interacting with the API. Use the qwen:0.5b model, which is already running for you with the help of ollama server.

To get the exact name of ollama server , You can use command hostname , in this example , the hostname is ollama-server-1755523044.

ai-engineer@ollama-server-1755523044:~$ hostname
ollama-server-1755523044

NOTE: All ports from 80 to 8080 are open on the ollama-server. Run the application on any of these ports, then access it in your browser using the IP_ADDRESS.



forneça código em python para servidor em flask que interage com api do openai e/ou ollama e na interface dele aceite que o usuario crie prompt para pedir para ele criar 1 poema
aplicação deve ser servida na porta 8080
também deve consumir os valores como openai api key, endpoint, modelo, etc, tudo de variáveis de ambiente.
e traga .env de exemplo


Aqui vai um **exemplo completo** de aplicação Flask servindo na **porta 8080** que conversa com **OpenAI** **e/ou** **Ollama**, escolhendo o provedor via variável de ambiente.
A interface web aceita um **prompt** do usuário para gerar **1 poema**.
Todas as credenciais e configurações vêm de **variáveis de ambiente** (e deixei um `.env` de exemplo no final).

---

# `app.py`

```python
import os
import json
import requests
from flask import Flask, request, render_template_string, redirect, url_for, flash

# ----------------------------
# Config via variáveis de ambiente
# ----------------------------
PROVIDER = os.environ.get("PROVIDER", "ollama").lower()  # "openai" ou "ollama"
# OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com")  # pode apontar para um proxy compatível
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_USE_RESPONSES_API = os.environ.get("OPENAI_USE_RESPONSES_API", "false").lower() == "true"
# Ollama
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen:0.5b")
OLLAMA_STREAM = os.environ.get("OLLAMA_STREAM", "false").lower() == "true"

# Flask
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret")  # para flash messages
app = Flask(__name__)
app.secret_key = SECRET_KEY

# ----------------------------
# HTML (inline, simples)
# ----------------------------
TEMPLATE = """
<!doctype html>
<html lang="pt-br">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Poemas com LLM (OpenAI / Ollama)</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; }
    header { margin-bottom: 16px; }
    form { display: grid; gap: 12px; max-width: 720px; }
    textarea { width: 100%; min-height: 120px; padding: 10px; font-size: 1rem; }
    input[type="text"], select { padding: 8px; font-size: 1rem; }
    button { padding: 10px 14px; font-size: 1rem; cursor: pointer; }
    .row { display: grid; gap: 8px; grid-template-columns: 1fr 1fr; }
    .result { white-space: pre-wrap; padding: 12px; background: #f6f6f6; border-radius: 8px; max-width: 720px; }
    .env { font-size: 0.9rem; color: #555; }
    .flash { color: #b00020; margin: 8px 0; }
  </style>
</head>
<body>
  <header>
    <h1>Gerador de Poemas — OpenAI / Ollama</h1>
    <p class="env">Provedor atual: <strong>{{ provider }}</strong>
      {% if provider == "openai" %}(modelo: {{ openai_model }}, endpoint: {{ openai_base }}){% endif %}
      {% if provider == "ollama" %}(modelo: {{ ollama_model }}, endpoint: {{ ollama_base }}){% endif %}
    </p>
  </header>

  {% with messages = get_flashed_messages() %}
    {% if messages %}
      {% for m in messages %}
        <div class="flash">{{ m }}</div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  <form method="post" action="{{ url_for('generate') }}">
    <label for="prompt">Tema/briefing do poema (ex.: "noite chuvosa em Porto Alegre, tom melancólico")</label>
    <textarea id="prompt" name="prompt" placeholder="Descreva o que você quer no poema..." required>{{ prompt or "" }}</textarea>

    <div class="row">
      <div>
        <label for="style">Estilo (opcional)</label>
        <input id="style" name="style" type="text" placeholder="soneto, haicai, livre, cordel..." value="{{ style or '' }}"/>
      </div>
      <div>
        <label for="length">Comprimento (opcional)</label>
        <input id="length" name="length" type="text" placeholder="curto, médio, ~12 versos..." value="{{ length or '' }}"/>
      </div>
    </div>

    <div class="row">
      <div>
        <label for="language">Idioma do poema</label>
        <select id="language" name="language">
          <option value="pt-br" {% if language == "pt-br" %}selected{% endif %}>Português (Brasil)</option>
          <option value="en" {% if language == "en" %}selected{% endif %}>Inglês</option>
        </select>
      </div>
      <div>
        <label for="provider">Provedor (sobrepõe o .env)</label>
        <select id="provider" name="provider">
          <option value="auto" selected>auto (.env)</option>
          <option value="openai">openai</option>
          <option value="ollama">ollama</option>
        </select>
      </div>
    </div>

    <button type="submit">Criar 1 poema</button>
  </form>

  {% if poem %}
    <h2>Poema</h2>
    <div class="result">{{ poem }}</div>
  {% endif %}
</body>
</html>
"""

# ----------------------------
# Helpers
# ----------------------------

def build_instruction(prompt: str, style: str = "", length: str = "", language: str = "pt-br") -> str:
    # Mensagem única e objetiva pro LLM
    lang_label = "Português do Brasil" if language.lower() == "pt-br" else "English"
    pieces = [
        "Você é um assistente literário.",
        "Tarefa: escrever exatamente 1 poema, sem explicações adicionais.",
        f"Idioma: {lang_label}.",
    ]
    if style.strip():
        pieces.append(f"Estilo desejado: {style.strip()}.")
    if length.strip():
        pieces.append(f"Comprimento desejado: {length.strip()}.")
    pieces.append(f"Tema/briefing: {prompt.strip()}")
    pieces.append("Não inclua títulos, prólogos ou epílogos — apenas o poema.")
    return "\n".join(pieces)

def call_openai(prompt_text: str) -> str:
    """
    Faz chamada à API OpenAI.
    Usa Responses API se OPENAI_USE_RESPONSES_API=true, senão usa Chat Completions.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    if OPENAI_USE_RESPONSES_API:
        # Responses API
        url = f"{OPENAI_BASE_URL.rstrip('/')}/v1/responses"
        payload = {
            "model": OPENAI_MODEL,
            "input": prompt_text,
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        r.raise_for_status()
        data = r.json()
        # resposta pode vir em data["output_text"] (OpenAI SDK) ou em "content"→"text"
        # fallback defensivo:
        if "output_text" in data:
            return data["output_text"]
        if "choices" in data and data["choices"]:
            content = data["choices"][0].get("message", {}).get("content", "")
            if content:
                return content
        # formato alternativo (array content)
        if "content" in data and data["content"]:
            parts = []
            for c in data["content"]:
                if c.get("type") == "output_text":
                    parts.append(c.get("text", ""))
                elif c.get("type") == "text":
                    parts.append(c.get("text", ""))
            if parts:
                return "\n".join(parts)
        return json.dumps(data, ensure_ascii=False)
    else:
        # Chat Completions
        url = f"{OPENAI_BASE_URL.rstrip('/')}/v1/chat/completions"
        payload = {
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful literary assistant."},
                {"role": "user", "content": prompt_text},
            ],
            "temperature": 0.9,
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]

def call_ollama(prompt_text: str) -> str:
    """
    Faz chamada à API do Ollama (endpoint /api/generate).
    """
    url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt_text,
        "stream": OLLAMA_STREAM,
        "options": {
            "temperature": 0.9
        }
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
    r.raise_for_status()
    # Se stream=false, resposta vem como JSON único
    # Se stream=true, resposta vem linha-a-linha (precisaria agregar) — aqui usamos stream=false por padrão
    data = r.json()
    # Campo pode ser "response"
    return data.get("response", json.dumps(data, ensure_ascii=False))

def get_provider(request_provider: str) -> str:
    """
    Decide qual provedor usar: form > env.
    """
    if request_provider and request_provider.lower() in ("openai", "ollama"):
        return request_provider.lower()
    return PROVIDER

# ----------------------------
# Rotas
# ----------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        TEMPLATE,
        provider=PROVIDER,
        openai_model=OPENAI_MODEL,
        openai_base=OPENAI_BASE_URL,
        ollama_model=OLLAMA_MODEL,
        ollama_base=OLLAMA_BASE_URL,
        poem=None,
        prompt="",
        style="",
        length="",
        language="pt-br",
    )

@app.route("/", methods=["POST"])
def generate():
    user_prompt = (request.form.get("prompt") or "").strip()
    style = (request.form.get("style") or "").strip()
    length = (request.form.get("length") or "").strip()
    language = (request.form.get("language") or "pt-br").strip()
    chosen_provider = get_provider(request.form.get("provider", "auto"))

    if not user_prompt:
        flash("Informe um tema/briefing para o poema.")
        return redirect(url_for("index"))

    instruction = build_instruction(user_prompt, style=style, length=length, language=language)

    try:
        if chosen_provider == "openai":
            if not OPENAI_API_KEY:
                raise RuntimeError("OPENAI_API_KEY não configurada.")
            poem = call_openai(instruction)
        else:
            poem = call_ollama(instruction)
    except requests.HTTPError as e:
        msg = f"Erro HTTP ao chamar {chosen_provider}: {e.response.status_code} - {e.response.text}"
        flash(msg)
        poem = ""
    except Exception as e:
        flash(f"Erro ao gerar poema: {e}")
        poem = ""

    return render_template_string(
        TEMPLATE,
        provider=chosen_provider,
        openai_model=OPENAI_MODEL,
        openai_base=OPENAI_BASE_URL,
        ollama_model=OLLAMA_MODEL,
        ollama_base=OLLAMA_BASE_URL,
        poem=poem,
        prompt=user_prompt,
        style=style,
        length=length,
        language=language,
    )

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    # Servir na porta 8080, acessível externamente (0.0.0.0)
    app.run(host="0.0.0.0", port=8080, debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
```

---

# `.env` (exemplo)

```env
# Provedor padrão: "openai" ou "ollama"
PROVIDER=ollama

# Flask
FLASK_SECRET_KEY=troque-esta-chave
FLASK_DEBUG=false

# OpenAI (use se PROVIDER=openai)
OPENAI_API_KEY=coloque_sua_chave_aqui
OPENAI_BASE_URL=https://api.openai.com
OPENAI_MODEL=gpt-4o-mini
# Use a Responses API (true/false). Se false, usa Chat Completions.
OPENAI_USE_RESPONSES_API=false

# Ollama (use se PROVIDER=ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen:0.5b
# Streaming no /api/generate (true/false). Mantemos false no app para simplificar.
OLLAMA_STREAM=false
```

---

## Como rodar

1. Salve `app.py` e o `.env` no mesmo diretório.
2. Instale dependências:

```bash
pip install flask requests python-dotenv
```

3. Exporte as variáveis (ou use `python-dotenv`, executando com `ENV` carregado pelo shell):

```bash
export $(grep -v '^#' .env | xargs)
```

4. Inicie o servidor:

```bash
python app.py
```

5. Acesse:

```
http://localhost:8080
```

---


http://192.168.1.109:8080/

Erro HTTP ao chamar ollama: 404 - {"error":"model 'qwen:0.5b' not found"}




> ollama run deepseek-r1:70b "me mostre um codigo em python que comunica com api do ollama"
Error: 500 Internal Server Error: model requires more system memory (35.6 GiB) than is available (11.4 GiB)

 ~              