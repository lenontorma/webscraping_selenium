import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



chrome_options = Options()
#chrome_options.add_argument("--headless") # Executar em modo headless (sem interface gráfica)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


try:
    driver = webdriver.Chrome(options=chrome_options)
    print("Navegador Chrome iniciado com sucesso!")
    driver.get("https://casaraoimoveis.com.br/imoveis/vendas/pelotas/todos-os-tipos/?")
    print(f"Título da página: {driver.title}")
    time.sleep(2) # Espera para visualização
except Exception as e:
    print(f"Erro ao iniciar o navegador: {e}")


def fetch_page(url: str) -> str:
    response = requests.get(url)
    return response.text

def parse_page(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    divs_com_classe = soup.find_all('div', class_='card-imovel-info')
    for div in divs_com_classe:
        print(f"Div com classe 'item-lista': {div.text}")
    


if __name__ == "__main__":
    url = 'https://casaraoimoveis.com.br/imoveis/vendas/pelotas/todos-os-tipos/?'
    html = fetch_page(url)
    parse = parse_page(html)
