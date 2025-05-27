from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def obter_titulos_cnpq():
    dados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        )

        url = "http://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas&ano=2025"
        page.goto(url)
        page.wait_for_selector("div.content h4")

        soup = BeautifulSoup(page.content(), "html.parser")
        elementos = soup.select("div.content h4")

        for h4 in elementos:
            titulo = h4.get_text(strip=True)

            # Obtém o link
            link_tag = h4.find_parent("a")
            link = link_tag["href"] if link_tag and link_tag.has_attr("href") else url

            # Resumo
            paragrafo = ""
            p_tag = h4.find_next_sibling("p")
            if not p_tag:
                parent_div = h4.find_parent("div", class_="content")
                if parent_div:
                    p_tag = parent_div.find("p")
            if p_tag:
                paragrafo = p_tag.get_text(strip=True)

            # Data de inscrição
            data_inscricao = ""
            parent_div = h4.find_parent("div", class_="content")
            if parent_div:
                inscricao_div = parent_div.find("div", class_="inscricao")
                if inscricao_div:
                    li_tag = inscricao_div.find("li")
                    if li_tag:
                        data_inscricao = li_tag.get_text(strip=True)

            dados.append({
                "titulo": titulo,
                "link": link,
                "resumo": paragrafo,
                "prazo_envio": data_inscricao
            })

        browser.close()

    return dados
