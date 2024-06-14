from bs4 import BeautifulSoup
import pandas as pd
import requests

def request(url):
    try:
        response = requests.get(url)
        return response
    except ConnectionError:
        print("Erro de conexão. Verifique sua rede e o URL.")
    except TimeoutError:
        print("A solicitação demorou muito tempo para responder. Tente novamente mais tarde.")
    except Exception as ex:
        print(f"Erro inesperado: {ex}")

def raspar_dados(response):
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            titulo = []
            salario = []
            descricao = []
            empresa = []
            for product in soup.find_all('div', class_='job_seen_beacon'):
                titulo = product.find_all('span', id_='jobTitle-370eb6c01e1bc650').get_text()
                #preco = product.find('span', class_='andes-money-amount__fraction').get_text()
                #link = product.select_one('a')['href']
                titulo.append(titulo)
                #precos.append(preco)
                #links.append(link)
            return titulo
        else:
            print("Não foi possível acessar o site.")
    except Exception as erro:
            print(f'Erro inesperado {erro}')


url = 'https://br.indeed.com/jobs?q=python&l='
response = request(url)
print(response)
titulo = raspar_dados(response)