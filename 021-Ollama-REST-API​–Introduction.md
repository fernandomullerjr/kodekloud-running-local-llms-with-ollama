# Ollama REST API​ – Introduction

---

# 📚 Ollama REST API – Introdução

## 1. O que é a Ollama REST API?

A **Ollama REST API** permite enviar e receber dados de modelos de linguagem (LLMs) de forma programática usando **HTTP**.
Isso significa que você pode integrar modelos do Ollama em:

* Aplicações web
* Scripts e automações
* Interfaces gráficas (ex.: Open WebUI)
* Serviços backend

---

## 2. Fluxo de Comunicação

### 🔄 **Fluxo básico**

```
Usuário → Aplicativo → Ollama API → Modelo LLM → Ollama API → Aplicativo → Usuário
```

**Passo a passo:**

1. **Usuário**: envia uma pergunta ou comando.
2. **App**: recebe o input e faz uma requisição HTTP para o Ollama (`/api/generate` ou `/api/chat`).
3. **LLM**: processa a entrada e gera a resposta.
4. **Ollama API**: retorna a resposta ao aplicativo.
5. **App**: exibe o resultado para o usuário.

💡 *Essa arquitetura permite que a lógica da aplicação e a IA fiquem desacopladas — você pode trocar o modelo sem mudar o app.*

---

## 3. Endpoints principais

### 📌 3.1 Listar modelos instalados

```bash
GET /api/tags
```

```bash
curl http://localhost:11434/api/tags
```

---

### 📌 3.2 Gerar texto com um prompt simples

```bash
POST /api/generate
```

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Explique o que é aprendizado de máquina."
}'
```

---

### 📌 3.3 Conversa com contexto (modo chat)

```bash
POST /api/chat
```

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama2",
  "messages": [
    {"role": "system", "content": "Você é um especialista em tecnologia."},
    {"role": "user", "content": "Explique o conceito de blockchain."}
  ]
}'
```

---

### 📌 3.4 Baixar um modelo

```bash
POST /api/pull
```

```bash
curl http://localhost:11434/api/pull -d '{
  "name": "mistral"
}'
```

---

### 📌 3.5 Remover um modelo

```bash
DELETE /api/delete
```

```bash
curl -X DELETE http://localhost:11434/api/delete -d '{
  "name": "mistral"
}'
```

---

### 📌 3.6 Gerar resposta com parâmetros avançados

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Liste 5 ideias de negócio para 2025",
  "options": {
    "temperature": 0.8,
    "top_p": 0.9,
    "num_ctx": 4096
  }
}'
```

---

## 4. Exemplo de fluxo em código (JavaScript)

```javascript
async function askOllama(prompt) {
  const res = await fetch("http://localhost:11434/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "llama2",
      prompt: prompt,
      stream: false
    })
  });

  const data = await res.json();
  console.log("Resposta do LLM:", data.response);
}

askOllama("Explique física quântica em termos simples");
```

---

## 5. Boas práticas de uso

* **Confirme se o Ollama está rodando** (`ollama serve`).
* **Sempre teste** `GET /api/tags` antes para verificar modelos disponíveis.
* Use `stream: true` para **respostas em tempo real**.
* Ajuste `temperature` e `top_p` para controlar criatividade.
* Limite `max_tokens` para evitar respostas muito longas.
* Separe **lógica de aplicação** e **processamento LLM** para maior flexibilidade.

---

## 6. Resumo da Aula

| Conceito              | Explicação                                                            |
| --------------------- | --------------------------------------------------------------------- |
| **Fluxo**             | Usuário → App → API → LLM → API → App → Usuário                       |
| **API Base**          | `http://localhost:11434`                                              |
| **Endpoints chave**   | `/api/tags`, `/api/generate`, `/api/chat`, `/api/pull`, `/api/delete` |
| **Geração de texto**  | `POST /api/generate` com `prompt`                                     |
| **Chat com contexto** | `POST /api/chat` com `messages`                                       |
| **Parâmetros úteis**  | `temperature`, `top_p`, `num_ctx`, `max_tokens`                       |
| **Boas práticas**     | Testar conexão, controlar contexto, usar streaming quando possível    |

