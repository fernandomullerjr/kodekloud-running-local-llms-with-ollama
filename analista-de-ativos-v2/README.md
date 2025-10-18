# StatusInvest Scraper + Ollama Analyst (WSL ready)

Toolkit para coletar indicadores de ativos no Status Invest e alimentar um modelo local do Ollama (ex.: Gemma 2 9B) para análise fundamentalista.

## Requisitos
- WSL2 (Ubuntu 22.04) ou Linux
- Python 3.10+
- [Ollama](https://ollama.com/) instalado e funcionando (`ollama --version`)
- Navegador headless via Playwright

## Setup rápido
```bash
make install
```
Isso cria a venv, instala dependências e baixa o Chromium headless para o Playwright.

## Como usar
### 1) Scraping (Playwright recomendado)
```bash
make scrape TICKER=BBAS3
```
Saída: JSON com indicadores.

### 2) Scraping (fallback com requests/bs4)
```bash
make scrape-requests TICKER=BBAS3
```

### 3) Analisar com modelo do Ollama
Antes, crie seu modelo (veja Modelfiles abaixo). Depois:
```bash
make analise TICKER=BBAS3 MODEL=analista-fundamentalista-gemma
```
> `MODEL` é opcional, default no script é `analista-fundamentalista-gemma`.

## Modelfiles de exemplo
- `Modelfile.gemma` : usa `gemma2:9b` como base.
- `Modelfile.fingpt` : usa um `.gguf` local (FinGPT/Mistral). Ajuste o nome do arquivo.

### Criar o modelo (Gemma)
```bash
ollama pull gemma2:9b
ollama create analista-fundamentalista-gemma -f Modelfile.gemma
```

### Criar o modelo (FinGPT/Mistral .gguf)
Coloque o arquivo `.gguf` no mesmo diretório e ajuste o nome dentro do `Modelfile.fingpt`. Então:
```bash
ollama create analista-fundamentalista-fingpt -f Modelfile.fingpt
```

## Observações importantes
- Respeite os Termos de Uso e robots.txt do site alvo.
- Use com prudência (rate limit, backoff). Selecione indicadores por rótulos — seletores podem mudar.
- Os scripts são heurísticos; revise-os conforme a página evoluir.

## Comandos úteis
```bash
# Ambiente
make install

# Scraping
make scrape TICKER=BBAS3
make scrape-requests TICKER=BBAS3

# Análise (usa Ollama)
make analise TICKER=BBAS3 MODEL=analista-fundamentalista-gemma
```
