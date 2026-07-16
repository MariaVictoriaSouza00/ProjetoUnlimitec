import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def obter_titulos_fapesp():
    url = "https://fapesp.br/2185/chamadas-de-propostas-2026"

    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    dados = []

    for a in soup.select("p > a"):
        titulo = a.get_text(strip=True)
        link = a.get("href")

        if not link:
            continue

        if not link.startswith("http"):
            link = "https://fapesp.br" + link

        dados.append({
            "titulo": titulo,
            "link": link
        })

    print(f"FAPESP: {len(dados)} chamadas encontradas")
    return dados

