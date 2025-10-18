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

async def scrape_statusinvest_acao(ticker: str) -> Dict:
    url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/127 Safari/537.36"),
            locale="pt-BR"
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="networkidle", timeout=60000)

        # fechar cookies/banners se houver
        for sel in ["button:has-text('Aceitar')", "button:has-text('Fechar')", "button[aria-label*='fechar' i]"]:
            try:
                if await page.locator(sel).is_visible():
                    await page.click(sel, timeout=2000)
            except:
                pass

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

        await browser.close()

    return {
        "ticker": ticker.upper(),
        "url": url,
        "titulo": titulo.strip() if titulo else ticker.upper(),
        "setor": setor,
        "indicadores": indicadores
    }

if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "bbas3"
    data = asyncio.run(scrape_statusinvest_acao(t))
    print(json.dumps(data, ensure_ascii=False, indent=2))
