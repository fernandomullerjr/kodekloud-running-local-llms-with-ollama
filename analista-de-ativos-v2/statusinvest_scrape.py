import asyncio
import json
import re
from typing import Dict, Optional, List

from playwright.async_api import async_playwright

LABELS_PT = {
    "P/L": ["P/L", "Preço/Lucro"],
    "P/VP": ["P/VP", "Preço/Valor Patrimonial"],
    "DY": ["Dividend", "Dividend Yield", "Dividendo"],
    "ROE": ["ROE", "Return on Equity"],
    "ROIC": ["ROIC"],
    "Margem Líquida": ["Margem Líquida", "Net Margin"],
    "Margem EBITDA": ["Margem EBITDA", "EBITDA Margin"],
    "Crescimento Lucros": ["Crescimento de Lucros", "Cresc. Lucro"],
    "Dív. Líq/EBITDA": ["Dívida Líquida / EBITDA", "Divida Liquida / EBITDA", "DL/EBITDA"],
    "Payout": ["Payout"],
}

NUM_RE = re.compile(r"-?\d{1,3}([.\s]\d{3})*(,\d+)?%?|-?\d+,\d+%?")

def normalize_number(s: str) -> Optional[float]:
    if not s:
        return None
    s = s.strip()
    if s.endswith('%'):
        return s
    s = s.replace('.', '').replace(' ', '').replace('\xa0', '').replace(',', '.')
    try:
        return float(s)
    except:
        return None

async def extract_by_labels(page, label_candidates: List[str]) -> Optional[str]:
    for label in label_candidates:
        locator = page.locator(
            "xpath=//*[contains(translate(normalize-space(text()), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÂÃÀÉÊÍÓÔÕÚÇ', "
            "'abcdefghijklmnopqrstuvwxyzáâãàéêíóôõúç'), "
            f"'{label.lower()}')]"
        )
        count = await locator.count()
        for i in range(count):
            el = locator.nth(i)
            box = el.locator("xpath=ancestor::*[self::div or self::li or self::tr][1]")
            try:
                text = await box.inner_text()
            except:
                continue
            m = NUM_RE.search(text)
            if m:
                return m.group(0).strip()
    return None

def extract_number_from_text(text: str) -> Optional[float]:
    """Extrai o primeiro número válido de um texto."""
    text = text.replace('R$', '').replace('%', '').strip()
    try:
        return normalize_number(text)
    except:
        return None

async def scrape_dividend_history(page, ticker):
    """Captura histórico de dividendos e DY médios"""
    try:
        # Seção de dividendos - pode estar em abas ou seções específicas
        dividend_data = {
            "dy_12m": None,
            "dy_medio_5a": None,
            "dy_medio_10a": None,
            "historico_12m": []
        }
        
        # Procurar por DY últimos 12 meses
        try:
            dy_12m_locator = page.locator("text=/DY.*12.*meses?/i").first.locator("xpath=ancestor::*[self::div or self::tr][1]")
            dy_12m_text = await dy_12m_locator.text_content()
            dy_12m_value = extract_number_from_text(dy_12m_text)
            if dy_12m_value:
                dividend_data["dy_12m"] = dy_12m_value
        except:
            pass
            
        # Procurar por DY médio 5 anos
        try:
            dy_5a_locator = page.locator("text=/DY.*5.*anos?/i").first.locator("xpath=ancestor::*[self::div or self::tr][1]")
            dy_5a_text = await dy_5a_locator.text_content()
            dy_5a_value = extract_number_from_text(dy_5a_text)
            if dy_5a_value:
                dividend_data["dy_medio_5a"] = dy_5a_value
        except:
            pass
            
        # Procurar por DY médio 10 anos
        try:
            dy_10a_locator = page.locator("text=/DY.*10.*anos?/i").first.locator("xpath=ancestor::*[self::div or self::tr][1]")
            dy_10a_text = await dy_10a_locator.text_content()
            dy_10a_value = extract_number_from_text(dy_10a_text)
            if dy_10a_value:
                dividend_data["dy_medio_10a"] = dy_10a_value
        except:
            pass
            
        # Tentar acessar seção de histórico de dividendos
        try:
            # Procurar botão/aba de dividendos
            dividend_tab = page.locator("text=/dividendos?/i").first
            if await dividend_tab.is_visible():
                await dividend_tab.click()
                await page.wait_for_timeout(2000)
                
                # Capturar tabela de histórico
                dividend_rows = page.locator("table tr:has-text('/')")  # linhas com datas
                count = await dividend_rows.count()
                
                for i in range(min(count, 12)):  # últimos 12 meses
                    try:
                        row = dividend_rows.nth(i)
                        row_text = await row.text_content()
                        
                        # Extrair data e valor (formato pode variar)
                        parts = row_text.split()
                        date_found = None
                        value_found = None
                        
                        for part in parts:
                            if '/' in part and len(part) >= 7:  # formato dd/mm/yyyy
                                date_found = part
                            elif 'R$' in part or '%' in part:
                                value_found = extract_number_from_text(part)
                                
                        if date_found and value_found:
                            dividend_data["historico_12m"].append({
                                "data": date_found,
                                "valor": value_found
                            })
                    except:
                        continue
        except:
            pass
            
        return dividend_data
        
    except Exception as e:
        print(f"Erro ao capturar histórico de dividendos: {e}")
        return {
            "dy_12m": None,
            "dy_medio_5a": None,
            "dy_medio_10a": None,
            "historico_12m": []
        }

