import asyncio
import json
import re
from typing import Dict, Optional, List
from playwright.async_api import async_playwright

async def wait_for_page_load(page):
    """Aguarda o carregamento completo da página"""
    try:
        # Aguarda por indicadores específicos do Status Invest
        await page.wait_for_selector("text=/P\\/L|DY|ROE/i", timeout=30000)
        await page.wait_for_timeout(3000)  # Aguarda um pouco mais para AJAX
    except:
        await page.wait_for_timeout(5000)

def extract_number_from_string(text: str) -> Optional[float]:
    """Extrai número de uma string, lidando com formatos brasileiros"""
    if not text:
        return None
    
    # Remove caracteres não numéricos, mantendo pontos, vírgulas e sinais
    text = re.sub(r'[^\d,.\-+%]', '', text.strip())
    
    if '%' in text:
        # Retorna como string se for porcentagem
        return text
    
    # Converte formato brasileiro (1.234,56) para float
    if ',' in text and '.' in text:
        # Formato: 1.234,56
        text = text.replace('.', '').replace(',', '.')
    elif ',' in text and text.count(',') == 1:
        # Formato: 123,56
        text = text.replace(',', '.')
    
    try:
        return float(text)
    except:
        return None

async def scrape_basic_indicators(page) -> Dict:
    """Scraping dos indicadores básicos"""
    indicators = {}
    
    # Mapeamento mais específico baseado no Status Invest
    mappings = {
        "P/L": ["P/L", "Preço/Lucro"],
        "P/VP": ["P/VP", "Preço/Valor Patrimonial"],
        "DY": ["DY", "Dividend Yield", "Div. Yield"],
        "ROE": ["ROE"],
        "ROIC": ["ROIC"],
        "Margem Líquida": ["Margem Líquida", "Marg. Líquida"],
        "Margem EBITDA": ["Margem EBITDA", "Marg. EBITDA"],
        "Dív. Líq/EBITDA": ["Dív. Líq./EBITDA", "Divida Liquida/EBITDA"],
        "Payout": ["Payout"]
    }
    
    # Procurar em diferentes estruturas do Status Invest
    for key, labels in mappings.items():
        value = None
        
        for label in labels:
            try:
                # Estratégia 1: Procurar por texto seguido de valor
                locator = page.locator(f"text=/{re.escape(label)}/i")
                count = await locator.count()
                
                for i in range(count):
                    try:
                        element = locator.nth(i)
                        
                        # Procurar valor no mesmo elemento ou elementos próximos
                        parent = element.locator("xpath=ancestor::*[self::div or self::li or self::tr or self::td][1]")
                        parent_text = await parent.text_content()
                        
                        # Extrair número do texto
                        numbers = re.findall(r'-?\d{1,3}(?:[.\s]\d{3})*(?:,\d+)?%?', parent_text)
                        if numbers:
                            # Pegar o último número encontrado (geralmente é o valor)
                            value = extract_number_from_string(numbers[-1])
                            if value is not None:
                                break
                                
                    except:
                        continue
                
                if value is not None:
                    break
                    
            except:
                continue
        
        indicators[key] = value
    
    return indicators

