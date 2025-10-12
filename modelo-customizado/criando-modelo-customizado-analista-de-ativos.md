
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
