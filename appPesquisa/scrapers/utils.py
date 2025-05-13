import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def configurar_driver():
    options = Options()
    options.add_argument("--headless")  # Executa sem interface gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Tentando encontrar o Google Chrome no sistema
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Caminho padrão do Chrome
    chromium_path = "C:/Caminho/para/o/Chromium/chrome.exe"  # Caminho do Chromium se necessário

    # Verifica se o Google Chrome está instalado, caso contrário, use o Chromium
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
