import json
import re
import requests
from bs4 import BeautifulSoup

NUM_RE = re.compile(r"-?\d{1,3}([.\s]\d{3})*(,\d+)?%?|-?\d+,\d+%?")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9"
}

def normalize_number(s):
    if not s: return None
    s = s.strip()
    if s.endswith("%"): return s
    s = s.replace(".", "").replace(" ", "").replace("\xa0","").replace(",", ".")
    try:
        return float(s)
    except:
        return None

def scrape_statusinvest_requests(ticker="bbas3"):
    url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    h = soup.find(["h1","h2"])
    titulo = h.get_text(strip=True) if h else ticker.upper()

    labels_map = {
        "P/L": ["P/L", "Preço/Lucro"],
        "P/VP": ["P/VP", "Preço/Valor Patrimonial"],
        "Dividend Yield": ["Dividend", "Dividend Yield", "Dividendo"],
        "ROE": ["ROE"],
        "ROIC": ["ROIC"],
        "Margem Líquida": ["Margem Líquida"],
        "Dív. Líq/EBITDA": ["Dívida Líquida / EBITDA", "DL/EBITDA"]
    }

    indicadores = {}
    text = soup.get_text(" ", strip=True)
    for key, variants in labels_map.items():
        val = None
        for label in variants:
            i = text.lower().find(label.lower())
            if i != -1:
                snippet = text[max(0, i-60): i+160]
                m = NUM_RE.search(snippet)
                if m:
                    val = m.group(0)
                    break
        indicadores[key] = normalize_number(val) if val else None

    return {
        "ticker": ticker.upper(),
        "url": url,
        "titulo": titulo,
        "indicadores": indicadores
    }

if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "bbas3"
    print(json.dumps(scrape_statusinvest_requests(t), ensure_ascii=False, indent=2))
