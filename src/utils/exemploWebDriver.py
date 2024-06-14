from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do Selenium
def configure_selenium():
    options = Options()
    options.add_argument("--headless")  # Executa o navegador em modo headless (sem GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Função para fazer scraping da página
def scrape_page(url, driver, headers, cookies):
    driver.get(url)
    time.sleep(random.uniform(2, 7))  # Delay aleatório para simular comportamento humano
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')

# Função para obter proxies
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    for row in soup.find('table', id='proxylisttable').tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].text,
            'port': row.find_all('td')[1].text
        })
    return proxies

# Função para usar proxies em requisições
def fetch_url_with_proxy(url, proxies):
    for proxy in proxies:
        try:
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            response = requests.get(url, proxies={"http": proxy_url, "https": proxy_url}, headers = headers, cookies = cookies, timeout=5)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logging.warning(f"Proxy {proxy_url} falhou. - {e}")
            continue
    return None

def get_initial_cookies(url, headers):
    session = requests.Session()
    response = session.get(url, headers=headers)
    return session.cookies.get_dict()


# Função principal de scraping
def main_scraping():
    base_url = "https://www.example.com/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.example.com"
    }
    proxies = get_proxies()
    cookies = get_initial_cookies(base_url, headers)
    html_content = fetch_url_with_proxy(base_url, proxies, headers, cookies)
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
    else:
        print("Failed to fetch the page using proxies.")
    
    return soup




# Execução do código
if __name__ == "__main__":
    try: 
        with open("dados.html", "x") as file:
            soup = main_scraping()
            file.write(soup)
    except:
        soup = main_scraping()
        print("O arquivo já existe na pasta")
    finally:
        with open("dados.html", "r") as file:
            soup = file.read()