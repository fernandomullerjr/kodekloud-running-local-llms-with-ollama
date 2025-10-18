
Vamos montar **passo a passo** um **modelo personalizado** para **análise fundamentalista de ativos (ações, FIIs, stocks)**, que interpreta indicadores como P/L, ROE, DY, P/VP, crescimento, endividamento e outros, e responde de forma estruturada se o ativo é de “qualidade” ou não.

---

# 🧠 Objetivo

Criar um modelo local (via **Ollama**) que:

* Recebe o nome ou dados de um ativo (ex: PETR4, AAPL, HGLG11);
* Analisa **fundamentos** (indicadores quantitativos e qualitativos);
* Classifica o ativo como **“bom”, “neutro” ou “ruim”**;
* Justifica a decisão em linguagem natural e formato técnico (Markdown ou JSON).

---

## 🧩 1. Conceito do modelo

O modelo será **derivado de um modelo base**, como `mistral`, `llama3` ou `gemma`.
Usaremos um **Modelfile** para definir:

* Persona: analista fundamentalista;
* Estilo: técnico, estruturado, sem linguagem emocional;
* Parâmetros: temperatura baixa (para consistência analítica);
* Template: estrutura de saída padronizada (Markdown ou JSON).

---

## ⚙️ 2. Exemplo completo de **Modelfile**

Salve como `Modelfile`:

```bash
# Modelfile: analista-fundamentalista
FROM llama3

SYSTEM """
Você é um analista fundamentalista de investimentos. 
Sua função é avaliar empresas, fundos imobiliários e ações com base em seus fundamentos e indicadores.
Use dados quantitativos e qualitativos sempre que disponíveis, e adote uma linguagem técnica e objetiva.

Regras:
- Explique o raciocínio de forma estruturada.
- Classifique o ativo em uma das categorias: "Alta qualidade", "Neutro" ou "Baixa qualidade".
- Baseie-se em métricas como P/L, P/VP, ROE, margem líquida, dívida líquida/EBITDA, payout, crescimento e setor.
- Seja imparcial e nunca dê recomendações de compra/venda — apenas análise.
- Se não houver dados suficientes, diga isso claramente.
"""

PARAMETER temperature 0.4
PARAMETER top_p 0.9
PARAMETER num_predict 512

TEMPLATE """
Ativo: {{ .Prompt }}

Responda com a seguinte estrutura:

**Resumo do Ativo**
- Nome / Ticker:
- Setor:
- Breve descrição:

**Indicadores Fundamentais**
- P/L:
- P/VP:
- ROE:
- Dividend Yield:
- Margem Líquida:
- Crescimento de Lucros:
- Dívida Líquida / EBITDA:
- Outros relevantes:

**Análise Qualitativa**
- Pontos fortes:
- Pontos fracos:
- Considerações sobre o setor:

**Classificação Final**
- Qualidade: Alta | Neutra | Baixa
- Justificativa resumida:
"""
```

---

## 🚀 3. Criando o modelo

No terminal do Ubuntu (WSL):

```bash
ollama create analista-fundamentalista -f Modelfile
```

E para rodar:

```bash
ollama run analista-fundamentalista
```

Teste com prompts como:

```
PETR4
```

ou

```
HGLG11
```

ou ainda:

```
AAPL — analise fundamentalista
```

---

## 🧮 4. Exemplos de interação

### Exemplo 1

**Prompt:**

```
PETR4
```

**Resposta esperada:**

```
**Resumo do Ativo**
- Nome / Ticker: Petrobras (PETR4)
- Setor: Petróleo e Gás
- Breve descrição: Estatal brasileira de energia e exploração de petróleo.

**Indicadores Fundamentais**
- P/L: 4,5
- P/VP: 1,1
- ROE: 27%
- Dividend Yield: 18%
- Margem Líquida: 25%
- Dívida Líquida / EBITDA: 1,2x

**Análise Qualitativa**
- Pontos fortes: alta geração de caixa, margens robustas.
- Pontos fracos: risco político e volatilidade de preços do petróleo.

**Classificação Final**
- Qualidade: Alta
- Justificativa: indicadores de rentabilidade fortes, endividamento controlado e múltiplos atrativos, apesar do risco político.
```