async def scrape_statusinvest_acao(ticker: str) -> dict:
    """
    Faz scraping da página de uma ação na Status Invest.
    """
    ticker = ticker.upper().strip()
    url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--disable-dev-shm-usage",
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                ],
            )
            ctx = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/127 Safari/537.36"
                ),
                locale="pt-BR",
                viewport={"width": 1366, "height": 768},
            )
            page = await ctx.new_page()

            # Bloqueia recursos que atrapalham o 'idle' e só pesam
            async def _route(route, request):
                u = request.url
                if any(u.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".woff", ".woff2")):
                    return await route.abort()
                if any(h in u for h in ("googletagmanager.com", "google-analytics.com", "doubleclick.net", "hotjar", "segment.io")):
                    return await route.abort()
                return await route.continue_()
            await page.route("**/*", _route)

            # Carrega até DOM pronto; 'networkidle' é instável em sites com long-polling
            await page.goto(url, wait_until="domcontentloaded", timeout=180000)

            # Espera por um elemento que comprove que a página carregou os indicadores
            try:
                await page.wait_for_selector("text=/P\\/L|Preço\\/Lucro/i", timeout=120000)
            except:
                # como fallback, espere o título
                await page.wait_for_selector("h1, h2", timeout=60000)

            # título / setor (heurística simples)
            try:
                titulo = await page.locator("h1, h2").first.inner_text()
            except:
                titulo = ticker.upper()

            setor = None
            try:
                chips = page.locator("a, span")
                n = await chips.count()
                n = min(200, n)
                for i in range(n):
                    t = await chips.nth(i).inner_text()
                    if any(k in t.lower() for k in ["setor", "bancos", "energia", "utilidades", "consumo", "imobiliário", "industrial", "financeiro"]):
                        setor = t.strip()
                        break
            except:
                pass

            indicadores = {}
            for key, variants in LABELS_PT.items():
                raw = await extract_by_labels(page, variants)
                indicadores[key] = normalize_number(raw) if raw else None

            # Capturar histórico de dividendos
            dividend_history = await scrape_dividend_history(page, ticker)
            
            data = {
                "ticker": ticker,
                "url": url,
                "titulo": titulo,
                "setor": setor,
                "indicadores": indicadores,
                "dividendos": dividend_history  # Nova seção
            }
            
            await browser.close()
            return data
            
        except Exception as e:
            raise RuntimeError(f"Erro no scraping do Playwright: {e}")

if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "bbas3"
    data = asyncio.run(scrape_statusinvest_acao(t))
    print(json.dumps(data, ensure_ascii=False, indent=2))
