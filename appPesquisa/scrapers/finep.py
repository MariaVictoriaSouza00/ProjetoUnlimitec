from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appPesquisa.scrapers.utils import configurar_driver

def obter_titulos_finep():
    dados = []
    driver = configurar_driver()
    try:
        driver.get("http://www.finep.gov.br/chamadas-publicas/chamadaspublicas?pchave=&situacao=aberta&d1=01-01-2025")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item h3 a"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        elementos = soup.select("div.item h3 a")

        for el in elementos:
            titulo = el.get_text(strip=True)
            link = el["href"].strip()

            # Links no site da FINEP podem ser relativos. Checa e ajusta.
            if not link.startswith("http"):
                link = "http://www.finep.gov.br" + link

            dados.append({"titulo": titulo, "link": link})

    except Exception as e:
        print("Erro no FINEP:", e)
    finally:
        driver.quit()

    return dados
