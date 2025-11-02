import asyncio
import json
import time
import signal
import sys
from playwright.async_api import async_playwright

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Timeout global atingido")

async def debug_statusinvest_structure(ticker: str, max_timeout: int = 120):
    """Debug da estrutura da página Status Invest com timeout global"""
    ticker = ticker.upper().strip()
    url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
    
    print(f"🚀 Iniciando debug para {ticker}")
    print(f"🔗 URL: {url}")
    print(f"⏰ Timeout máximo: {max_timeout} segundos")
    print("=" * 60)
    
    # Configurar timeout global
    if max_timeout > 0:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(max_timeout)
    
    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,  # Mostra o browser
                slow_mo=500      # Execução mais rápida
            )
            page = await browser.new_page()
            
            print("📥 Carregando página...")
            try:
                # Timeout menor para goto, permitindo fallback
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                print("✅ Página carregada com domcontentloaded")
            except Exception as e:
                print(f"⚠️ Erro no carregamento inicial: {e}")
                try:
                    # Tentar novamente sem wait_until
                    await page.goto(url, timeout=20000)
                    print("✅ Página carregada sem wait_until")
                except Exception as e2:
                    print(f"❌ Falha total no carregamento: {e2}")
                    return
            
            print("⏳ Aguardando carregamento AJAX...")
            await page.wait_for_timeout(3000)  # Reduzido de 5000
            
            print(f"🔍 Analisando estrutura de: {url}")
            print("=" * 60)
            
            # 1. Verificar título da página
            print("\n🏷️ TÍTULO DA PÁGINA:")
            try:
                title = await page.title()
                print(f"Título: {title}")
            except Exception as e:
                print(f"Erro ao capturar título: {e}")
            
            # 2. Verificar seções principais (limitado)
            print("\n📊 SEÇÕES PRINCIPAIS:")
            try:
                sections = await page.locator("section, div[class*='card'], div[class*='indicator']").all()
                print(f"Encontradas {len(sections)} seções")
                
                for i, section in enumerate(sections[:10]):  # Reduzido de 15
                    try:
                        text = await section.text_content()
                        if text and len(text.strip()) > 10:
                            clean_text = ' '.join(text.split()[:8])  # Reduzido de 10
                            print(f"Seção {i:2d}: {clean_text}...")
                    except:
                        print(f"Seção {i:2d}: [Erro ao capturar]")
            except Exception as e:
                print(f"Erro ao capturar seções: {e}")
            
            # 3. Verificar indicadores com dados numéricos (limitado)
            print("\n📈 ELEMENTOS COM NÚMEROS:")
            try:
                elements_with_numbers = await page.locator("text=/\\d+[,.]\\d+%?/").all()
                print(f"Encontrados {len(elements_with_numbers)} elementos com números")
                
                for i, el in enumerate(elements_with_numbers[:15]):  # Reduzido de 25
                    try:
                        text = await el.text_content()
                        parent = el.locator("xpath=..")
                        parent_text = await parent.text_content()
                        
                        parent_clean = ' '.join(parent_text.split()[:6])  # Reduzido de 8
                        print(f"Número {i:2d}: '{text}' - Contexto: '{parent_clean}...'")
                    except:
                        print(f"Número {i:2d}: [Erro ao capturar]")
            except Exception as e:
                print(f"Erro ao capturar números: {e}")
            
            # 4. Procurar indicadores específicos (otimizado)
            print("\n🎯 PROCURANDO INDICADORES ESPECÍFICOS:")
            specific_indicators = ["P/L", "P/VP", "DY", "ROE", "ROIC", "Margem", "Payout"]
            
            for indicator in specific_indicators:
                try:
                    elements = await page.locator(f"text=/{indicator}/i").all()
                    if len(elements) > 0:
                        print(f"{indicator}: Encontrados {len(elements)} elementos")
                        
                        # Mostrar apenas o primeiro
                        try:
                            el = elements[0]
                            parent = el.locator("xpath=ancestor::*[self::div or self::li or self::tr][1]")
                            context = await parent.text_content()
                            context_clean = ' '.join(context.split()[:8])
                            print(f"  └─ 1: {context_clean}...")
                        except:
                            pass
                    else:
                        print(f"{indicator}: Não encontrado")
                except Exception as e:
                    print(f"{indicator}: Erro na busca - {e}")
            
            # 5. Salvar HTML (sempre tenta)
            print(f"\n💾 Salvando HTML...")
            html_content = await page.content()
            filename = f"debug_{ticker.lower()}_structure.html"
            
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"✅ HTML salvo em: {filename}")
                print(f"📊 Tamanho do arquivo: {len(html_content)} caracteres")
            except Exception as e:
                print(f"❌ Erro ao salvar HTML: {e}")
            
            # 6. Capturar screenshot (sempre tenta)
            print(f"\n📸 Capturando screenshot...")
            try:
                screenshot_filename = f"debug_{ticker.lower()}_screenshot.png"
                await page.screenshot(path=screenshot_filename, full_page=True)
                print(f"✅ Screenshot salvo em: {screenshot_filename}")
            except Exception as e:
                print(f"❌ Erro ao capturar screenshot: {e}")
            
            # 7. Aguardar apenas 3 segundos antes de fechar
            print(f"\n⏱️ Aguardando 3 segundos antes de fechar...")
            await page.wait_for_timeout(3000)
            
            print("🔄 Fechando browser...")
            await browser.close()
            
            print("\n✅ DEBUG CONCLUÍDO!")
            print(f"📁 Arquivos gerados:")
            print(f"   - {filename}")
            print(f"   - {screenshot_filename}")
            print("=" * 60)
            
    except TimeoutError:
        print(f"\n⏰ TIMEOUT GLOBAL ATINGIDO ({max_timeout}s)")
        print("🔄 Encerrando debug...")
        if browser:
            try:
                await browser.close()
            except:
                pass
    except Exception as e:
        print(f"\n❌ Erro durante o debug: {e}")
    finally:
        # Cancelar alarm
        if max_timeout > 0:
            signal.alarm(0)

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "BBAS3"
    
    # Verificar se foi passado timeout como argumento
    timeout = 120
    if len(sys.argv) > 2:
        try:
            timeout = int(sys.argv[2])
        except:
            timeout = 120
    
    start_time = time.time()
    try:
        asyncio.run(debug_statusinvest_structure(ticker, timeout))
    except KeyboardInterrupt:
        print("\n🛑 Debug interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o debug: {e}")
    finally:
        end_time = time.time()
        print(f"⏱️ Tempo total: {end_time - start_time:.2f} segundos")