---

## 🧠 5. Melhoria com **formato JSON**

Se você quiser integrar esse modelo com automações (ex: Python, Node, ou dashboard),
mude o `TEMPLATE` para gerar **JSON estruturado**:

```bash
TEMPLATE """
Ativo: {{ .Prompt }}

Responda SOMENTE no formato JSON, seguindo o modelo abaixo:

{
  "ticker": "",
  "setor": "",
  "indicadores": {
    "pl": "",
    "pvp": "",
    "roe": "",
    "dy": "",
    "margem_liquida": "",
    "divida_ebitda": "",
    "crescimento": ""
  },
  "analise": {
    "pontos_fortes": [],
    "pontos_fracos": [],
    "classificacao": "Alta | Neutra | Baixa",
    "justificativa": ""
  }
}
"""
```

💡 Assim, o output pode ser consumido facilmente por automações ou sistemas que fazem ranking de ativos.

---

## 📈 6. Tornando o modelo “fundamentado em dados reais”

O Ollama não tem acesso direto à internet (por padrão),
mas você pode integrá-lo com scripts externos que buscam os dados e os passam no prompt.

### Exemplo via Python:

```python
import requests
import subprocess
import json

def get_dados_acao(ticker):
    url = f"https://api.example.com/acoes/{ticker}"  # pode ser StatusInvest, AlphaVantage, Yahoo Finance etc.
    return requests.get(url).json()

def analisar_ativo(ticker):
    dados = get_dados_acao(ticker)
    prompt = f"{ticker} - {dados}"
    resultado = subprocess.run(["ollama", "run", "analista-fundamentalista"], input=prompt, text=True, capture_output=True)
    return resultado.stdout

print(analisar_ativo("PETR4"))
```

---

## 🧱 7. Boas práticas

✅ **Temperatura baixa (0.3–0.5):** respostas mais objetivas e consistentes.
✅ **Templates padronizados:** facilita automação.
✅ **Use SYSTEM para papel fixo:** evita “drift” de personalidade.
✅ **Integre com APIs externas:** fornece dados reais de indicadores.
✅ **Evite recomendações explícitas de compra/venda.**

---

## 🧩 8. Extensões possíveis

* Adicionar suporte a **fundos imobiliários (FIIs)** e **ações estrangeiras (stocks)**;
* Inserir classificação ESG (Ambiental, Social, Governança);
* Integrar com **base de dados local (SQLite ou CSV)**;
* Criar variação do modelo para **análise técnica** (gráficos e tendências);
* Criar **pipeline com Open WebUI** para dashboards financeiros.

---

## 🏁 9. Conclusão

Esse tipo de modelo é ideal para:

* **Painéis internos** de research;
* **Automação de relatórios financeiros**;
* **Chatbots analíticos** em Open WebUI ou Telegram;
* **Estudos educacionais** sobre fundamentos de ativos.

> 💬 “O diferencial não está em treinar um novo modelo, mas em ensinar um modelo existente a pensar como um analista.”
















--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
- Dia 18/10/2025

Perfeito, Fernando 💪
Vamos montar **dois setups completos**:

1️⃣ **Gemma 2 9B** — modelo geral, excelente para raciocínio analítico e linguagem natural (ideal para uso diário e análise textual).
2️⃣ **FinGPT** — modelo especializado em finanças, ajustado com vocabulário e lógica financeira.

Você poderá rodar ambos no **Ollama** dentro do **WSL** (Ubuntu 22), alternando conforme a necessidade.

---

# ⚙️ 1. Instalação e configuração do Ollama (se ainda não estiver)

> Pule este passo se já tiver o Ollama instalado.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Depois:

```bash
ollama --version
```

