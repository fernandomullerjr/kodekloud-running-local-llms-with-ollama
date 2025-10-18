.PHONY: venv install playwright scrape scrape-requests analise

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
