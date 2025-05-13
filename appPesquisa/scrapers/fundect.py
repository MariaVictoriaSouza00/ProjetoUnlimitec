from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appPesquisa.scrapers.utils import configurar_driver

def obter_titulos_fundect():
    dados = []
    
    # Configura o driver (agora com o webdriver-manager)
    driver = configurar_driver()

    try:
        # Acessa a página de chamadas da FUNDECT
        driver.get("https://www.fundect.ms.gov.br/category/chamadas-abertas/")

        # Espera até que os cards estejam visíveis na página
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card-body"))
        )

        # Obtém o HTML da página usando BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.select("div.card-body")

        for card in cards:
            link_tag = card.find("a", href=True)
            titulo_tag = card.find("h5", class_="card-title")

            if link_tag and titulo_tag:
                link = link_tag["href"].strip()
                titulo = titulo_tag.get_text(strip=True)

                # Garante que o link seja absoluto
                if not link.startswith("http"):
                    link = "https://www.fundect.ms.gov.br" + link

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

                # Junta os parágrafos encontrados para formar o resumo
                textoResumo = " ".join(p.get_text(strip=True) for p in paragrafos)

                # Adiciona os dados à lista
                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": textoResumo
                })

    except Exception as e:
        print("Erro na FUNDECT:", e)
    finally:
        driver.quit()  # Garante que o driver seja fechado corretamente

    return dados
