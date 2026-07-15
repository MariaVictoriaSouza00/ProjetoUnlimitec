import requests
from bs4 import BeautifulSoup

def obter_parceiros():
    url = "https://www.facom.ufms.br/laboratorios/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        parceiros = []

        blocos = soup.find_all("div", class_="elementor-widget-wrap")

        for i, bloco in enumerate(blocos):

            # 🔥 IGNORA O PRIMEIRO BLOCO
            if i == 0:
                continue

            h2s = bloco.find_all("h2")

            if len(h2s) < 2:
                continue

            titulo = h2s[0].get_text(strip=True)
            descricao = h2s[1].get_text(strip=True)

            # 🔥 FILTRO EXTRA (evita lixo tipo #pesquisa)
            if "LABORATÓRIO" not in titulo.upper():
                continue

            link_tag = bloco.find("a", href=True)
            link = link_tag["href"] if link_tag else "#"

            parceiros.append({
                "titulo": titulo,
                "descricao": descricao,
                "site": link
            })

        return parceiros

    except Exception as e:
        print("ERRO SCRAPER:", e)
        return []