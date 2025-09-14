
# Lab: Working With Ollama API




## PENDENTE

    Baixar deepseek de 70B que ocupa 40GB.

    Testar deepseek de 70B. Utilizar o JQ para formatar o JSON.






# lab

The Ollama service is running on the ollama-server.

To access the server, use the following SSH command:

ssh ai-engineer@$IP_ADDRESS




2 / 5

Ollama Labs

Which one of the following models is present on the system right now?

ai-engineer@ollama-server-1757812065:~$ ollama ls
NAME         ID              SIZE      MODIFIED           
qwen:0.5b    b5dc5e784f2a    394 MB    About a minute ago    
ai-engineer@ollama-server-1757812065:~$ date
Sun Sep 14 01:12:18 UTC 2025
ai-engineer@ollama-server-1757812065:~$ 





3 / 5

Ollama Labs

Use curl to send a message to the /generate endpoint of the API, asking Who invented computing? using the qwen:0.5b model. Store the command in the /home/ai-engineer/q3.

Is the right command stored in the /home/ai-engineer/q3?


~~~~bash
# Ollama via CURL

curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen:0.5b",
    "prompt": "Who invented computing?",
    "stream": false
  }'
~~~~


vi /home/ai-engineer/q3


ai-engineer@ollama-server-1757812065:~$ curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen:0.5b",
    "prompt": "Who invented computing?",
    "stream": false
  }'
{"model":"qwen:0.5b","created_at":"2025-09-14T01:14:07.919438333Z","response":"The first known use of computing was in the 18th century by German mathematician Carl Friedrich Gauss. Gauss used his skills as a musician and mathematician to create complex algorithms that could be used for various purposes, such as scientific calculation, data analysis, and artificial intelligence.","done":true,"done_reason":"stop","context":[151644,872,198,15191,35492,24231,30,151645,198,151644,77091,198,785,1156,3881,990,315,24231,572,304,279,220,16,23,339,9294,553,5938,20976,1103,21998,79374,93216,13,93216,1483,806,7361,438,264,38744,323,20976,1103,311,1855,6351,25185,429,1410,387,1483,369,5257,9895,11,1741,438,12344,21937,11,821,6358,11,323,20443,11229,13],"total_duration":8958262311,"load_duration":2429705802,"prompt_eval_count":12,"prompt_eval_duration":395795748,"eval_count":57,"eval_duration":6130396935}ai-engineer@ollama-server-1757812065:~$ vi /home/ai-engineer/q3
ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ cat /home/ai-engineer/q3
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen:0.5b",
    "prompt": "Who invented computing?",
    "stream": false
  }'
ai-engineer@ollama-server-1757812065:~$ date
Sun Sep 14 01:14:41 UTC 2025
ai-engineer@ollama-server-1757812065:~$ 











4 / 5

Ollama Labs

Send the same Who invented computing? message, but don’t stream the output this time. Store the command in the /home/ai-engineer/q4.

Is the right command stored in the /home/ai-engineer/q4?

~~~~bash
# Ollama via CURL

curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen:0.5b",
    "prompt": "Who invented computing?",
    "stream": false
  }'
~~~~


vi /home/ai-engineer/q4









5 / 5

Ollama Labs

Send a request to the /chat endpoint of the API this time with the following chat history:

    User: Who invented computing?
    Assistant: Charles Babbage
    User: When?

Don’t stream the output. Store the command in the /home/ai-engineer/q5.

Is the right command stored in the /home/ai-engineer/q5?


```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {"role": "user", "content": "Who invented computing?"}
    {"role": "assistant", "content": "Charles Babbage"},
    {"role": "user", "content": "When?"}
  ],
  "stream": false
}'
```


erro

ai-engineer@ollama-server-1757812065:~$ curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {"role": "user", "content": "Who invented computing?"}
    {"role": "assistant", "content": "Charles Babbage"},
    {"role": "user", "content": "When?"}
  ],
  "stream": false
}'
{"error":"invalid character '{' after array element"}ai-engineer@ollama-server-1757812065:~$ 



- JSON corrigido

curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {"role": "user", "content": "Who invented computing?"},
    {"role": "assistant", "content": "Charles Babbage"},
    {"role": "user", "content": "When?"}
  ],
  "stream": false
}'





ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {"role": "user", "content": "Who invented computing?"},
    {"role": "assistant", "content": "Charles Babbage"},
    {"role": "user", "content": "When?"}
  ],
  "stream": false
}'
{"model":"qwen:0.5b","created_at":"2025-09-14T01:23:23.62947454Z","message":{"role":"assistant","content":"In 1845, Charles Babbage invented the first practical computer."},"done_reason":"stop","done":true,"total_duration":4863688713,"load_duration":2368094742,"prompt_eval_count":25,"prompt_eval_duration":783244293,"eval_count":17,"eval_duration":1707903413}ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ date
Sun Sep 14 01:23:26 UTC 2025
ai-engineer@ollama-server-1757812065:~$ 


vi /home/ai-engineer/q5


- DEU ERRADA:


ai-engineer@ollama-server-1757812065:~$ vi /home/ai-engineer/q5
ai-engineer@ollama-server-1757812065:~$ cat /home/ai-engineer/q5
curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {"role": "user", "content": "Who invented computing?"},
    {"role": "assistant", "content": "Charles Babbage"},
    {"role": "user", "content": "When?"}
  ],
  "stream": false
}'
ai-engineer@ollama-server-1757812065:~$ 




- VERIFICANDO A SOLUÇÃO

Step 1: Construct the curl Command

To send a message to the /chat endpoint with the provided chat history using the qwen:0.5b model without streaming, use:

curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {
      "role": "user",
      "content": "who invented computing?"
    },
    {
      "role": "assistant",
      "content": "Charles Babbage"
    },
    {
      "role": "user",
      "content": "when?"
    }
  ],
  "stream": false
}'

Step 2: Save the Command in the /home/ai-engineer/q5

Store the command in the file located at /home/ai-engineer/q5 by executing the following command:

vi /home/ai-engineer/q5

Then, insert the following text:

curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {
      "role": "user",
      "content": "who invented computing?"
    },
    {
      "role": "assistant",
      "content": "Charles Babbage"
    },
    {
      "role": "user",
      "content": "when?"
    }
  ],
  "stream": false
}'





Entendi o que aconteceu ✅

O seu comando está **correto do ponto de vista técnico**, mas o sistema do curso provavelmente está validando **a resposta esperada exatamente como no enunciado**, incluindo:

* As letras minúsculas (`who invented computing?`, `when?`)
* O formato das quebras de linha (cada chave em uma nova linha, como no exemplo do enunciado).

---

## 🔎 Diferença entre sua resposta e a esperada

* **Sua versão**:

```json
{"role": "user", "content": "Who invented computing?"},
{"role": "user", "content": "When?"}
```

* **Esperada** (no exercício):

```json
{
  "role": "user",
  "content": "who invented computing?"
},
{
  "role": "user",
  "content": "when?"
}
```

Note:

* O curso pediu **tudo em minúsculas**.
* O curso pediu o **formato multilinha** (estilo identado).

---

## ✅ Como corrigir

Edite novamente o arquivo:

```bash
vi /home/ai-engineer/q5
```

E deixe **exatamente assim**:

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {
      "role": "user",
      "content": "who invented computing?"
    },
    {
      "role": "assistant",
      "content": "Charles Babbage"
    },
    {
      "role": "user",
      "content": "when?"
    }
  ],
  "stream": false
}'
```

Depois verifique com:

```bash
cat /home/ai-engineer/q5
```

---






- PASSANDO EXATAMENTE ASSIM, O CURSO ACUSOU COMO CORRETA A QUESTÃO:

~~~~bash

ai-engineer@ollama-server-1757812065:~$ vi /home/ai-engineer/q5
ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ cat /home/ai-engineer/q5
curl http://localhost:11434/api/chat -d '{
  "model": "qwen:0.5b",
  "messages": [
    {
      "role": "user",
      "content": "who invented computing?"
    },
    {
      "role": "assistant",
      "content": "Charles Babbage"
    },
    {
      "role": "user",
      "content": "when?"
    }
  ],
  "stream": false
}'

ai-engineer@ollama-server-1757812065:~$ 
ai-engineer@ollama-server-1757812065:~$ date
Sun Sep 14 01:28:32 UTC 2025
ai-engineer@ollama-server-1757812065:~$ 
~~~~