from airflow.decorators import dag, task
from datetime import datetime
import os
import json
import tempfile
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@task
def run_extract_task():
    # Configuração do Selenium
    service = Service(log_path=os.devnull)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp(prefix='selenium_')}")
    chrome_options.add_argument("--remote-debugging-port=0")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://casaraoimoveis.com.br/imoveis/alugueis/pelotas/todos-os-tipos/"
        driver.get(url)
        time.sleep(3)

        # Função para carregar todos os cards
        def carregar_todos_os_cards(driver):
            scroll_pause = 2
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

        # Função para extrair endereço e características
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
                        continue
            except Exception:
                pass

            return endereco, caracteristicas

        # Carregar todos os cards
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

                link_elements = card.find_elements(By.TAG_NAME, "a")
                if not link_elements:
                    continue

                url_imovel = link_elements[0].get_attribute("href")
                if not url_imovel or "/imovel/" not in url_imovel:
                    continue

                driver.execute_script(f"window.open('{url_imovel}', '_blank');")
                driver.switch_to.window(driver.window_handles[1])

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "p.endereco"))
                    )
                except TimeoutException:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                endereco, caracteristicas = extrair_endereco(driver)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1.5)

                dados.append({
                    "card": i,
                    "url": url_imovel,
                    "endereco": endereco,
                    "caracteristicas": caracteristicas
                })

            except Exception:
                if len(driver.window_handles) > 1:
                    driver.switch_to.window(driver.window_handles[1])
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                continue

        # Certifica-se de que o diretório 'data' existe
        os.makedirs('data', exist_ok=True)
        with open('data/resultados_raw.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

        print(f"\nColeta finalizada! {len(dados)} imóveis processados.")

    finally:
        driver.quit()


# DAG
@dag(
    dag_id="web_scraper_casarao_imoveis",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["web_scraping", "imoveis"]
)
def run_extract():
    run_extract_task()


# Instancia a DAG
run_extract()
