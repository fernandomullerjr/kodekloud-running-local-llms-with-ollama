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

def scrape_dividend_history_requests(soup, ticker):
    """Captura histórico de dividendos usando requests/BeautifulSoup"""
    try:
        dividend_data = {
            "dy_12m": None,
            "dy_medio_5a": None,
            "dy_medio_10a": None,
            "historico_12m": []
        }
        
        # Procurar por textos com DY e períodos
        text_content = soup.get_text().lower()
        
        # Regex para capturar DY com períodos
        import re
        
        # DY 12 meses
        dy_12m_match = re.search(r'dy.*12.*meses?.*?(\d+[,.]?\d*)', text_content)
        if dy_12m_match:
            dividend_data["dy_12m"] = float(dy_12m_match.group(1).replace(',', '.'))
            
        # DY médio 5 anos
        dy_5a_match = re.search(r'dy.*5.*anos?.*?(\d+[,.]?\d*)', text_content)
        if dy_5a_match:
            dividend_data["dy_medio_5a"] = float(dy_5a_match.group(1).replace(',', '.'))
            
        # DY médio 10 anos
        dy_10a_match = re.search(r'dy.*10.*anos?.*?(\d+[,.]?\d*)', text_content)
        if dy_10a_match:
            dividend_data["dy_medio_10a"] = float(dy_10a_match.group(1).replace(',', '.'))
            
        # Procurar tabelas de histórico
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    cell_texts = [cell.get_text().strip() for cell in cells]
                    
                    # Procurar por datas (formato brasileiro)
                    for i, text in enumerate(cell_texts):
                        if re.match(r'\d{2}/\d{2}/\d{4}', text):
                            # Tentar extrair valor da próxima célula
                            if i + 1 < len(cell_texts):
                                value_text = cell_texts[i + 1]
                                value = extract_number_from_text(value_text)
                                if value:
                                    dividend_data["historico_12m"].append({
                                        "data": text,
                                        "valor": value
                                    })
                                    
        return dividend_data
        
    except Exception as e:
        print(f"Erro ao capturar dividendos via requests: {e}")
        return {
            "dy_12m": None,
            "dy_medio_5a": None,
            "dy_medio_10a": None,
            "historico_12m": []
        }

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

    # Adicionar captura de dividendos
    dividend_history = scrape_dividend_history_requests(soup, ticker)
    
    data = {
        "ticker": ticker,
        "url": url,
        "titulo": titulo,
        "indicadores": indicadores,
        "dividendos": dividend_history  # Nova seção
    }
    
    return data

if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "bbas3"
    print(json.dumps(scrape_statusinvest_requests(t), ensure_ascii=False, indent=2))
