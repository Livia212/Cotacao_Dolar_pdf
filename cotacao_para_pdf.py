# Código Python que implementa a automação descrita no trabalho
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from reportlab.pdfgen import canvas
import time
import os

# Função para capturar a cotação do dólar
def capturar_cotacao():
    try:
        # Configurar o Selenium
        service = Service('./chromedriver')  # Ajuste o caminho do chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Executar sem abrir o navegador
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(service=service, options=options)

        # Acessar o site de cotação
        url = "https://www.google.com/search?q=cotação+dólar"
        driver.get(url)
        time.sleep(2)  # Aguardar o carregamento da página

        # Capturar o valor da cotação
        elemento_cotacao = driver.find_element(By.XPATH, "//span[contains(@class, 'DFlfde')]")
        cotacao = elemento_cotacao.text

        driver.quit()
        return cotacao

    except Exception as e:
        print(f"Erro ao capturar cotação: {e}")
        return None

# Função para gerar o PDF com a cotação
def gerar_pdf(cotacao):
    nome_arquivo = "cotacao_dolar.pdf"
    c = canvas.Canvas(nome_arquivo)
    c.drawString(100, 750, "Relatório de Cotação do Dólar")
    c.drawString(100, 700, f"Cotação atual do dólar: {cotacao}")
    c.drawString(100, 650, f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    c.save()

    # Abrir o PDF automaticamente
    os.startfile(nome_arquivo)  # Isso abrirá o PDF com o aplicativo padrão

    print(f"Relatório salvo como: {nome_arquivo}")
    
    return nome_arquivo

# Fluxo principal
cotacao_dolar = "4.95"  # Exemplo manual (vou implementar a geração do PDF)
if cotacao_dolar:
    nome_pdf = gerar_pdf(cotacao_dolar)
    print(f"Relatório gerado: {nome_pdf}")
else:
    print("Não foi possível capturar a cotação.")

# Confirmar a existência do arquivo PDF gerado
os.path.exists(nome_pdf)
