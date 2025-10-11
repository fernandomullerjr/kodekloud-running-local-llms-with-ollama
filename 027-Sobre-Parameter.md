
# ⚙️ Seção: **PARAMETER — Ajustando o Comportamento do Modelo**

## 🎯 Objetivo

Compreender como usar a instrução `PARAMETER` no **Modelfile** para ajustar o estilo, a criatividade e o controle das respostas geradas pelo modelo.

---

## 🧩 1. O que é o `PARAMETER`

A instrução **`PARAMETER`** define **valores de configuração** que afetam a **forma como o modelo gera texto**.
Ela permite **refinar o comportamento do LLM**, controlando aspectos como:

* **Criatividade** (temperatura, top_p)
* **Tamanho da resposta** (num_predict)
* **Formatação e paradas** (stop tokens)
* **Controle de performance e contexto**

Exemplo básico:

```bash
PARAMETER temperature 0.7
PARAMETER num_predict 256
PARAMETER stop "Usuário:"
```

---

## 🧠 2. Estrutura e sintaxe

A sintaxe geral é:

```bash
PARAMETER <nome> <valor>
```

Cada parâmetro é independente — você pode definir quantos quiser no Modelfile.

---

## ⚙️ 3. Principais parâmetros suportados

| Parâmetro             | Função                                        | Valor comum  | Descrição prática                                                 |
| --------------------- | --------------------------------------------- | ------------ | ----------------------------------------------------------------- |
| **temperature**       | Grau de criatividade / aleatoriedade          | 0.2 a 1.0    | Valores baixos tornam respostas mais objetivas e determinísticas. |
| **top_p**             | Controle de amostragem (Nucleus Sampling)     | 0.7 a 1.0    | Restringe o modelo a tokens com probabilidade acumulada até *p*.  |
| **num_predict**       | Tamanho máximo da resposta (tokens)           | 128 a 1024   | Define até onde o modelo pode gerar texto.                        |
| **stop**              | Cadeia de caracteres que interrompe a geração | `"Usuário:"` | Faz o modelo parar quando encontra esse texto.                    |
| **repeat_penalty**    | Penaliza repetições excessivas                | 1.0 a 2.0    | Evita que o modelo repita frases ou palavras.                     |
| **presence_penalty**  | Incentiva diversidade de tópicos              | 0.0 a 1.0    | Aumenta chance de introduzir novos temas.                         |
| **frequency_penalty** | Reduz repetição literal                       | 0.0 a 1.0    | Penaliza palavras já usadas.                                      |

---

## 🧪 4. Exemplo prático de aplicação

### Modelfile:

```bash
FROM mistral

SYSTEM """
Você é um assistente técnico da Appmax.
Responda de forma concisa, técnica e sem informalidades.
"""

PARAMETER temperature 0.4
PARAMETER top_p 0.8
PARAMETER num_predict 400
PARAMETER stop "Usuário:"
```

### O que acontece:

* O modelo se torna **mais previsível e preciso** (baixa temperatura);
* Limita o tamanho das respostas (400 tokens);
* Para automaticamente quando o usuário fala novamente;
* Mantém consistência técnica e formal.

---

## 🧮 5. Comparando configurações

| Configuração      | Temperatura                                          | Resultado típico |
| ----------------- | ---------------------------------------------------- | ---------------- |
| `temperature 0.2` | Respostas diretas, repetitivas, com tom profissional |                  |
| `temperature 0.7` | Equilíbrio entre criatividade e foco                 |                  |
| `temperature 1.0` | Respostas criativas, informais, mais livres          |                  |

💡 *Dica:* sempre comece com `temperature=0.7` e ajuste conforme o objetivo do modelo.

---

## 🧱 6. Boas práticas com `PARAMETER`

✅ **Teste incrementalmente** — altere um parâmetro por vez e observe os efeitos.
✅ **Documente** os valores no Modelfile (com comentários).
✅ **Evite valores extremos** — podem causar instabilidade ou truncar respostas.
✅ **Ajuste conforme o tipo de modelo:**

* Modelos pequenos (Mistral, Gemma): temperatura 0.5–0.8
* Modelos grandes (Llama 3, Mixtral): 0.3–0.7

---

## 🧭 7. Exercício de prática

> **Objetivo:** Explorar como `PARAMETER` afeta o estilo do modelo.

1. Crie três Modelfiles idênticos, mas altere a temperatura:

   * `temperature 0.3`
   * `temperature 0.7`
   * `temperature 1.0`
2. Faça a mesma pergunta em todos:

   ```
   Explique o que é aprendizado de máquina em uma frase.
   ```
3. Compare o tom e a consistência das respostas.

---

## 🧩 8. Dica avançada — parâmetros em tempo de execução

Além de definir no Modelfile, você pode **sobrescrever parâmetros ao rodar o modelo**:

```bash
ollama run suporte-tecnico --temperature 0.6 --num-predict 500
```

Isso é útil para **testes rápidos** sem recriar o modelo.

---

## 🧾 9. Conclusão

`PARAMETER` é uma das partes mais poderosas do Modelfile — ele transforma o modelo base em uma **persona ajustada ao contexto de uso**.
Dominar esses ajustes permite criar modelos:

* Mais confiáveis em produção;
* Mais criativos para prototipagem;
* Mais eficientes para suporte e automação.

---


