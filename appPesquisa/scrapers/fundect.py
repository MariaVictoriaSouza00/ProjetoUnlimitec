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

                # Acessa a página da chamada
                driver.get(link)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "p"))
                )

                detalhe_soup = BeautifulSoup(driver.page_source, "html.parser")

                # Tenta primeiro <div id="content">
                content_div = detalhe_soup.find("div", id="content")
                paragrafos = content_div.find_all("p") if content_div else []

                # Se não houver conteúdo em <div id="content">, tenta <div class="text">
                if not paragrafos:
                    text_div = detalhe_soup.find("div", class_="text")
                    if text_div:
                        paragrafos = text_div.find_all("p")

                # Junta os parágrafos encontrados
                textoResumo = " ".join(p.get_text(strip=True) for p in paragrafos)

                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": textoResumo
                })

    except Exception as e:
        print("Erro na FUNDECT:", e)
    finally:
        driver.quit()

    return dados
