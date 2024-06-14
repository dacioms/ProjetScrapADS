#Camila e Maria

from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

driver.get('https://www.glassdoor.com.br/Vaga/niter%C3%B3i-rio-de-janeiro-brasil-python-vagas-SRCH_IL.0,29_IC2409809_KO30,36.htm')

time.sleep(5)

html_dinamico = driver.page_source

soup_dinamico = BeautifulSoup(html_dinamico, 'html.parser')

nome_empresaList = []
nome_vagaList = []
localList = []


div_completa = soup_dinamico.find_all('div', class_="jobCard JobCard_jobCardContent__X81Ew JobCardWrapper_easyApplyLabelNoWrap__PtpgT")

for elemento in div_completa:

    nome_empresa = elemento.find('span', class_="EmployerProfile_compactEmployerName__LE242")
    nome_vaga = elemento.find('a', class_="JobCard_jobTitle___7I6y")
    local = elemento.find('div', class_="JobCard_location__rCz3x")
 

    if nome_empresa and nome_vaga:
      
        nome_empresaList.append(nome_empresa.getText().strip())
        nome_vagaList.append(nome_vaga.getText().strip())
        localList.append(local.getText().strip())
    
        
        print("Nome empresa:", nome_empresa.getText().strip())
        print("Nome vaga:", nome_vaga.getText().strip())
        print("Local:", local.getText().strip())
   


driver.quit()

git config --global user.name "Fulano de Tal"
$ git config --global user.email fulanodetal@exemplo.br