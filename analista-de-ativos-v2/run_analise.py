import asyncio
import json
import subprocess
import sys

from statusinvest_scrape import scrape_statusinvest_acao
from statusinvest_requests import scrape_statusinvest_requests

DEFAULT_MODEL = "analista-fundamentalista-gemma"

def run_ollama(model: str, payload: dict) -> str:
    prompt = (
        "Analise o ativo abaixo e classifique a qualidade (Alta|Neutra|Baixa).\n"
        "Dados:\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )
    proc = subprocess.run(
        ["ollama", "run", model],
        input=prompt, text=True, capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    return proc.stdout

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python run_analise.py <TICKER> [MODEL]")
        sys.exit(1)
    ticker = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL

    try:
        data = asyncio.run(scrape_statusinvest_acao(ticker))
    except Exception as e:
        print(f"[fallback] Playwright falhou: {e}\nUsando requests/bs4…")
        data = scrape_statusinvest_requests(ticker)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("\n================= RESPOSTA DO MODELO =================\n")
    print(run_ollama(model, data))
