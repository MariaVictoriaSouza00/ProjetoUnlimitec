import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver():
    options = Options()
    options.add_argument("--headless")  # Executa sem interface gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Caminhos para o Chrome e o Chromium
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Caminho do Chrome
    chromium_path = "C:/chromium/chrome.exe"  # Caminho do Chromium (caso você tenha instalado)

    # Verifica se o Google Chrome está instalado, caso contrário, usa o Chromium
    if not os.path.exists(chrome_path):
        if os.path.exists(chromium_path):
            print("Chrome não encontrado, usando Chromium.")
            options.binary_location = chromium_path  # Usar o Chromium
        else:
            print("Chrome nem Chromium encontrado! Certifique-se de que um dos navegadores esteja instalado.")
            raise Exception("Navegador não encontrado")
    else:
        options.binary_location = chrome_path  # Usar o Google Chrome

    # Configura o WebDriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    return driver
