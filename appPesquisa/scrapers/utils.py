from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver():
    options = Options()
    options.headless = True  # Para rodar sem interface gráfica

    # Se você sabe o caminho do seu navegador, pode adicionar ele aqui:
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Exemplo no Windows

    # Usa o webdriver_manager para configurar o ChromeDriver automaticamente
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver
