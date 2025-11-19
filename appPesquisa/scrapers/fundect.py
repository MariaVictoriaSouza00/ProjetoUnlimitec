import requests
from bs4 import BeautifulSoup

def obter_titulos_fundect():
    dados = []
    url_base = "https://www.fundect.ms.gov.br"

    try:
        res = requests.get(
            f"{url_base}/category/chamadas-abertas/",
            timeout=15,
            verify=False  # evita handshake error
        )
    except Exception as e:
        print("Erro ao acessar página principal da FUNDECT:", e)
        return []  # ← nunca deixe retornar None

    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.select("div.card-body")

    for card in cards:
        link_tag = card.find("a", href=True)
        titulo_tag = card.find("h5", class_="card-title")

        if link_tag and titulo_tag:
            link = link_tag["href"].strip()
            titulo = titulo_tag.get_text(strip=True)

            if not link.startswith("http"):
                link = url_base + link

            try:
                detalhe_res = requests.get(
                    link,
                    timeout=15,
                    verify=False
                )
                detalhe_soup = BeautifulSoup(detalhe_res.text, "html.parser")

                content_div = detalhe_soup.find("div", id="content")
                paragrafos = content_div.find_all("p") if content_div else []

                if not paragrafos:
                    text_div = detalhe_soup.find("div", class_="text")
                    if text_div:
                        paragrafos = text_div.find_all("p")

                textoResumo = " ".join(p.get_text(strip=True) for p in paragrafos)

                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": textoResumo
                })

            except Exception as e:
                print(f"Erro ao acessar detalhes: {link} - {e}")
                continue

    return dados
