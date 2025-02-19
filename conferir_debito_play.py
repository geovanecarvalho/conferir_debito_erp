from playwright.sync_api import sync_playwright, TimeoutError
from unidecode import unidecode
import os, csv, requests
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis de ambiente
ERP_USERNAME = os.getenv('ERP_USERNAME')
ERP_PASSWORD = os.getenv('ERP_PASSWORD')
CONTA_AZUL_USERNAME = os.getenv('CONTA_AZUL_USERNAME')
CONTA_AZUL_PASSWORD = os.getenv('CONTA_AZUL_PASSWORD')

STATUS_ERP = ""
STATUS_AZUL = ""
STATUS = ""
LOGIN_ERP = 0
LOGIN_AZUL = 0

todos_cpf = []

# Função para carregar os CPFs do arquivo cpf.txt
def carregar_cpfs():
    with open("cpf.txt", "r") as file:
        arquivo = file.readlines()
        return [i.strip() for i in arquivo]

# Função para fazer login no ERP
def login_erp(page):
    global LOGIN_ERP
    if LOGIN_ERP < 1:
        LOGIN_ERP += 1
        sleep(2)
        print("Preenchendo login ERP")
        page.fill('xpath=/html/body/app-root/div/div[2]/ng-component/div/div/form/span[1]/input', ERP_USERNAME)
        sleep(2)
        page.fill('xpath=/html/body/app-root/div/div[2]/ng-component/div/div/form/span[2]/input', ERP_PASSWORD)
        sleep(2)
        page.click('xpath=/html/body/app-root/div/div[2]/ng-component/div/div/form/button')
        sleep(3)
        print("Login ERP realizado")

# Função para fazer login no Conta Azul
def login_conta_azul(page):
    global LOGIN_AZUL
    if LOGIN_AZUL < 1:
        LOGIN_AZUL += 1
        print("Realizando login no Conta Azul")
        page.goto("https://login.contaazul.com/")
        sleep(5)
        input_login = page.query_selector_all('//input')
        if len(input_login) >= 2:
            input_login[0].fill(CONTA_AZUL_USERNAME)
            input_login[1].fill(CONTA_AZUL_PASSWORD)
            sleep(1)
            page.click('xpath=/html/body/div[4]/div/div[1]/div/div/div[2]/div/div/div[3]/div/div/form/div/div/div[4]/div/div/span/button')
            sleep(30)
            print("Login Conta Azul realizado")
        else:
            print("Erro ao encontrar campos de login no Conta Azul")

# Função para consultar dados no ERP
def consultar_erp(page, cpf):
    global STATUS_ERP
    print(f"Consultando ERP para CPF: {cpf}")
    page.goto("https://jardim-paraiso.devhut.app/login")
    login_erp(page)
    sleep(3)

    dados_erp = extrair_dados_erp(page, cpf)
    if not dados_erp:
        return None

    verificar_status_erp(page, cpf)

    return dados_erp

# Função para extrair dados do ERP
def extrair_dados_erp(page, cpf):
    bairros = ["JARDIM ABC", "MESQUITA", "JARDIM EDITE", "REMANSO", "JARDIM SATELITE", "SETOR MESQUITA", "PQ DAS AMERICAS", "PARQUE DAS AMERICAS", "MAURI DE CASTRO", "DOM BOSCO"]
    sleep(2)

    # Navegar para a nova URL para extrair os dados
    print(f"Navegando para a nova URL para extrair dados para CPF: {cpf}")
    page.goto("https://jardim-paraiso.devhut.app/clientes")
    sleep(5)

    # Preencher o CPF na nova página
    page.fill('xpath=//*[@id="pn_id_2-table"]/thead/tr[2]/th[4]/input', cpf)  # Substitua o XPath pelo correto
    sleep(2)
    page.click('xpath=//*[@id="pn_id_2-table"]/tbody/tr/td[1]')  # Substitua o XPath pelo correto
    sleep(5)

    try:
        consute_cidade = page.locator('xpath=/html/body/app-root/div/div[2]/app-cliente-edit/div/div/div/form/div[7]/div[3]/p-autocomplete/div/input').input_value()
        print(f"Cidade encontrada: {consute_cidade}")
    except TimeoutError as e:
        print(f"Erro ao extrair cidade: {e}")
        consute_cidade = ""

    try:
        consute_bairro = page.locator('xpath=//*[@id="bairro"]').input_value()
        print(f"Bairro encontrado: {consute_bairro}")
    except TimeoutError as e:
        print(f"Erro ao extrair bairro: {e}")
        consute_bairro = ""

    try:
        consute_endereco = page.locator('xpath=/html/body/app-root/div/div[2]/app-cliente-edit/div/div/div/form/div[8]/textarea').input_value()
        print(f"Endereço encontrado: {consute_endereco}")
    except TimeoutError as e:
        print(f"Erro ao extrair endereço: {e}")
        consute_endereco = ""

    try:
        consute_nome = page.locator('xpath=/html/body/app-root/div/div[2]/app-cliente-edit/div/div/div/form/div[2]/textarea').input_value()
        print(f"Nome encontrado: {consute_nome}")
    except TimeoutError as e:
        print(f"Erro ao extrair nome: {e}")
        consute_nome = ""

    print(f"Dados extraídos da nova URL: Nome={consute_nome}, Cidade={consute_cidade}, Bairro={consute_bairro}, Endereço={consute_endereco}")

    if "CIDADE OCIDENTAL" in consute_cidade:
        if consute_bairro in bairros:
            ENTREGA = "CORREIOS"
        else:
            ENTREGA = "MOTO"
    else:
        ENTREGA = "CORREIOS"

    return {
        "NOME": unidecode(consute_nome.upper()),
        "CIDADE": unidecode(consute_cidade.upper()),
        "BAIRRO": unidecode(consute_bairro.upper()),
        "ENDERECO": unidecode(consute_endereco.upper()),
        "ENTREGA": ENTREGA
    }

