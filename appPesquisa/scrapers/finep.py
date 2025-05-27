from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def obter_titulos_finep():
    dados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Acessa a página principal das chamadas públicas
        page.goto("http://www.finep.gov.br/chamadas-publicas/chamadaspublicas?pchave=&situacao=aberta&d1=01-01-2025")
        page.wait_for_selector("div.item h3 a")

        soup = BeautifulSoup(page.content(), "html.parser")
        elementos = soup.select("div.item h3 a")

        for el in elementos:
            titulo = el.get_text(strip=True)
            link = el["href"].strip()

            if not link.startswith("http"):
                link = "http://www.finep.gov.br" + link

            try:
                page.goto(link)
                page.wait_for_selector("div.item_fields")

                soup_chamada = BeautifulSoup(page.content(), "html.parser")
                campos = soup_chamada.select_one("div.item_fields")

                descricao = ""
                prazo_envio = ""
                publico_alvo = ""
                data_publicacao = ""

                # Descrição
                desc = campos.select_one("div.group.desc .text")
                if desc:
                    descricao = desc.get_text(separator="\n", strip=True)

                for grupo in campos.select("div.group"):
                    titulo_campo = grupo.select_one("div.tit")
                    valor_campo = grupo.select_one("div.text")

                    if titulo_campo and valor_campo:
                        chave = titulo_campo.get_text(strip=True).lower()
                        valor = valor_campo.get_text(" ", strip=True)

                        if "prazo para envio" in chave:
                            prazo_envio = valor
                        elif "público-alvo" in chave:
                            publico_alvo = valor
                        elif "data de publicação" in chave:
                            data_publicacao = valor

                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": descricao,
                    "prazo_envio": prazo_envio,
                    "publico_alvo": publico_alvo,
                    "data_publicacao": data_publicacao
                })

            except Exception as e:
                print(f"Erro ao acessar detalhes da chamada: {link} - {e}")

        browser.close()

    return dados