Se aparecer algo como `ollama version 0.3.x`, está pronto.

---

# 🧠 2. Instalação do **Gemma 2 9B**

A Google lançou o **Gemma 2 9B** com excelente custo/benefício — leve, raciocínio técnico e suporte multilíngue.

### ✅ Passos:

```bash
ollama pull gemma2:9b
```

Espere o download (~5 GB).

Teste o modelo:

```bash
ollama run gemma2:9b
```

---

## 🧩 Crie o modelo customizado “Analista Fundamentalista – Gemma”

Crie o arquivo:

```bash
nano Modelfile
```

Cole:

```bash
# Modelfile: analista-fundamentalista-gemma
FROM gemma2:9b

SYSTEM """
Você é um analista fundamentalista de investimentos.
Analise ações, FIIs e stocks com base em fundamentos econômicos e financeiros.
Avalie múltiplos como P/L, P/VP, ROE, DY, endividamento e crescimento.
Classifique o ativo como 'Alta qualidade', 'Neutra' ou 'Baixa qualidade'.
Não faça recomendações de compra/venda.
"""

PARAMETER temperature 0.4
PARAMETER top_p 0.9
PARAMETER num_predict 512

TEMPLATE """
Ativo: {{ .Prompt }}

Responda com a estrutura:

**Resumo do Ativo**
**Indicadores Fundamentais**
**Análise Qualitativa**
**Classificação Final**
"""
```

Salve e crie o modelo:

```bash
ollama create analista-fundamentalista-gemma -f Modelfile
```

Execute:

```bash
ollama run analista-fundamentalista-gemma
```

Teste:

```
PETR4
```

ou

```
HGLG11
```

---

# 💼 3. Instalação e uso do **FinGPT**

O **FinGPT** é um modelo **finetuned** em relatórios, notícias e balanços financeiros.
Ele não está no repositório oficial do Ollama, então você precisará **baixar a versão compatível em `.gguf`** e importá-la.

---

## 🧩 A) Baixando o modelo (via Hugging Face)

Acesse o Hugging Face e busque o repositório:

