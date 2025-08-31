 material, focando em
arquitetura
parâmetros
weights in llm
treinamento de ia
context length
embedding length
quantization


---

# 📚 Models and Model Parameters — Versão Avançada

## 1. Arquitetura de Modelos LLM

A **arquitetura** define como o modelo é construído internamente — quais camadas, mecanismos e fluxos de informação ele usa.

* **Transformers**:

  * Base de praticamente todos os LLMs modernos.
  * Possuem camadas de **self-attention** que permitem ao modelo considerar todas as palavras de uma entrada simultaneamente.
* **Variantes**:

  * **Decoder-only** (ex.: GPT, LLaMA, Mistral) → ótima para geração de texto.
  * **Encoder-decoder** (ex.: T5, FLAN-T5) → melhor para tradução, resumo e tarefas seq2seq.
* **Tamanho da arquitetura**:

  * Definido pelo número de **camadas**, **cabeças de atenção** e **dimensão de embeddings**.
  * Modelos maiores → maior capacidade, mas mais consumo de recursos.

---

## 2. Parâmetros do Modelo

Os parâmetros controlam **como o modelo gera texto** e **quais recursos são usados**.

| Parâmetro           | Função                                                         |
| ------------------- | -------------------------------------------------------------- |
| **temperature**     | Controla a aleatoriedade: baixo = previsível, alto = criativo. |
| **top\_p**          | Amostragem baseada em probabilidade cumulativa.                |
| **top\_k**          | Limita a escolha às *k* opções mais prováveis.                 |
| **repeat\_penalty** | Reduz repetições indesejadas.                                  |
| **max\_tokens**     | Limita a saída gerada.                                         |
| **num\_ctx**        | Número de tokens que o modelo pode considerar no contexto.     |
| **seed**            | Garante reprodutibilidade das respostas.                       |

> No Ollama, você pode definir parâmetros no comando `ollama run` ou em um **Modelfile**.

**Exemplo:**
Se você pedir uma receita e colocar `temperature` alto, o modelo pode inventar pratos criativos. Com `temperature` baixo, ele vai te dar a receita mais comum.

---

## 3. Weights in LLM -  Weights (Pesos) — O “Conhecimento Gravado”

Os **weights** (pesos) são os valores numéricos aprendidos durante o **treinamento** do modelo.

* Cada peso representa a **força da conexão** entre dois neurônios.
* Estão distribuídos em milhões ou bilhões de parâmetros.
* Pesos treinados definem **o conhecimento do modelo** — alterar pesos exige **treinamento ou fine-tuning**.
* No Ollama, os weights vêm empacotados no arquivo do modelo (`.bin`, `.gguf`).

Os **weights** são como **livros e receitas** guardados na estante da cozinha:

* Cada peso é um número que representa algo que o modelo aprendeu.
* Durante o treinamento, o modelo “escreve” esses números na memória.
* Mais parâmetros (pesos) = mais conhecimento, mas também mais espaço e processamento.

**Exemplo:**
Um chef experiente (modelo grande) tem milhares de receitas memorizadas. Um chef iniciante (modelo pequeno) sabe menos receitas, mas cozinha mais rápido.

---

## 4. Treinamento de IA (LLMs)

Treinar um LLM envolve várias etapas:

1. **Pré-treinamento**

   * O modelo aprende padrões de linguagem com **grandes quantidades de texto**.
   * Objetivo: prever a próxima palavra dado um contexto.

2. **Fine-tuning**

   * Ajuste fino com dados específicos (jurídico, médico, programação etc.).
   * Pode ser **full fine-tuning** (re-treinar todos os pesos) ou **LoRA** (ajustar apenas pequenas camadas).

3. **Instrução e alinhamento**

   * Técnicas como RLHF (Reinforcement Learning from Human Feedback) para ajustar comportamento.

> No contexto do **Ollama**, você normalmente não treina do zero — utiliza modelos já treinados e, se necessário, faz fine-tuning ou adapta via Modelfiles.

