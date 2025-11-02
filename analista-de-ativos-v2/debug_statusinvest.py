import asyncio
import json
from playwright.async_api import async_playwright

async def debug_statusinvest_structure(ticker: str):
    """Debug da estrutura da página Status Invest"""
    ticker = ticker.upper().strip()
    url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=False para ver a página
        page = await browser.new_page()
        
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        print(f"🔍 Analisando estrutura de: {url}")
        print("=" * 60)
        
        # 1. Verificar seções principais
        print("\n📊 SEÇÕES PRINCIPAIS:")
        sections = await page.locator("section, div[class*='card'], div[class*='indicator']").all()
        for i, section in enumerate(sections[:10]):
            try:
                text = await section.text_content()
                if text and len(text.strip()) > 0:
                    print(f"Seção {i}: {text[:100]}...")
            except:
                pass
        
        # 2. Verificar indicadores com dados numéricos
        print("\n📈 ELEMENTOS COM NÚMEROS:")
        elements_with_numbers = await page.locator("text=/\\d+[,.]\\d+%?/").all()
        for i, el in enumerate(elements_with_numbers[:20]):
            try:
                text = await el.text_content()
                parent_text = await el.locator("xpath=..").text_content()
                print(f"Número {i}: '{text}' - Contexto: '{parent_text[:50]}...'")
            except:
                pass
        
        # 3. Verificar abas ou botões relacionados a dividendos
        print("\n💰 ELEMENTOS RELACIONADOS A DIVIDENDOS:")
        dividend_elements = await page.locator("text=/dividend|divid|dy|rend/i").all()
        for i, el in enumerate(dividend_elements[:10]):
            try:
                text = await el.text_content()
                tag_name = await el.evaluate("el => el.tagName")
                classes = await el.get_attribute("class") or ""
                print(f"Dividendo {i}: '{text}' - Tag: {tag_name} - Classes: {classes}")
            except:
                pass
        
        # 4. Verificar tabelas
        print("\n📋 TABELAS ENCONTRADAS:")
        tables = await page.locator("table").all()
        for i, table in enumerate(tables):
            try:
                rows = await table.locator("tr").count()
                first_row = await table.locator("tr").first.text_content()
                print(f"Tabela {i}: {rows} linhas - Primeira linha: '{first_row[:100]}...'")
            except:
                pass
        
        # 5. Verificar estrutura específica do Status Invest
        print("\n🏗️ ESTRUTURA ESPECÍFICA:")
        
        # Verificar cards de indicadores
        indicator_cards = await page.locator("div[class*='indicator'], div[class*='card'], div[class*='metric']").all()
        for i, card in enumerate(indicator_cards[:15]):
            try:
                text = await card.text_content()
                if any(keyword in text.lower() for keyword in ['p/l', 'p/vp', 'dy', 'roe', 'dividend']):
                    print(f"Card {i}: {text[:100]}...")
            except:
                pass
        
        # 6. Salvar HTML para análise offline
        html_content = await page.content()
        with open(f"debug_{ticker.lower()}_structure.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n💾 HTML salvo em: debug_{ticker.lower()}_structure.html")
        
        # 7. Verificar se existem APIs ou dados JSON na página
        print("\n🔌 VERIFICANDO REQUISIÇÕES AJAX:")
        page.on("response", lambda response: print(f"Response: {response.url}") if "api" in response.url or "json" in response.url else None)
        
        # Aguardar um pouco para capturar requests
        await page.wait_for_timeout(5000)
        
        await browser.close()

if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "BBAS3"
    asyncio.run(debug_statusinvest_structure(ticker))