---




# 📌 Campos e Parâmetros da Ollama REST API

## 1. Campos Comuns (presentes na maioria das chamadas)

| Campo        | Tipo    | Obrigatório? | Descrição                                                                                                          | Exemplo                                             |
| ------------ | ------- | ------------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| **model**    | string  | ✅            | Nome do modelo instalado no Ollama. Deve aparecer no `/api/tags`.                                                  | `"model": "llama2"`                                 |
| **prompt**   | string  | ⚠️\*         | Texto ou instrução enviada para o modelo (usado em `/api/generate`).                                               | `"prompt": "Explique a teoria da relatividade"`     |
| **messages** | array   | ⚠️\*         | Lista de mensagens para manter contexto de conversa (usado em `/api/chat`).                                        | `[{"role":"user","content":"Olá"}]`                 |
| **stream**   | boolean | ❌            | Se `true`, envia resposta em fluxo contínuo (streaming). Se `false`, espera a resposta completa antes de devolver. | `"stream": true`                                    |
| **options**  | objeto  | ❌            | Conjunto de parâmetros para controlar comportamento do modelo.                                                     | `"options": {"temperature":0.7}`                    |
| **system**   | string  | ❌            | Prompt de sistema (define comportamento global do modelo).                                                         | `"system": "Você é um especialista em tecnologia."` |
| **template** | string  | ❌            | Modelo de template para formatar a entrada.                                                                        | `"template": "{{prompt}}"`                          |
| **context**  | array   | ❌            | Dados binários codificados que representam histórico do modelo (tokens).                                           | Não comum para iniciantes.                          |

⚠️ *Ou `prompt` ou `messages` devem ser usados, dependendo do endpoint.*

---

## 2. Campos no Endpoint `/api/generate`

Este endpoint é usado para **gerar texto sem manter histórico de conversa**.

```jsonc
{
  "model": "llama2",
  "prompt": "Liste 3 curiosidades sobre inteligência artificial",
  "stream": false,
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "num_ctx": 4096,
    "repeat_penalty": 1.1,
    "stop": ["\n\n"]
  }
}
```

### Campos do `options` mais comuns:

| Campo               | Tipo  | Padrão            | Descrição                                                                       |
| ------------------- | ----- | ----------------- | ------------------------------------------------------------------------------- |
| **temperature**     | float | 0.8               | Controla criatividade: baixo = respostas mais objetivas, alto = mais criativas. |
| **top\_p**          | float | 0.9               | Filtra palavras pela soma de probabilidades.                                    |
| **top\_k**          | int   | 40                | Considera apenas as *k* palavras mais prováveis.                                |
| **repeat\_penalty** | float | 1.1               | Penaliza repetições excessivas.                                                 |
| **num\_ctx**        | int   | depende do modelo | Janela de contexto (tokens que o modelo “lembra”).                              |
| **max\_tokens**     | int   | ilimitado         | Limita tamanho da resposta.                                                     |
| **stop**            | array | \[]               | Lista de sequências que interrompem a geração.                                  |

---

## 3. Campos no Endpoint `/api/chat`

Este endpoint é usado para **manter histórico e simular chat**.

```jsonc
{
  "model": "llama2",
  "messages": [
    { "role": "system", "content": "Você é um assistente educado e objetivo." },
    { "role": "user", "content": "Quem descobriu o Brasil?" },
    { "role": "assistant", "content": "O Brasil foi oficialmente descoberto em 1500 por Pedro Álvares Cabral." }
  ],
  "stream": false,
  "options": {
    "temperature": 0.2
  }
}
```

### Valores para `role`:

* `"system"` → Define regras e contexto global.
* `"user"` → Mensagens enviadas pelo usuário.
* `"assistant"` → Respostas do modelo.

