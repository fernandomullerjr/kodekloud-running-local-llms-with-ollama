
# 🎨 Aula: **Customizing Models**

## 🎯 Objetivo

Ao final desta aula, o aluno será capaz de:

* Entender o que significa **customizar um modelo de linguagem**;
* Personalizar modelos via **Modelfile** (prompts, parâmetros, adapters);
* Criar personas e estilos de resposta;
* Compreender boas práticas de versionamento e deploy local.

---

## 🧩 1. O que significa “Customizar um Modelo”

Customizar um modelo é o processo de **ajustar o comportamento, o tom e a função de um LLM** sem precisar reentreinar do zero.

Em vez de treinar novos pesos (como no *fine-tuning*), você:

* Reutiliza um modelo base (ex: `mistral`, `llama3`, `gemma`);
* Adiciona instruções e parâmetros no **Modelfile**;
* Cria um novo modelo “derivado”, com comportamento fixo e controlável.

📘 **Analogia:**

> Assim como um *Dockerfile* define como construir uma imagem,
> o *Modelfile* define como “reprogramar” o modelo base para uma tarefa específica.

---

## 🧠 2. Formas de customização

| Tipo                            | Método                      | Exemplo                                  |
| ------------------------------- | --------------------------- | ---------------------------------------- |
| **1. Persona / Função**         | Alterar `SYSTEM`            | “Você é um professor de Python.”         |
| **2. Estilo de resposta**       | Ajustar `PARAMETER`         | `temperature`, `top_p`, `stop`           |
| **3. Formato de output**        | Usar `TEMPLATE`             | Forçar respostas em JSON, Markdown, etc. |
| **4. Contexto / comportamento** | Inserir `SYSTEM` multilinha | Regras de ética, foco em produto, etc.   |
| **5. Adaptação leve (LoRA)**    | Incluir `ADAPTER`           | `ADAPTER lora://suporte-appmax`          |

---

## ⚙️ 3. Estrutura base para customização

Exemplo de um Modelfile personalizado:

```bash
# Modelfile: appmax-suporte
FROM mistral

SYSTEM """
Você é um assistente técnico da Appmax.
Responda de forma profissional, objetiva e sempre em português.
"""

PARAMETER temperature 0.5
PARAMETER top_p 0.9
PARAMETER num_predict 512

TEMPLATE """
Usuário: {{ .Prompt }}
Suporte Técnico:
"""
```

Depois:

```bash
ollama create appmax-suporte -f Modelfile
ollama run appmax-suporte
```

---

## 🎭 4. Criando Personas

Você pode moldar o modelo para “interpretar papéis” específicos.
Cada persona define *voz, estilo e comportamento*.

### Exemplo 1 — Professor de Python

```bash
SYSTEM "Você é um professor de Python que explica conceitos de forma simples e prática."
PARAMETER temperature 0.6
```

### Exemplo 2 — Jornalista de tecnologia

```bash
SYSTEM "Você escreve notícias de tecnologia com linguagem jornalística, sem opiniões pessoais."
PARAMETER temperature 0.8
```

### Exemplo 3 — Analista de logs

```bash
SYSTEM "Você analisa logs de sistema e responde com um resumo técnico em Markdown."
PARAMETER temperature 0.3
PARAMETER num_predict 300
```

---

## 📄 5. Personalizando o formato de saída (TEMPLATE)

A diretiva `TEMPLATE` permite definir **como o modelo recebe e devolve o prompt**.

### Exemplo: Formato pergunta-resposta

```bash
TEMPLATE """
Pergunta: {{ .Prompt }}
Resposta:
"""
```

### Exemplo: Output em JSON

```bash
TEMPLATE """
Análise:
{{ .Prompt }}

Responda no formato JSON:
{
  "resumo": "...",
  "prioridade": "alta|média|baixa"
}
"""
```

📌 Isso garante respostas estruturadas — útil para automações e integrações.

---

## 🧬 6. Adicionando adaptadores (LoRA)

Quando o Ollama for configurado com suporte a **LoRA adapters**, você pode combinar modelos base com ajustes de domínio específico.

```bash
FROM llama3
ADAPTER lora://chat-suporte
```

💡 *Use adapters para adaptar um modelo geral a um domínio (ex: financeiro, jurídico, técnico).*

---

## 🧪 7. Exemplo prático — Criando um modelo “Appmax Helper”

```bash
# Modelfile
FROM llama3
SYSTEM """
Você é o Appmax Helper — um assistente de integração para novos desenvolvedores.
Explique conceitos de API de forma didática e clara.
"""
PARAMETER temperature 0.5
PARAMETER top_p 0.85
TEMPLATE """
Usuário: {{ .Prompt }}
Appmax Helper:
"""
```

Crie e rode:

```bash
ollama create appmax-helper -f Modelfile
ollama run appmax-helper
```

Teste com:

```
Como integrar a API de pagamento via PIX?
```

---

## 🧱 8. Boas práticas de customização

✅ **Use nomes claros** (ex: `appmax-helper`, `python-teacher`).
✅ **Documente** cada alteração com comentários no Modelfile.
✅ **Teste** diferentes temperaturas antes de fixar.
✅ **Versione** os Modelfiles com Git (`Modelfile.v1`, `v2` etc).
✅ **Evite sobrecarregar o SYSTEM** — mantenha instruções curtas e específicas.
✅ **Padronize o output** (TEMPLATE ou formato JSON) para automações.

---

## 🧩 9. Exercício prático

> **Objetivo:** criar um modelo de “Analista de Suporte Appmax”
> com estilo técnico, respostas curtas e formato Markdown.

### Passos:

1. Basear-se no modelo `mistral`;
2. SYSTEM: persona técnica (suporte Appmax);
3. PARAMETER: `temperature 0.4`, `num_predict 300`;
4. TEMPLATE: saída em Markdown (`**Problema:** ... **Solução:** ...`);
5. Testar e comparar com o modelo base (`ollama run mistral`).

---

## 🧠 10. Discussão guiada

💬 **Perguntas para debate:**

* Quando vale a pena criar um novo Modelfile em vez de ajustar o prompt manualmente?
* Quais parâmetros mais influenciam o “estilo” de um modelo?
* Como equilibrar criatividade e previsibilidade em um modelo de suporte?
* Que tipos de customização facilitam automação via API?

---

## 🧾 11. Conclusão

Customizar modelos é o passo essencial para **trazer IA para o contexto da sua empresa ou produto**.
Com pequenas alterações em **SYSTEM**, **PARAMETER** e **TEMPLATE**, você transforma um modelo genérico em um **assistente especializado, estável e com identidade própria**.

> 💡 “O poder da IA não está só no modelo que você usa, mas em como você o molda para o seu contexto.”

---

## 📚 12. Recursos e leituras complementares

* [Documentação oficial do Ollama](https://github.com/ollama/ollama)
* [Model customization guide (OpenWebUI)](https://docs.openwebui.com/)
* [Prompt Engineering Handbook (Brev.dev)](https://www.brev.dev/prompt-engineering)
* [LoRA Adapters Overview](https://huggingface.co/docs/peft/index)
