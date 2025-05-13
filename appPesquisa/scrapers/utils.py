from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver():
    options = Options()
    options.add_argument("--headless")  # Executa sem interface gráfica
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Configura o ChromeDriver automaticamente
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    return driver