---

## 4. Campos em `/api/pull` (baixar modelo)

```json
{
  "name": "mistral",
  "stream": true
}
```

* **name** → Nome do modelo (pode incluir tag de versão).
* **stream** → Recebe progresso de download em tempo real.

---

## 5. Campos em `/api/delete` (remover modelo)

```json
{
  "name": "mistral"
}
```

* **name** → Nome do modelo a ser removido.

---

## 6. Resumo rápido dos campos

| Campo      | Onde usar                     | Função principal                |
| ---------- | ----------------------------- | ------------------------------- |
| `model`    | todos                         | Define qual LLM será usado      |
| `prompt`   | `/api/generate`               | Entrada direta de texto         |
| `messages` | `/api/chat`                   | Histórico de conversas          |
| `stream`   | todos                         | Ativa streaming de resposta     |
| `options`  | `/api/generate` e `/api/chat` | Ajusta comportamento            |
| `system`   | `/api/chat`                   | Define o papel e regras do LLM  |
| `template` | `/api/generate`               | Formata entrada                 |
| `context`  | avançado                      | Mantém estado entre requisições |

---











-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------
-------------------------------------------------------------------------

- Comando para testar


```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1:latest",
    "prompt": "Explique o que é aprendizado de máquina.",
    "stream": false
  }'
```


resposta veio zoada:

