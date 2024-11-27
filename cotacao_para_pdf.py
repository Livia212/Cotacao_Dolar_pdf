# Código Python que implementa a automação descrita no trabalho
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.pdfgen import canvas
import time
import os
import subprocess

# Função para capturar a cotação de uma moeda
def capturar_cotacao(moeda):
    try:
        # Configurar o WebDriver, pois o Selenium usando o Chromedriver não tava pegando
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Executar sem abrir o navegador
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Acessar o site de cotação
        url = f"https://www.google.com/search?q=cotação+{moeda}"
        driver.get(url)

        # Aguarde o carregamento do valor na pagina
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='DFlfde SwHCTb' and @data-precision='2']"))
        )

        # Captura o valor da cotação
        elemento_cotacao = driver.find_element(By.XPATH, "//span[@class='DFlfde SwHCTb' and @data-precision='2']")
        cotacao = elemento_cotacao.text
        driver.quit()
        return cotacao

    except Exception as e:
        print(f"Erro ao capturar cotação para {moeda}: {e}")
        return None

# Função para gerar o PDF
def gerar_pdf(cotacoes):
    nome_arquivo = "cotacoes_moedas_corrigido.pdf"
    c = canvas.Canvas(nome_arquivo)
    c.drawString(100, 750, "Relatório de Cotações")
    y = 700
    for moeda, cotacao in cotacoes.items():
        c.drawString(100, y, f"Cotação atual de {moeda}: {cotacao}")
        y -= 50
    c.drawString(100, y, f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    c.save()

    print(f"Relatório salvo como: {nome_arquivo}")
    return nome_arquivo

# Função para abrir o PDF
def abrir_pdf(nome_arquivo):
    if os.name == 'nt':  # Para Windows
        os.startfile(nome_arquivo)
    elif os.name == 'posix':  # Para MacOS/Linux
        subprocess.run(['open', nome_arquivo])  # Para MacOS
        # subprocess.run(['xdg-open', nome_arquivo])  # Para Linux
    else:
        print("Sistema operacional não suportado para abrir o PDF automaticamente.")

# Fluxo principal
moedas = ["euro", "dólar", "libra"]
cotacoes = {moeda: capturar_cotacao(moeda) or "Erro" for moeda in moedas}

# Gera o PDF
nome_pdf = gerar_pdf(cotacoes)

# Abre o PDF após gerar
abrir_pdf(nome_pdf)


