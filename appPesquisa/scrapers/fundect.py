from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def obter_titulos_fundect():
    dados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.fundect.ms.gov.br/category/chamadas-abertas/")
        page.wait_for_selector(".card-body")

        soup = BeautifulSoup(page.content(), "html.parser")
        cards = soup.select("div.card-body")

        for card in cards:
            link_tag = card.find("a", href=True)
            titulo_tag = card.find("h5", class_="card-title")

            if link_tag and titulo_tag:
                link = link_tag["href"].strip()
                if not link.startswith("http"):
                    link = "https://www.fundect.ms.gov.br" + link
                titulo = titulo_tag.get_text(strip=True)

                # Vai para a página do item
                page.goto(link)
                page.wait_for_selector("p")

                detalhe_soup = BeautifulSoup(page.content(), "html.parser")
                content_div = detalhe_soup.find("div", id="content")
                paragrafos = content_div.find_all("p") if content_div else []

                if not paragrafos:
                    text_div = detalhe_soup.find("div", class_="text")
                    if text_div:
                        paragrafos = text_div.find_all("p")

                resumo = " ".join(p.get_text(strip=True) for p in paragrafos)
                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": resumo
                })

        browser.close()
    return dados