~~~~bash
^C
> curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1:latest",
    "prompt": "Explique o que é aprendizado de máquina.",
    "stream": false
  }'
{"model":"deepseek-r1:latest","created_at":"2025-09-07T01:34:37.530647482Z","response":"\u003cthink\u003e\nOkay, the user asked \"Explicar o que é aprendizado de máquina.\" which translates to explaining what machine learning is in Portuguese. Let me start by understanding their query.\n\nFirst, they might be a Portuguese speaker looking for a clear definition of machine learning. The question seems straightforward but maybe they need it broken down into simple terms. They could be someone new to the field, perhaps a student or a professional curious about AI and ML trends.\n\nSince they're asking in Portuguese, I should make sure my response is also in Portuguese to match their language preference. But wait, the example provided was in English. Hmm, maybe I need to provide both? No, the user wants an explanation in Portuguese according to their query's requirement.\n\nBut let me think deeper. The term \"aprendizado de máquina\" is specific to Brazilian Portuguese because of Google Translate examples. So confirming they're likely from Brazil or speak that variant. They might not be familiar with technical jargon, so avoiding complex terms unless necessary.\n\nNow, why are they asking this? Could be for a school project, personal interest, or maybe considering entering the field and wants foundational knowledge. The explanation should cover basics without diving too deep into mathematics or programming details unless asked.\n\nThey might need to distinguish ML from other AI concepts like deep learning or neural networks. Also, clarifying that it's not just about data processing but building models with predictive power is important. Highlighting examples in Portuguese could help them relate better—like classificando spam emails, previsão de vendas, etc.\n\nAre they possibly looking for career opportunities related to ML? Or maybe how it applies to everyday technologies like chatbots or recommendation systems? Including real-world applications can make the explanation more engaging and show practical relevance.\n\nI should structure the answer starting with a simple definition, then differentiate between machine learning and artificial intelligence. Next, explain that it's about building models from data, followed by examples of tasks. Then describe how ML works in steps: data collection, model building, training, prediction, iteration.\n\nNeed to avoid markdown as per instructions, so keep the response natural with Portuguese terms. Make sure key points are covered without being too technical. Maybe mention supervised and unsupervised learning briefly but not go into detail unless necessary.\n\nCheck if there's a deeper need: perhaps they want to know how ML is used in their industry or if it's accessible for someone without advanced math skills. But since the query is just about defining what machine learning is, sticking to that scope while providing enough context for understanding.\n\nAlso, ensuring clarity on why data is essential and how models improve over time. Emphasize adaptability as a key feature. Maybe touch upon ethical considerations briefly? Not unless specified, but if they're asking broadly, it might be implied. However, the user hasn't indicated that, so better to keep focused on definition.\n\nFinally, summarize ML's role in AI and its practical benefits. Make sure the explanation is approachable for someone unfamiliar with the subject.\n\u003c/think\u003e\nOkay, vamos explicar o Aprendizado de Máquina em termos simples:\n\n**O que é Aprendizado de Máquina?**\n\nÉ um subcampo da **Inteligência Artificial (IA)** que se concentra em *ensinar computadores a aprender tarefas sem programação explícita*.\n\nImagine: você quer fazer uma máquina realizar alguma coisa inteligente, como classificar fotos, prever resultados futuros, ou identificar padrões complexos. Ao invés de dar instruções detalhadas para cada caso (como um programa tradicional), você dá a ela **exemplos** e faz com que ela \"aprenda\" com esses exemplos.\n\nPense assim:\n\n1.  **Dado:** Você fornece dados ao computador.\n2.  **Objetivo:** Você diz qual o objetivo desejado (por exemplo, classificar os dados, prever algo).\n3.  **Aprendizado:** O computador analisa os dados e tenta encontrar padrões ou regras que permitam alcançar esse objetivo.\n\n**Como Funciona Básico:**\n\n*   Você coleta uma quantidade grande de **dados** relacionados ao problema (ex.: muitas fotos de gatos anotadas como \"gato\", muitas linhas de vendas passadas, dados sobre alunos e suas notas).\n*   O computador cria um modelo matemático baseado nesses dados. Esse modelo é uma representação simplificada das regras que o conectam.\n*   Usando esse modelo, o computador pode fazer **previsões** ou **classificações** em novos dados que ele nunca viu antes.\n\n**Exemplos Típicos de Tarefas do Aprendizado de Máquina:**\n\n*   **Classificação:** Decidir se um e-mail é spam ou não, identificar uma imagem como gato/cachorro/humano, analisar o sentimento de uma avaliação de produto (positivo/negativo).\n*   **Regressão:** Prever quanto um imóvel vai custar com base em características, estimar a nota média de um filme no futuro.\n*   **Clusterização/Análise de Agrupamento:** Agrupar documentos semanais ou clientes similares (ex.: encontrar grupos de compradores com comportamentos diferentes).\n*   **Geração de Conteúdo:** Criar textos, imagens, música seguindo padrões aprendidos.\n\n**Em Resumo:**\n\nO Aprendizado de Máquina é a capacidade dos computadores de *aprender e melhorar com experiência*, ajustando modelos internos a partir de dados. Ele permite que máquinas executem tarefas complexas, tornando-se mais eficientes ou acuradas ao longo do tempo à medida que recebem mais informações. É o processo pelo qual a IA vai além da programação rígida e consegue se adaptar e aprender com os dados que processa.","done":true,"done_reason":"stop","context":[151669,43953,2372,297,1709,3958,67346,25846,409,135702,13,151670,151667,198,32313,11,279,1196,4588,330,8033,415,277,297,1709,3958,67346,25846,409,135702,1189,892,46918,311,25021,1128,5662,6832,374,304,42188,13,6771,752,1191,553,8660,862,3239,382,5338,11,807,2578,387,264,42188,18601,3330,369,264,2797,7271,315,5662,6832,13,576,3405,4977,30339,714,7196,807,1184,432,10865,1495,1119,4285,3793,1
709,28730,446,20114,23494,336,259,546,14847,6351,300,11,21145,4883,7806,9870,30369,5385,288,5908,1613,324,11107,14845,1293,78,653,23230,3784,71528,1709,2166,65,336,9870,64066,13,28024,297,58896,27525,5841,264,43090,39486,83669,2994,2025,12967,435,70337,4744,384,390,46106,511,10515,277,384,92717,469,2643,27945,1709,1882,64,13],"total_duration":31409136126,"load_duration":53409271,"prompt_eval_count":12,"prompt_eval_duration":4078852,"eval_count":1243,"eval_duration":31350779663}%              
 ~                      
