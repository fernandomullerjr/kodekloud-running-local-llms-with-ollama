
# Essential Ollama CLI Commands

---


# 📚 Comandos Essenciais do Ollama

Este guia reúne os comandos mais importantes do **Ollama** para **gerenciar, executar e personalizar LLMs** localmente.

---

## 1. Instalar um modelo

Baixa e instala um modelo do repositório oficial do Ollama.

```bash
ollama pull <modelo>
```

**Exemplo:**

```bash
ollama pull llama2
```

💡 *É como “baixar um aplicativo” — o modelo fica salvo no seu computador.*

---

## 2. Listar modelos instalados

Mostra todos os modelos que você já baixou.

```bash
ollama list
```

💡 *Útil para saber quais modelos já estão disponíveis localmente.*

---

## 3. Ver informações sobre um modelo

Mostra detalhes de um modelo, como arquitetura, parâmetros, tamanho e data de instalação.

```bash
ollama show <modelo>
```

**Exemplo:**

```bash
ollama show llama2
```


> ollama show deepseek-r1:latest
  Model
    architecture        qwen3
    parameters          8.2B
    context length      131072
    embedding length    4096
    quantization        Q4_K_M

  Capabilities
    completion
    thinking

  Parameters
    stop           "<｜begin▁of▁sentence｜>"
    stop           "<｜end▁of▁sentence｜>"
    stop           "<｜User｜>"
    stop           "<｜Assistant｜>"
    temperature    0.6
    top_p          0.95

  License
    MIT License
    Copyright (c) 2023 DeepSeek
    ...


💡 *É como abrir a ficha técnica do modelo para saber suas especificações.*

---

## 4. Executar um modelo

Inicia o modelo e abre o modo interativo.

```bash
ollama run <modelo>
```

**Exemplo:**

```bash
ollama run mistral
```

💡 *É como “abrir o aplicativo” e começar a conversar.*

---

## 5. Executar com um prompt direto

Executa o modelo com uma entrada e já retorna a resposta, sem entrar no modo interativo.

```bash
ollama run <modelo> "Seu prompt aqui"
```

**Exemplo:**

```bash
ollama run llama2 "Explique a teoria da relatividade de forma simples"
```

---

## 6. Remover um modelo

Apaga um modelo instalado e libera espaço.

```bash
ollama rm <modelo>
```

**Exemplo:**

```bash
ollama rm gemma
```

💡 *Bom para economizar espaço de armazenamento.*

---

## 7. Criar um modelo customizado

Cria um modelo baseado em outro, usando um **Modelfile**.

```bash
ollama create <nome> -f Modelfile
```

**Exemplo:**

```bash
ollama create meu-assistente -f Modelfile
```

---

## 8. Definir parâmetros no Modelfile

Dentro de um **Modelfile**, você pode configurar ajustes padrão.

**Exemplo:**

```text
FROM llama2
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM "Você é um especialista em IA."
```

---

## 9. Passar parâmetros direto na execução

Defina parâmetros sem precisar criar um Modelfile.

```bash
ollama run <modelo> --temperature 0.2 --top_p 0.8 "Responda de forma técnica"
```

---

## 10. Encerrar execução do modelo

Quando estiver no modo interativo, para encerrar:

* **Ctrl + D** ou
* Digite:

```text
/bye
```

---

## 11. Ver ajuda dos comandos

Mostra todos os comandos e opções disponíveis.

```bash
ollama help
```

---

## 📝 Resumo Rápido

| Ação                          | Comando                             |
| ----------------------------- | ----------------------------------- |
| Instalar modelo               | `ollama pull <modelo>`              |
| Listar modelos                | `ollama list`                       |
| Ver info do modelo            | `ollama show <modelo>`              |
| Executar modelo               | `ollama run <modelo>`               |
| Prompt direto                 | `ollama run <modelo> "texto"`       |
| Remover modelo                | `ollama rm <modelo>`                |
| Criar modelo customizado      | `ollama create <nome> -f Modelfile` |
| Passar parâmetros na execução | `ollama run <modelo> --param valor` |
| Encerrar execução             | `Ctrl+D` ou `/bye`                  |
| Ajuda                         | `ollama help`                       |

---
