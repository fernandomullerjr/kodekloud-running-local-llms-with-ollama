
# Modelfile - Introduction

Aqui vai um **material de apoio completo** para uma aula introdutória sobre **Modelfile** — o formato usado para configurar, personalizar e versionar modelos no ecossistema **Ollama / Open WebUI / LLM local**.

O conteúdo está estruturado em **módulos didáticos**, com **exemplos práticos**, **tópicos de discussão** e **tarefas sugeridas**.

---

# 🧠 Aula: **Introdução ao Modelfile**

## 🎯 Objetivo

Ao final desta aula, o aluno será capaz de:

* Entender o que é um **Modelfile** e sua função no ambiente LLM;
* Criar e editar Modelfiles para personalizar o comportamento de modelos;
* Executar e testar modelos customizados com o **Ollama**;
* Compreender parâmetros como `FROM`, `SYSTEM`, `PARAMETER` e `TEMPLATE`.

---

## 🧩 1. Conceito

**Modelfile** é um **arquivo de configuração declarativo** usado para **definir, adaptar e versionar modelos de linguagem** no Ollama.

👉 Ele é semelhante a um `Dockerfile`:
cada linha descreve como construir um **modelo final** a partir de outro modelo base.

Exemplo simples:

```bash
FROM mistral
SYSTEM "Você é um assistente educado e prestativo."
```

Isso cria um novo modelo chamado (por exemplo) `mistral-educado`, baseado em `mistral`, mas com instruções de sistema personalizadas.

---

## 🧰 2. Estrutura básica de um Modelfile

Um Modelfile segue uma estrutura simples e legível:

| Instrução   | Função                                                     |
| ----------- | ---------------------------------------------------------- |
| `FROM`      | Define o modelo base                                       |
| `SYSTEM`    | Define o prompt de sistema (comportamento base do modelo)  |
| `PARAMETER` | Ajusta hiperparâmetros do modelo (ex: temperatura, top_p)  |
| `TEMPLATE`  | Define o formato de prompt do usuário                      |
| `LICENSE`   | (opcional) adiciona informações de licença                 |
| `ADAPTER`   | (opcional) combina modelos LoRA ou adapters personalizados |

---

## ⚙️ 3. Exemplo prático completo

```bash
# Modelfile: suporte-tecnico
FROM mistral
SYSTEM """
Você é um agente de suporte técnico da Appmax.
Seja cordial e forneça respostas detalhadas, mas objetivas.
"""

PARAMETER temperature 0.6
PARAMETER top_p 0.9

TEMPLATE """
Usuário: {{ .Prompt }}
Suporte Técnico:
"""
```

📘 **O que este exemplo faz:**

* Usa o modelo **Mistral** como base;
* Define uma persona fixa (“agente de suporte técnico da Appmax”);
* Configura os parâmetros de geração (menos aleatório);
* Define um formato fixo de conversa.

---

## 🚀 4. Criando e rodando um modelo customizado

1. Crie o arquivo `Modelfile`:

   ```bash
   nano Modelfile
   ```

2. Cole o conteúdo do exemplo acima e salve.

3. Crie o modelo:

   ```bash
   ollama create suporte-tecnico -f Modelfile
   ```

4. Rode o modelo:

   ```bash
   ollama run suporte-tecnico
   ```

---

## 🧩 5. Personalização avançada

### a) **Parâmetros ajustáveis**

Você pode controlar aspectos como:

```bash
PARAMETER temperature 0.7
PARAMETER num_predict 512
PARAMETER stop "Usuário:"
```

### b) **Modelos híbridos (com LoRA / Adapters)**

```bash
FROM llama2
ADAPTER lora://assistente-suporte
```

### c) **Template personalizado**

Permite controlar como o modelo processa o input/output:

```bash
TEMPLATE """
Pergunta do usuário:
{{ .Prompt }}

Resposta:
"""
```

---

## 🧪 6. Exercício prático

> **Objetivo:** criar um modelo “Professor de Python”.

### Passos:

1. Basear-se no modelo `mistral`.
2. Definir `SYSTEM` como um instrutor experiente de Python.
3. Limitar `temperature` a 0.5.
4. Criar um template que use:

   ```
   Estudante: {{ .Prompt }}
   Professor:
   ```
5. Salvar o arquivo e rodar:

   ```bash
   ollama create professor-python -f Modelfile
   ollama run professor-python
   ```

---

## 🧱 7. Boas práticas

✅ Use nomes curtos e descritivos nos modelos (`ollama create appmax-support`).
✅ Mantenha os prompts de sistema consistentes e claros.
✅ Versione seus Modelfiles no Git.
✅ Documente cada alteração com comentários (`# Comentário explicativo`).
✅ Teste os parâmetros antes de fixá-los.

---

## 📚 8. Recursos complementares

* [Documentação oficial do Ollama](https://github.com/ollama/ollama)
* [Modelos disponíveis](https://ollama.ai/library)
* [Guia de Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
* [Open WebUI Modelfile integration](https://docs.openwebui.com/)

---

## 🧩 9. Atividade de fixação

> **Desafio:**
> Crie um Modelfile que use `FROM mistral` e atue como:
>
> * um **analista de logs de sistema**,
> * com `temperature=0.3`,
> * e que responda em formato de **relatório técnico Markdown**.

Depois, teste com:

```bash
ollama run analista-logs
```

---

## 🏁 10. Conclusão

O **Modelfile** é uma forma poderosa e simples de **controlar o comportamento dos modelos** de IA locais.
Assim como um `Dockerfile`, ele facilita:

* Reprodutibilidade;
* Customização;
* Deploy controlado de modelos em times e pipelines internos.

---