~~~~




ollama run deepseek-r1:70b

ollama pull deepseek-r1:70b


ollama pull deepseek-r1:70b


> df -h
Filesystem      Size  Used Avail Use% Mounted on
none            7.8G     0  7.8G   0% /usr/lib/modules/5.15.167.4-microsoft-standard-WSL2
none            7.8G  4.0K  7.8G   1% /mnt/wsl
drivers         150G  135G   16G  90% /usr/lib/wsl/drivers
/dev/sdb       1007G   45G  912G   5% /
none            7.8G  120K  7.8G   1% /mnt/wslg
none            7.8G     0  7.8G   0% /usr/lib/wsl/lib
rootfs          7.8G  2.4M  7.8G   1% /init
none            7.8G  6.3M  7.8G   1% /run
none            7.8G     0  7.8G   0% /run/lock
none            7.8G     0  7.8G   0% /run/shm
tmpfs           4.0M     0  4.0M   0% /sys/fs/cgroup
none            7.8G  468K  7.8G   1% /mnt/wslg/versions.txt
none            7.8G  468K  7.8G   1% /mnt/wslg/doc
C:\             150G  135G   16G  90% /mnt/c
G:\             782G  483G  299G  62% /mnt/g
snapfuse        128K  128K     0 100% /snap/bare/5


> ollama pull deepseek-r1:70b
pulling manifest
pulling 4cd576d9aa16:   1% ▕                                                                                                               ▏ 297 MB/ 42 GB  8.6 MB/s   1h21m






