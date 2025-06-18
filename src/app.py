from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# --- Configurações (sem alterações) ---
caminho_chromedriver = r"C:\Users\Lenon Torma\Desktop\Jornada_de_dados\projeto_end_to_end\requests_bs4\chromedriver.exe"
service = Service(caminho_chromedriver)
chrome_options = Options()
# chrome_options.add_argument("--headless=new")
url = "https://casaraoimoveis.com.br/imoveis/alugueis/pelotas/todos-os-tipos/"

def sua_funcao_de_extracao(html_completo: str):
    soup = BeautifulSoup(html_completo, 'html.parser')
    imoveis_encontrados = soup.find_all('div', class_='card-imovel')
    print(f"    -> Encontrei {len(imoveis_encontrados)} cards de imóveis no HTML final.")
    return imoveis_encontrados

def raspar_pagina_com_rolagem_infinita(url: str):
    driver = None
    try:
        print("[ENGENHARIA DE DADOS] Iniciando o processo de web scraping...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)

        altura_anterior = driver.execute_script("return document.body.scrollHeight")
        print(f"Altura inicial da página: {altura_anterior} pixels.")

        while True:
            # --- MUDANÇA PRINCIPAL AQUI ---
            # 1. Encontramos o último elemento carregado
            cards_imoveis = driver.find_elements(By.CSS_SELECTOR, "div.card-imovel")
            
            if cards_imoveis:
                print(f"[AÇÃO] Rolando até o último dos {len(cards_imoveis)} imóveis visíveis...")
                # 2. Executamos um script para rolar até ele
                # O argumento {behavior: 'smooth', block: 'center'} ajuda a simular um usuário
                # e centraliza o elemento na tela, o que é ótimo para acionar eventos.
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cards_imoveis[-1])
            else:
                # Caso de borda: se nenhum card for encontrado, faz uma rolagem padrão
                print("[AÇÃO] Nenhum card encontrado ainda, fazendo rolagem padrão.")
                driver.execute_script("window.scrollBy(0, 800);") # Rola 800 pixels para baixo

            # Espera inteligente para o conteúdo carregar
            time.sleep(3) # Aumentei um pouco o tempo para dar margem à animação da rolagem e à resposta da rede

            altura_nova = driver.execute_script("return document.body.scrollHeight")
            print(f"Nova altura: {altura_nova} pixels.")

            if altura_nova == altura_anterior:
                # Tenta uma última rolagem para garantir que não parou por um falso negativo
                print("[VERIFICAÇÃO] Altura não mudou. Tentando uma última rolagem forçada...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                altura_nova = driver.execute_script("return document.body.scrollHeight")
                if altura_nova == altura_anterior:
                    print("\n[STATUS] Fim da página confirmado. Não há mais conteúdo para carregar.")
                    break
            
            altura_anterior = altura_nova
        
        print("\n[COLETA] Coletando o HTML final da página completa...")
        html_final = driver.page_source
        dados_extraidos = sua_funcao_de_extracao(html_final)
        return dados_extraidos

    except Exception as e:
        print(f"[ERRO] Um erro inesperado ocorreu: {e}")
        return None
    finally:
        if driver:
            print("[STATUS] Processo finalizado. Fechando o navegador.")
            driver.quit()

# --- Execução Principal (sem alterações) ---
if __name__ == "__main__":
    todos_os_imoveis = raspar_pagina_com_rolagem_infinita(url)
    if todos_os_imoveis:
        print(f"\n--- RESULTADO FINAL ---")
        print(f"Total de imóveis coletados: {len(todos_os_imoveis)}")
    else:
        print("\n--- Nenhuma informação foi coletada. ---")