Treinar um modelo é como **ensinar um chef**:

1. **Pré-treinamento**:
   O chef lê milhares de receitas de diferentes tipos.

2. **Fine-tuning**:
   Depois, ele faz um curso especializado (por exemplo, só comida japonesa).

3. **Alinhamento**:
   Ele aprende a conversar de forma educada e seguir regras (RLHF — “feedback humano”).

**Exemplo:**
No Ollama, você normalmente baixa um chef já treinado (modelo pronto) e só ajusta como ele trabalha (parâmetros).

---

## 5. Context Length

O **comprimento de contexto** (context length ou `num_ctx`) é a quantidade de tokens que o modelo consegue considerar em uma única janela de atenção.

* **Tokens**: partes de palavras (ex.: "computador" → "compu", "tador").
* Quanto maior o `context length`, mais informação passada anteriormente o modelo consegue lembrar.
* Limitações:

  * Mais contexto = mais memória RAM usada.
  * Modelos pequenos podem ter 2k a 4k tokens, modelos avançados chegam a 128k ou mais.

---

## 6. Embedding Length — “O DNA das Palavras”

O **embedding length** (dimensão do embedding) é o tamanho do vetor numérico usado para representar cada token.

* Ex.: se o embedding length = 4096, cada token é convertido em um vetor de 4096 números.
* Impacta:

  * **Capacidade de representação** → vetores maiores capturam nuances mais ricas.
  * **Uso de memória** → vetores maiores ocupam mais espaço.
* É definido pela arquitetura do modelo e **não pode ser alterado** sem re-treinamento.

O **embedding length** é como o **código genético** das palavras:

* Cada palavra é transformada em um vetor (lista de números).
* O tamanho desse vetor é o **embedding length**.
* Vetores maiores guardam mais detalhes, mas ocupam mais espaço.

**Exemplo:**
Se você descreve uma maçã com apenas 3 palavras (“vermelha, doce, redonda”), a informação é limitada. Com 50 palavras, você descreve muito melhor.

---

## 7. Quantization (Quantização) — “Comprimir para Caber”

A **quantização** reduz a precisão numérica dos pesos para economizar memória e acelerar a execução.

* **Precisões comuns**:

  * **FP16** (16-bit floating point) → bom equilíbrio.
  * **INT8** (8-bit integer) → menor consumo, perda mínima de qualidade.
  * **INT4** (4-bit integer) → extremamente leve, mas pode perder qualidade perceptível.
* Benefícios:

  * Menor uso de RAM e VRAM.
  * Modelos grandes podem rodar em hardware mais fraco.
* No Ollama, modelos `.gguf` já podem vir quantizados (`Q4_0`, `Q5_K_M` etc.).

A **quantização** é como **reduzir a resolução de uma foto**:

* Mantém a ideia geral, mas ocupa menos espaço.
* Troca números grandes (ex.: 32 bits) por menores (ex.: 8 ou 4 bits).
* Ganha velocidade e economiza memória, com pequena perda de qualidade.

**Exemplo:**
Foto em **4K** (modelo FP32) → ocupa muito espaço e é super nítida.
Foto em **HD** (modelo INT8) → ocupa menos espaço e ainda é boa.
Foto muito comprimida (INT4) → super leve, mas perde detalhes.

---

## 8. Resumo com Analogias

| Conceito         | Analogia                  | Papel no LLM                                |
| ---------------- | ------------------------- | ------------------------------------------- |
| Arquitetura      | Projeto da casa           | Define a estrutura do modelo                |
| Parâmetros       | Configuração do forno     | Controlam como ele responde                 |
| Weights          | Livros de receitas        | Conhecimento aprendido                      |
| Treinamento      | Curso do chef             | Ensina o modelo a agir                      |
| Context Length   | Memória de curto prazo    | Quantidade de informação lembrada           |
| Embedding Length | DNA das palavras          | Como palavras são representadas             |
| Quantization     | Reduzir resolução da foto | Menos recursos, possível perda de qualidade |

---
