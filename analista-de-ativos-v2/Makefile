.PHONY: venv install playwright scrape scrape-requests analise debug debug-analyze

PY?=python3
PIP?=pip
VENV?=.venv

venv:
	$(PY) -m venv $(VENV)
	. $(VENV)/bin/activate && $(PIP) install --upgrade pip

install: venv
	. $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	. $(VENV)/bin/activate && playwright install

# Scrape with Playwright (recommended)
scrape:
	. $(VENV)/bin/activate && $(PY) statusinvest_scrape.py $(TICKER)

# Scrape with requests/bs4 fallback
scrape-requests:
	. $(VENV)/bin/activate && $(PY) statusinvest_requests.py $(TICKER)

# Run analysis with Ollama model (MODEL var optional)
analise:
	. $(VENV)/bin/activate && $(PY) run_analise.py $(TICKER) $(MODEL)

# Debug para entender a estrutura (com timeout respeitado)
debug:
	@echo "🚀 Iniciando debug para $(TICKER)..."
	. $(VENV)/bin/activate && $(PY) debug_statusinvest.py $(TICKER) 60 || true
	@echo "✅ Debug concluído! Verifique os arquivos debug_$(shell echo $(TICKER) | tr A-Z a-z)_*"

# Debug com timeout customizado
debug-timeout:
	@echo "🚀 Iniciando debug para $(TICKER) com timeout $(TIMEOUT)s..."
	. $(VENV)/bin/activate && $(PY) debug_statusinvest.py $(TICKER) $(TIMEOUT) || true
	@echo "✅ Debug concluído!"

# Analisar arquivos gerados pelo debug
debug-analyze:
	@echo "📊 Analisando arquivos do debug..."
	@ls -la debug_$(shell echo $(TICKER) | tr A-Z a-z)_* 2>/dev/null || echo "❌ Nenhum arquivo de debug encontrado"
	@echo "🔍 Procurando indicadores no HTML..."
	@grep -i "p/l\|dy\|roe\|dividend\|payout" debug_$(shell echo $(TICKER) | tr A-Z a-z)_structure.html | head -10 2>/dev/null || echo "❌ HTML não encontrado"