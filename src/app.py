from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

caminho_chromedriver = r"C:\Users\Lenon Torma\Desktop\Jornada_de_dados\projeto_end_to_end\requests_bs4\chromedriver.exe"
service = Service(caminho_chromedriver)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
url = "https://casaraoimoveis.com.br/imoveis/alugueis/pelotas/todos-os-tipos/"

def extrair_endereco(driver):
    try:
        endereco = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.endereco"))
        ).text.strip()
    except Exception as e:
        print(f"Erro ao extrair endereço: {e}")
        endereco = "Endereço não encontrado"

    caracteristicas = {}

    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                "body > section > div.caracteristicas > div > div > div > div > div.col-lg-5 > div > div"))
        )
        rows = container.find_elements(By.CLASS_NAME, "row")
        for row in rows:
            try:
                nome_element = row.find_element(By.CLASS_NAME, "col")
                valor_element = row.find_element(By.CLASS_NAME, "valores")
                nome = nome_element.text.strip()
                valor = valor_element.text.strip()
                caracteristicas[nome] = valor
            except Exception as e:
                print(f"Erro ao extrair característica em uma linha: {e}")
                continue
    except Exception as e:
        print(f"Erro ao acessar características do imóvel: {e}")

    return endereco, caracteristicas

def carregar_todos_os_cards(driver):
    scroll_pause = 1.5
    scroll_step = 400
    max_tentativas = 15
    tentativas = 0
    total_anterior = 0

    while tentativas < max_tentativas:
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        time.sleep(scroll_pause)
        cards = driver.find_elements(By.XPATH, '//*[@id="imoveis"]/div')
        total_atual = len(cards)

        if total_atual > total_anterior:
            total_anterior = total_atual
            tentativas = 0
        else:
            tentativas += 1

    return total_anterior

def raspar_pagina():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(url)
        time.sleep(3)

        print("Carregando todos os cards com scroll...")
        total_cards = carregar_todos_os_cards(driver)
        print(f"Total de cards carregados: {total_cards}")

        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        dados = []

        for i in range(1, total_cards + 1):
            try:
                xpath_card = f'//*[@id="imoveis"]/div[{i}]'
                card = driver.find_element(By.XPATH, xpath_card)
                driver.execute_script("arguments[0].scrollIntoView();", card)
                time.sleep(1)

                # Verifica se o card possui uma tag <a>
                link_elements = card.find_elements(By.TAG_NAME, "a")
                if not link_elements:
                    print(f" Card {i} ignorado - sem tag <a> (provavelmente propaganda).")
                    continue

                url_imovel = link_elements[0].get_attribute("href")

                if not url_imovel or "/imovel/" not in url_imovel:
                    print(f" Card {i} ignorado - link não é de imóvel.")
                    continue

                driver.execute_script(f"window.open('{url_imovel}', '_blank');")
                driver.switch_to.window(driver.window_handles[1])

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "p.endereco"))
                    )
                except TimeoutException:
                    print(f"⏳ Timeout esperando o endereço no card {i}")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                endereco, caracteristicas = extrair_endereco(driver)
                print(f"Endereço do card {i}: {endereco}")
                print(f"Características: {caracteristicas}")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

                dados.append({
                    "card": i,
                    "url": url_imovel,
                    "endereco": endereco,
                    "caracteristicas": caracteristicas
                })

            except Exception as e:
                print(f"Erro no card {i} - {e}")
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                continue

        return dados

    finally:
        driver.quit()

if __name__ == "__main__":
    print("Iniciando scraping...")
    resultados = raspar_pagina()

    with open('resultados_imoveis.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"\nColeta finalizada! {len(resultados)} imóveis processados.")