🔗 [https://huggingface.co/FinGPT](https://huggingface.co/FinGPT)
ou
🔗 [https://huggingface.co/FinanceAI/finma-7b](https://huggingface.co/FinanceAI/finma-7b)

Baixe o arquivo `.gguf` (ex: `fingpt-mistral-7b.Q4_K_M.gguf`) — ele costuma ter de 4 a 8 GB.

Copie para o diretório do Ollama:

```bash
sudo mkdir -p /usr/share/ollama/models
sudo cp fingpt-mistral-7b.Q4_K_M.gguf /usr/share/ollama/models/
```

---

## 🧩 B) Criando o modelo no Ollama

Crie o arquivo:

```bash
nano Modelfile
```

Cole:

```bash
# Modelfile: analista-fundamentalista-fingpt
FROM ./fingpt-mistral-7b.Q4_K_M.gguf

SYSTEM """
Você é um analista financeiro especializado em análise fundamentalista.
Sua tarefa é avaliar empresas e fundos com base em seus fundamentos e múltiplos.
Use terminologia financeira correta e linguagem técnica.
Responda de forma estruturada e objetiva.
"""

PARAMETER temperature 0.3
PARAMETER top_p 0.85
PARAMETER num_predict 600

TEMPLATE """
Analisar o ativo: {{ .Prompt }}

Responda no formato:

{
  "ticker": "",
  "setor": "",
  "indicadores": {
    "pl": "",
    "pvp": "",
    "roe": "",
    "dy": "",
    "endividamento": ""
  },
  "analise": {
    "pontos_fortes": [],
    "pontos_fracos": [],
    "qualidade": "Alta | Neutra | Baixa"
  }
}
"""
```

Salve e crie o modelo:

```bash
ollama create analista-fundamentalista-fingpt -f Modelfile
```

Teste:

```bash
ollama run analista-fundamentalista-fingpt
```

Prompt:

```
AAPL — fundamentos e qualidade do ativo
```

---

# 🧩 4. Comparando os dois modelos

| Critério                  | **Gemma 2 9B**                 | **FinGPT (7B)**                   |
| ------------------------- | ------------------------------ | --------------------------------- |
| Domínio de finanças       | Médio (generalista)            | Alto (especializado)              |
| Linguagem natural (PT/EN) | Excelente                      | Boa (treino mais em inglês)       |
| Contexto analítico        | Ótimo                          | Excelente em fundamentos          |
| Tamanho                   | ~5 GB                          | 4–8 GB                            |
| Requisitos de hardware    | CPU i7 / 16 GB RAM mín.        | CPU ou GPU leve                   |
| Melhor uso                | Relatórios, análises completas | Dashboards e automação financeira |

💡 **Dica:**
Use o **Gemma 2 9B** para relatórios explicativos e
o **FinGPT** para análises rápidas e estruturadas (via JSON).

---

# 🔗 5. Integração com APIs (dados reais)

Você pode unir esses modelos a dados reais via Python:

```python
import requests, subprocess, json

ticker = "PETR4"
dados = requests.get(f"https://brapi.dev/api/quote/{ticker}").json()

prompt = f"Analise fundamentalista do ativo {ticker} com base nesses dados:\n{json.dumps(dados, indent=2)}"

result = subprocess.run(
    ["ollama", "run", "analista-fundamentalista-gemma"],
    input=prompt,
    text=True,
    capture_output=True
)

print(result.stdout)
```

Assim, o modelo analisa **dados reais atualizados**.

---

# 🧱 6. Boas práticas

✅ Prefira `temperature 0.3–0.5` para consistência;
✅ Teste prompts curtos (“PETR4 fundamentos”) e longos (“Analise PETR4 com foco em ROE e dívida líquida”);
✅ Mantenha logs dos resultados para validar coerência;
✅ Documente suas variações de Modelfile (v1, v2, etc).

---

# 🏁 7. Resumo final

| Cenário                                   | Modelo ideal         | Comando                                      |
| ----------------------------------------- | -------------------- | -------------------------------------------- |
| Análises explicativas e linguagem natural | **Gemma 2 9B**       | `ollama run analista-fundamentalista-gemma`  |
| Análises estruturadas com JSON            | **FinGPT (Mistral)** | `ollama run analista-fundamentalista-fingpt` |

---

Se quiser, posso gerar **os dois Modelfiles prontos + script Python completo** (com API da Brapi para dados de ações brasileiras) — formatado como um mini-projeto para rodar direto no WSL.
Quer que eu monte esse pacote para você (com arquivos `.Modelfile`, `.py` e exemplo de saída)?




> ollama ls
NAME                  ID              SIZE      MODIFIED
deepseek-r1:70b       d37b54d01a76    42 GB     4 weeks ago
deepseek-r1:latest    6995872bfe4c    5.2 GB    6 weeks ago
> ollama pull gemma2:9b
pulling manifest
pulling ff1d1fc78170:  27% ▕███████████████                                           ▏ 1.5 GB/5.4 GB   14 MB/s   4m34s


ollama pull gemma2:9b





> cd /home/fernando/cursos/ia-inteligencia-artificial/kodekloud-running-local-llms-with-ollama/modelo-customizado
> ollama create analista-fundamentalista-gemma -f Modelfile
gathering model components
using existing layer sha256:ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373
using existing layer sha256:097a36493f718248845233af1d3fefe7a303f864fae13bc31a3a9704229378ca
creating new layer sha256:87cd0771a511c1b2f2fb949937f06ecb6c33b5f2d8364285f476a34e9fafa52e
creating new layer sha256:846f6ee8cf2c24d89e566964df738b9f28202cd5bfa6cec1f0cc92d88a39f441
creating new layer sha256:619e1959902b73a513da9f715b9740056499aa57e5f75b5a87f419726aa0dced
writing manifest
success




- Resultado fraco:
NÃO TRAZ INDICADORES, NEM DE EXEMPLO
DADOS GENÉRICOS DEMAIS.


> ollama run analista-fundamentalista-gemma
>>> PETR4
**Riscos e Oportunidades**

##  PETR4 - Petrobras (Petróleo Brasileiro S.A.)

**Resumo do Ativo:**

Petrobras é a maior empresa brasileira de petróleo e gás natural, com operações em exploração, produção, refino,
transporte, comercialização e distribuição de combustíveis. A empresa possui ativos em diversos países, incluindo
Brasil, Estados Unidos, Argentina, Chile, Peru e Angola.

**Indicadores Fundamentais:**

* **ROE (Retorno sobre o Patrimônio Líquido):**  - Em análise constante devido à volatilidade do setor.
* **ROA (Retorno sobre Ativos):** - Em análise constante devido à volatilidade do setor.
* **P/L (Preço por Lucro):** - Em análise constante devido à volatilidade do setor.
* **Dividendo:** Petrobras tem histórico de pagamento de dividendos, mas a política pode variar com os resultados
e cenário econômico.

**Análise Qualitativa:**

* **Vantagens:**
    * Posição dominante no mercado brasileiro de petróleo e gás natural.
    * Ampla rede de infraestrutura logística.
    * Diversidade geográfica de operações.
    * Investimentos em energias renováveis.
* **Desvantagens:**
    * Vulnerabilidade a flutuações nos preços do petróleo.
    * Regulamentação governamental complexa e política.
    * Altos custos operacionais.
    * Histórico de escândalos de corrupção.

**Classificação Final:**

A classificação final depende da tolerância ao risco do investidor e da análise individual dos indicadores e
fatores mencionados acima.

**Riscos e Oportunidades:**

* **Riscos:**
    * Flutuações nos preços do petróleo.
    * Mudanças na política energética brasileira.
    * Concorrência acirrada no mercado global de petróleo.
    * Desastres naturais e eventos geopolíticos.
* **Oportunidades:**
    * Crescimento da demanda por energia em países emergentes.
    * Investimentos em tecnologias de produção mais eficientes.
    * Expansão para novos mercados internacionais.
    * Transição para energias renováveis.



**Observações:**

Esta análise é apenas um guia inicial e não deve ser considerada como aconselhamento financeiro profissional. É
importante realizar pesquisas adicionais e consultar um consultor financeiro antes de tomar

>>> Send a message (/? for help)






Feito! Montei um **mini-projeto completo** com scraping da Status Invest (Playwright + fallback requests/bs4) e integração com seu **modelo no Ollama**.

**Download:** [statusinvest_toolkit.zip](sandbox:/mnt/data/statusinvest_toolkit.zip)

### O que vem no pacote

* `statusinvest_scrape.py` — scraper **Playwright** (renderiza JS, recomendado).
* `statusinvest_requests.py` — fallback com **requests + BeautifulSoup**.
* `run_analise.py` — roda o scraper e passa os dados para seu modelo no **Ollama**.
* `Modelfile.gemma` — Modelfile para `gemma2:9b` (analista em Markdown).
* `Modelfile.fingpt` — Modelfile para `.gguf` (FinGPT/Mistral) com saída **JSON**.
* `requirements.txt`, `Makefile`, `README.md`.

### Como usar (resumo)

```bash
# 1) Preparar ambiente
make install

# 2) (Opcional) Criar modelo Gemma
ollama pull gemma2:9b
ollama create analista-fundamentalista-gemma -f Modelfile.gemma

# 3) Scraping (Playwright)
make scrape TICKER=BBAS3

# 4) Analisar com seu modelo
make analise TICKER=BBAS3 MODEL=analista-fundamentalista-gemma
```

Se quiser, ajusto os **rótulos** específicos para FIIs (vacância, P/VP, DY 12m, etc.) e adiciono um target `make scrape-fii TICKER=HGLG11`.