async def scrape_dividend_data(page) -> Dict:
    """Scraping específico para dados de dividendos"""
    dividend_data = {
        "dy_12m": None,
        "dy_medio_5a": None,
        "dy_medio_10a": None,
        "historico_12m": []
    }
    
    try:
        # Procurar por seção de dividendos ou abas
        dividend_sections = await page.locator("text=/dividend|divid|rend/i").all()
        
        for section in dividend_sections:
            try:
                # Clicar se for um botão/aba
                if await section.is_visible():
                    section_text = await section.text_content()
                    if any(word in section_text.lower() for word in ['dividendo', 'dividend', 'histórico']):
                        await section.click()
                        await page.wait_for_timeout(2000)
                        break
            except:
                continue
        
        # Procurar por dados específicos de DY
        page_content = await page.content()
        
        # Regex para capturar DY com períodos específicos
        dy_12m_match = re.search(r'dy.*?12.*?meses?.*?(\d+[,.]?\d*%?)', page_content, re.IGNORECASE)
        if dy_12m_match:
            dividend_data["dy_12m"] = extract_number_from_string(dy_12m_match.group(1))
        
        dy_5a_match = re.search(r'dy.*?5.*?anos?.*?(\d+[,.]?\d*%?)', page_content, re.IGNORECASE)
        if dy_5a_match:
            dividend_data["dy_medio_5a"] = extract_number_from_string(dy_5a_match.group(1))
        
        dy_10a_match = re.search(r'dy.*?10.*?anos?.*?(\d+[,.]?\d*%?)', page_content, re.IGNORECASE)
        if dy_10a_match:
            dividend_data["dy_medio_10a"] = extract_number_from_string(dy_10a_match.group(1))
        
        # Procurar tabelas de histórico
        tables = await page.locator("table").all()
        for table in tables:
            try:
                table_text = await table.text_content()
                if any(word in table_text.lower() for word in ['data', 'valor', 'dividendo', 'jcp']):
                    rows = await table.locator("tr").all()
                    for row in rows[1:13]:  # Pular header e pegar até 12 linhas
                        try:
                            row_text = await row.text_content()
                            # Procurar por data no formato brasileiro
                            date_match = re.search(r'\d{2}/\d{2}/\d{4}', row_text)
                            # Procurar por valor monetário
                            value_match = re.search(r'R?\$?\s*(\d+[,.]?\d*)', row_text)
                            
                            if date_match and value_match:
                                dividend_data["historico_12m"].append({
                                    "data": date_match.group(0),
                                    "valor": extract_number_from_string(value_match.group(1))
                                })
                        except:
                            continue
                    break
            except:
                continue
                
    except Exception as e:
        print(f"Erro ao capturar dados de dividendos: {e}")
    
    return dividend_data

async def scrape_company_info(page) -> tuple:
    """Scraping de informações básicas da empresa"""
    try:
        # Título - geralmente em h1 ou elemento principal
        title_selectors = ["h1", "h2", "[class*='title']", "[class*='header']"]
        titulo = None
        
        for selector in title_selectors:
            try:
                titulo = await page.locator(selector).first.text_content()
                if titulo and len(titulo.strip()) > 0:
                    break
            except:
                continue
        
        # Setor - procurar em elementos que contenham palavras-chave de setores
        setor = None
        setor_keywords = ["banco", "energia", "petróleo", "varejo", "imobiliário", "siderurgia", "telecom"]
        
        page_text = await page.text_content()
        for keyword in setor_keywords:
            if keyword.lower() in page_text.lower():
                # Procurar contexto mais específico
                setor_match = re.search(f'setor[^a-z]*([^.]*{keyword}[^.]*)', page_text, re.IGNORECASE)
                if setor_match:
                    setor = setor_match.group(1).strip()
                    break
                else:
                    setor = keyword.title()
                    break
        
        return titulo, setor
        
    except Exception as e:
        print(f"Erro ao capturar informações da empresa: {e}")
        return None, None

async def scrape_statusinvest_acao_v2(ticker: str) -> dict:
    """Versão melhorada do scraping Status Invest"""
    ticker = ticker.upper().strip()
    url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            page = await context.new_page()
            
            # Ir para a página e aguardar carregamento
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await wait_for_page_load(page)
            
            # Capturar dados
            titulo, setor = await scrape_company_info(page)
            indicadores = await scrape_basic_indicators(page)
            dividendos = await scrape_dividend_data(page)
            
            data = {
                "ticker": ticker,
                "url": url,
                "titulo": titulo or f"{ticker} - Status Invest",
                "setor": setor,
                "indicadores": indicadores,
                "dividendos": dividendos
            }
            
            await browser.close()
            return data
            
        except Exception as e:
            raise RuntimeError(f"Erro no scraping v2: {e}")

if __name__ == "__main__":
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else "BBAS3"
    data = asyncio.run(scrape_statusinvest_acao_v2(ticker))
    print(json.dumps(data, ensure_ascii=False, indent=2))