>
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1:latest",
    "prompt": "Explique COMO FAZER UMA PESQUISA NO GOOGLE.",
    "stream": false
  }' | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 11005    0 10884  100   121    272      3  0:00:40  0:00:39  0:00:01  2299
{
  "model": "deepseek-r1:latest",
  "created_at": "2025-09-07T01:56:16.108534148Z",
  "response": "<think>\nBem, o usuário está pedindo uma explicação sobre como fazer uma pesquisa no Google. Parece ser alguém que está começando a aprender sobre pesquisas eficientes ou talvez precise de um lembrete rápido para otimizar suas habilidades de busca.\n\nVou estruturar minha resposta em etapas claras, pois isso ajuda iniciantes a entenderem o processo passo a passo. Começarei com uma introdução simples para estabelecer contexto antes de mergulhar nos detalhes.\n\nPensando no usuário, provavelmente é um indivíduo sem experiência avançada em pesquisas online, talvez seja um estudante ou alguém aprendendo habilidades digitais. Ele pode não estar familiarizado com todas as ferramentas e recursos que o Google oferece.\n\nA consulta parece bastante direta - apenas sobre como fazer uma pesquisa no Google. Mas vou assumir que ele quer mais do que isso, então vou incluir dicas avançadas também para ir além da resposta básica.\n\nVou abordar isso em partes: primeiro a pesquisa simples, depois as técnicas mais sofisticadas usando operadores de busca e filtros. Usarei exemplos práticos porque pesquisar efetivamente é melhor demonstrado do que explicado por palavras sozinas.\n\nPreciso incluir uma seção sobre verificação de resultados para ensinar o usuário a avaliar a qualidade das informações, já que isso é fundamental mas muitas pessoas não param para pensar nisso. Um exemplo prático pode ajudar aqui - talvez mencionar sites como Google Scholar e Wikipedia com seus respectivos usos.\n\nComo ele escreveu em português simples, minha resposta deve manter um tom amigável e evitar jargões muito técnicos. Vou estruturar cada seção com uma explicação clara seguida por exemplos práticos.\n</think>\nClaro! Fazer uma pesquisa no Google envolve organizar suas palavras-chave de forma eficiente para obter os melhores resultados possíveis. Segue um guia passo a passo:\n\n---\n\n### **1. Defina sua busca**\n- Especifique claramente o que você está procurando (ex: artigo, notícia, tutorial, etc.).\n\n---\n\n### **2. Use palavras-chave relevantes e específicas**\n- Em vez de textos genéricos como \"carro\", use termos mais precisos:\n  - Exemplo: *\"carros elétricos 2024 vantagens\"* (busca sobre carros elétricos recentes).\n\n---\n\n### **3. Entenda os operadores do Google**\n- **`\"\"`** (*dois espaços duplos*): Encontra exatamente as palavras entre aspas.\n  - Exemplo: `\"receitas de bolo\"` (encontrará textos com a frase completa).\n  \n- **`-`**: Exclui resultados que contenham esse termo.\n  - Exemplo: `carros elétricos -preço` (remove mencões ao custo).\n\n- **`OR`**: Combina palavras alternativas em uma busca.\n  - Exemplo: `\"saúde mental\" OR \"bem-estar psicológico\"`.\n\n---\n\n### **4. Aproveite a barra (`/`) para agrupar termos**\n- Use `/` quando desejar que o Google use apenas um dos termos entre as palavras.\n  - Exemplo: `\"/ tecnologia / sustentabilidade\"` (encontra resultados com \"tecnologia\" ou \"sustentabilidade\").\n\n---\n\n### **5. Procure por arquivos específicos**\n- Use `.pdf` ou `.docx`, `.txt`, etc., para filtrar documentos:\n  - Exemplo: `\"exercícios de matemática\" filetype:pdf`.\n\n---\n\n### **6. Especifique o idioma**\n- Adicione `lang:` seguido do código da língua (ex: `pt-BR` ou `es`).\n  - Exemplo: `\"preço do petróleo\" lang:pt` para resultados em português.\n\n---\n\n### **7. Use datas (`date:`)**\n- Encontre informações específicas de um período:\n  - Exemplo: `covid vacina date:2023` (busca sobre vacinas da covid em 2023).\n\n---\n\n### **8. Acesse recursos especializados**\n- Sites como *Google Scholar* para artigos acadêmicos.\n- Redes sociais e blogs relevantes com o parâmetro `site:`:\n  - Exemplo: `site:tweeter.com` para resultados apenas no Twitter.\n\n---\n\n### **9. Filtre os resultados**\n- No menu suspenso do canto superior direito, selecione opções como \"Notícias\", \"Imagens\", \"Videos\" ou \"Arquivos\".\n- Use filtros de data, região e tipo de conteúdo para refinar sua busca.\n\n---\n\n### **10. Verifique a qualidade das informações**\n- Confira os sites (.org, .edu, .com) antes de usar as informações.\n- Exemplo: `site:wikipedia.org` ou `site:government`.\n\n---\n\n### **Exemplo Prático**\nSe você está procurando *\"como fazer uma pesquisa no Google com operadores\",* pode digitar:\n```\n\"pesquisa avançada Google\" -tutorial site:.com\n```\n\nIsso irá mostrar resultados em sites de domínio .com sem incluir tutoriais.\n\n---\n\nSiga essas dicas para melhorar sua produtividade na busca por informações!",
  "done": true,
  "done_reason": "stop",
  "context": [
    151669,
    43953,

    0
  ],
  "total_duration": 39967800915,
  "load_duration": 3830598921,
  "prompt_eval_count": 18,
  "prompt_eval_duration": 247251638,
  "eval_count": 1199,
  "eval_duration": 35888819793
}
>

 ~       


## PENDENTE

    Baixar deepseek de 70B que ocupa 40GB.

    Testar deepseek de 70B. Utilizar o JQ para formatar o JSON.




> ollama run deepseek-r1:70b "me mostre um codigo em python que comunica com api do ollama"
Error: 500 Internal Server Error: model requires more system memory (35.6 GiB) than is available (11.4 GiB)

 ~              