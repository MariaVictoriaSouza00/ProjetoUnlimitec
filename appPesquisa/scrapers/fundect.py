from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appPesquisa.scrapers.utils import configurar_driver

def obter_titulos_fundect():
    dados = []
    driver = configurar_driver()
    try:
        driver.get("https://www.fundect.ms.gov.br/category/chamadas-abertas/")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-body"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.select("div.card-body")

        for card in cards:
            link_tag = card.find("a", href=True)
            titulo_tag = card.find("h5", class_="card-title")

            if link_tag and titulo_tag:
                link = link_tag["href"].strip()
                titulo = titulo_tag.get_text(strip=True)
                dados.append({"titulo": titulo, "link": link})
                
    except Exception as e:
        print("Erro na FUNDECT:", e)
    finally:
        driver.quit()

    return dados