# Função para verificar o status do cliente no ERP
def verificar_status_erp(page, cpf):
    global STATUS_ERP
    print(f"Verificando status ERP para CPF: {cpf}")
    page.goto("https://jardim-paraiso.devhut.app/central-de-venda")
    sleep(5)
    page.click('xpath=//*[@id="menu-button"]')
    sleep(2)
    page.click('xpath=/html/body/app-root/div/app-topbar/div/span/app-menu/div/p-scrollpanel/div/div[1]/div/div/ul/li[3]/a')
    sleep(2)
    page.fill('xpath=/html/body/app-root/div/div[2]/app-consulta-geral-home/div/app-consulta-geral-cliente/app-cliente-list/p-table/div/div[2]/table/thead/tr[2]/th[4]/input', cpf)
    sleep(2)
    page.click('xpath=/html/body/app-root/div/div[2]/app-consulta-geral-home/div/app-consulta-geral-cliente/app-cliente-list/p-table/div/div[2]/table/tbody/tr/td[1]')
    sleep(2)

    a = page.query_selector_all('td')
    lista_de_datas = []

    print("Função verificar_status_erp chamada")

    for n, i in enumerate(a):
        print("Verificando elemento td")
        if i.text_content() == "MAN":
            n += 3
            if n < len(a):  # Adicionar verificação de limite
                i = a[n]
                data = i.text_content()
                lista_de_datas.append(data)

    print("Lista de datas coletadas:", lista_de_datas)

    if lista_de_datas:
        for data in lista_de_datas:
            if datetime.strptime(data, "%d/%m/%Y") < datetime.today():
                STATUS_ERP = "DEVE-ERP"
                break
        else:
            STATUS_ERP = "ERP-EM-DIA"
    else:
        STATUS_ERP = "ERP-EM-DIA"

    print("STATUS ERP: ", STATUS_ERP)

# Função para consultar dados no Conta Azul
def consultar_conta_azul(page, cpf):
    global STATUS_AZUL
    print(f"Consultando Conta Azul para CPF: {cpf}")
    page.goto("https://app.contaazul.com/#/ca/pessoas/clientes")
    sleep(10)
    page.fill('xpath=//*[@id="gateway"]/section/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/form/div/div/div/div[1]/input', cpf)
    sleep(5)
    page.click('xpath=//*[@id="gateway"]/section/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div/form/div/div/div/div[2]/div/span/button')
    sleep(5)

    try:
        if int(page.text_content('xpath=//*[@id="gateway"]/section/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/ul/li[1]/span')) > 0:
            sleep(2)
            page.click('xpath=//*[@id="gateway"]/section/div[3]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/table/tbody/tr/td[2]')
            sleep(2)
            valor = page.text_content('xpath=//*[@id="ng-app"]/body/div[13]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/span/span')
            sleep(2)

            print(f"Valor encontrado no Conta Azul: {valor}")

            if valor != "0,00":
                STATUS_AZUL = "DEVE-AZUL"
            else:
                STATUS_AZUL = "AZUL-EM-DIA"
        else:
            STATUS_AZUL = "NAO-EXISTE-CADASTRO-AZUL"
    except Exception as e:
        print(f"Erro ao consultar Conta Azul para CPF {cpf}: {e}")
        STATUS_AZUL = "ERRO-CONSULTA-AZUL"

    print("STATUS AZUL: ", STATUS_AZUL)

# Função para salvar os resultados no arquivo CSV
def salvar_resultado(nome, cpf, status, entrega, cidade, bairro, endereco):
    with open('update-endereco.csv', 'a', newline='', encoding='utf-8') as file:
        arquivo = csv.writer(file, delimiter=';')
        arquivo.writerow([nome, cpf, status, entrega, cidade, bairro, endereco])
    print(f"Resultado salvo para CPF: {cpf}")

# Função principal que coordena o fluxo do programa
def main():
    global STATUS
    todos_cpf = carregar_cpfs()
    print(f"Total de CPFs carregados: {len(todos_cpf)}")

    with sync_playwright() as p:
        # Primeiro navegador não headless para login
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Fazer login no ERP
        page.goto("https://jardim-paraiso.devhut.app/login")
        login_erp(page)

        # Fazer login no Conta Azul
        login_conta_azul(page)

        # Fechar o navegador não headless
        browser.close()

        # Segundo navegador headless para operações subsequentes
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for cpf in todos_cpf:
            try:
                print(f"Iniciando processamento para CPF: {cpf}")
                dados_erp = consultar_erp(page, cpf)
                if dados_erp:
                    consultar_conta_azul(page, cpf)
                    STATUS = STATUS_ERP + "-" + STATUS_AZUL
                    salvar_resultado(dados_erp["NOME"], cpf, STATUS, dados_erp["ENTREGA"], dados_erp["CIDADE"], dados_erp["BAIRRO"], dados_erp["ENDERECO"])
                else:
                    salvar_resultado("", cpf, "NAO-EXISTE-CADASTRO-ERP", "", "", "", "")
            except Exception as e:
                print(f"Erro ao processar CPF {cpf}: {e}")
                salvar_resultado("", cpf, "ERRO-DE-LEITURA", "", "", "", "")
                continue
            sleep(5)

        browser.close()

if __name__ == "__main__":
    main()