Ótima! Vou trazer exemplos **práticos e variados** de requisições para o endpoint **`/api/chat`** do **Ollama**, para que você possa mostrar em aula diferentes cenários de uso.

---

# 📚 Exemplos de Requisições – `/api/chat` no Ollama

## 1. Conversa simples com contexto

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {"role": "system", "content": "Você é um professor de história."},
    {"role": "user", "content": "Quem descobriu o Brasil?"}
  ]
}'
```

➡️ O `system` define o papel do modelo, e o `user` envia a pergunta.

---

## 2. Mantendo histórico de conversa

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {"role": "system", "content": "Você é um guia turístico."},
    {"role": "user", "content": "Quais são os pontos turísticos famosos em Paris?"},
    {"role": "assistant", "content": "Paris é famosa pela Torre Eiffel, o Louvre e a Catedral de Notre-Dame."},
    {"role": "user", "content": "E em Roma?"}
  ]
}'
```

➡️ O modelo recebe o histórico e entende que a segunda pergunta também é sobre turismo.

---

## 3. Ajustando parâmetros (temperature e max\_tokens)

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {"role": "user", "content": "Escreva um haicai sobre tecnologia."}
  ],
  "options": {
    "temperature": 0.9,
    "max_tokens": 50
  }
}'
```

➡️ `temperature` alta gera respostas mais criativas.
➡️ `max_tokens` limita o tamanho da resposta.

---

## 4. Streaming de resposta

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {"role": "user", "content": "Resuma a teoria da evolução em 3 frases."}
  ],
  "stream": true
}'
```

➡️ A resposta chega em partes (tokens) em tempo real.

---

## 5. Usando múltiplos roles (multi-turn conversation)

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {"role": "system", "content": "Você é um especialista em programação."},
    {"role": "user", "content": "Explique o que é recursão."},
    {"role": "assistant", "content": "Recursão é uma técnica em que uma função chama a si mesma."},
    {"role": "user", "content": "Pode dar um exemplo em Python?"}
  ]
}'
```

➡️ O histórico permite ao modelo conectar as respostas.

---

# 📝 Resumo rápido

* **`system`** → define regras globais de comportamento.
* **`user`** → entrada do usuário.
* **`assistant`** → resposta anterior do modelo (mantém contexto).
* **`options`** → ajusta comportamento (`temperature`, `top_p`, `max_tokens`, `num_ctx`).
* **`stream`** → habilita resposta em fluxo contínuo.

---

