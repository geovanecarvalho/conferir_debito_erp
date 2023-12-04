from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from unidecode import unidecode
import os, csv, requests
from datetime import datetime

STATUS_ERP = ""
STATUS_AZUL = ""
STATUS = ""
LOGIN_ERP = 0
LOGIN_AZUL = 0

todos_cpf = []

with open("cpf.txt","r") as file:
    arquivo = file.readlines()
    for i in arquivo:
            todos_cpf.append(i[:-1])



try:
    url_erp = "http://201.57.206.162:6237/jardim/"
    servico = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(service=servico, options=options)
    browser.get(url_erp)

   
    """ ========================================Conta Azul============================================ """
    for cpf in todos_cpf:
        try:
            if LOGIN_ERP < 1:
                LOGIN_ERP += 1
                sleep(2)
                browser.find_element(By.XPATH, "/html/body/app-root/div/div[2]/ng-component/body/div/div/form/div[1]/div/input").send_keys("geovane.oliveira")
                sleep(2)
                browser.find_element(By.XPATH, "/html/body/app-root/div/div[2]/ng-component/body/div/div/form/div[2]/div/input").send_keys("gti@vane")
                sleep(2)
                browser.find_element(By.XPATH, "/html/body/app-root/div/div[2]/ng-component/body/div/div/form/div[3]/button").click()

            sleep(3)
            url_erp = "http://201.57.206.162:6237/jardim/#/consulta-geral/cliente"
            browser.get(url_erp)
            sleep(3)
            browser.find_element(By.XPATH, "/html/body/app-root/div/div[2]/app-consulta-geral-home/div/app-consulta-geral-cliente/app-cliente-list/p-table/div/div[2]/table/thead/tr[2]/th[3]/input").send_keys(cpf)
            sleep(3)
            try:
                browser.find_element(By.XPATH, "/html/body/app-root/div/div[2]/app-consulta-geral-home/div/app-consulta-geral-cliente/app-cliente-list/p-table/div/div[2]/table/tbody/tr[1]").click()
            except:
                STATUS_ERP = "NAO-EXISTE-CADASTRO-ERP"
            
            sleep(5)
            a = browser.find_elements(By.TAG_NAME, "td")
            
            lista_de_datas = []
            
            for n, i in enumerate(a):
                if i.text == "MAN":
                    n += 3
                    i = a[n]
                    data = i.text

                    lista_de_datas.append(data)
            
            if lista_de_datas != []:
                for data in lista_de_datas:
                    if datetime.strptime(data, "%d/%m/%Y") < datetime.today():
                        STATUS_ERP = "DEVE-ERP"
                        break
                    else:
                        STATUS_ERP = "ERP-EM-DIA"
            
            if lista_de_datas == []:
                STATUS_ERP = "ERP-EM-DIA"

            if STATUS_ERP == "NAO-EXISTE-CADASTRO-ERP":
                STATUS_ERP = "NAO-EXISTE-CADASTRO-ERP"
            
            sleep(5)

            """ ========================================Conta Azul============================================ """
            
            
            
            # login no conta azul
            if LOGIN_AZUL < 1:
                url_conta_azul = "https://login.contaazul.com/"
                browser.get(url_conta_azul)
                
                LOGIN_AZUL += 1
                sleep(1)
                browser.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div/div/div[2]/div/div/div[3]/div/div/form/div/div/div[1]/div/div/div/input").send_keys("geovane.oliveira@gmail.com")
                sleep(1)
                browser.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div/div/div[2]/div/div/div[3]/div/div/form/div/div/div[2]/div/div/div/input").send_keys("456123")
                sleep(1)
                browser.find_element(By.XPATH, "/html/body/div[4]/div/div[1]/div/div/div[2]/div/div/div[3]/div/div/form/div/div/div[4]/div/div/span/button").click()
                sleep(5)

            sleep(5)
            url_conta_azul = "https://app.contaazul.com/#/ca/pessoas/clientes"
            browser.get(url_conta_azul)

            sleep(5)
            # Pesquisa CPF
            browser.find_element(By.CSS_SELECTOR, "#gateway > section > div.ds-container.ds-container--auto > div:nth-child(2) > div > div.ds-row > div > div > div.ds-data-grid-header.ds-u-margin-bottom--sm.ds-data-header-container > div.ds-row.ds-row--content-vertical-align-bottom.ds-u-margin-bottom--none > div:nth-child(1) > div > div > form > div > div > div > div.ds-input__container > input").send_keys(cpf)
                            
            sleep(5)
            # Clica em pesquisar
            browser.find_element(By.XPATH, "//*[@id='gateway']/section/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/form/div/div/div/div[2]/div/span/button").click()

            sleep(5)
            # Se existir uma valor clica
            if int(browser.find_element(By.XPATH,'//*[@id="gateway"]/section/div[2]/div[2]/div/div[2]/div/div/div[2]/div/ul/li[1]/span').text) > 0:
                sleep(3)
                browser.find_element(By.XPATH,"//*[@id='gateway']/section/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div/table/tbody/tr/td[2]").click()
                
                sleep(3)
                valor = browser.find_element(By.CSS_SELECTOR,'body > div.ds-rollover.ds-rollover--size-full.ds-rollover--is-opened.ds-rollover--active > div.ds-rollover-container > div.ds-rollover__body.has-footer > div > div > div > div > div:nth-child(1) > div > div > div.ds-total-bar-items > div:nth-child(1) > div > span > span').text
                
                sleep(5)

                if valor != "0,00":
                    STATUS_AZUL = "DEVE-AZUL"
                else:
                    STATUS_AZUL = "AZUL-EM-DIA"
            else:
                STATUS_AZUL = "NAO-EXISTE-CADASTRO-AZUL"
            
            STATUS = STATUS_ERP + "-" + STATUS_AZUL

            print("\n")
            print(cpf, STATUS)
            print("\n")
            with open('update-endereco.csv', 'a', newline='') as file:
                    arquivo = csv.writer(file, delimiter=';')
                    arquivo.writerow([cpf, STATUS])
        except:
            with open('update-endereco.csv', 'a', newline='') as file:
                arquivo = csv.writer(file, delimiter=';')
                arquivo.writerow([cpf, "ERRO-DE-LEITURA"])
            continue
        sleep(5)
except AssertionError:
    print("Erro sem conecxão com internet")
    