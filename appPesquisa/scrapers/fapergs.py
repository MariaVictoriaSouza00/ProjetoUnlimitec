import requests
from bs4 import BeautifulSoup

def obter_titulos_fapergs():
    url_lista = "https://fapergs.rs.gov.br/abertos"
    dados = []

    try:
        # 1. Baixa a página com a lista de editais
        response = requests.get(url_lista, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 2. Seleciona os blocos da lista (equivalente ao seu seletor Selenium)
        elementos = soup.select("div.matriz-ui-pagedlist-body article.conteudo-lista__item")

        for el in elementos:
            try:
                # Título e link
                titulo_tag = el.select_one("h2.conteudo-lista__item__titulo a")
                if not titulo_tag:
                    continue

                titulo = titulo_tag.get_text(strip=True)
                link = titulo_tag["href"]

                # A FAPERGS usa links relativos → corrigimos para link absoluto
                if link.startswith("/"):
                    link = "https://fapergs.rs.gov.br" + link

                # 3. Acessa a página do edital (equivalente ao driver.get)
                response_edital = requests.get(link, timeout=10)
                response_edital.raise_for_status()

                soup_edital = BeautifulSoup(response_edital.text, "html.parser")

                # 4. Extrai o texto do edital (equivalente ao driver.find_element)
                texto_tag = soup_edital.select_one("div.artigo__texto")
                texto = texto_tag.get_text(strip=True) if texto_tag else ""

                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": texto
                })

            except Exception as e:
                # Se algum edital der erro, ignora e segue
                continue

        return dados

    except Exception as e:
        print("Erro no scraper FAPERGS:", e)
        return []
