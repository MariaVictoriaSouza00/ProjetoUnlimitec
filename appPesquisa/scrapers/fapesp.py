import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3
import re


# Desabilita avisos do verify=False
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


def obter_titulos_fapesp():

    dados = []

    url = "https://fapesp.br/2185/chamadas-de-propostas-2026"
    url_base = "https://fapesp.br"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
            verify=False
        )

        response.raise_for_status()

    except requests.RequestException as e:

        print(
            "Erro ao acessar página da FAPESP:",
            e
        )

        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # ==========================================================
    # PROCURA TODAS AS REFERÊNCIAS:
    #
    # Chamada FAPESP 41/2026
    # Chamada FAPESP 40/2026
    # ...
    # Chamada FAPESP 01/2026
    # ==========================================================

    chamadas_encontradas = {}

    textos = soup.find_all(
        string=re.compile(
            r"Chamada FAPESP\s+\d{1,2}/2026",
            re.IGNORECASE
        )
    )

    for texto_chamada in textos:

        texto = texto_chamada.strip()

        match = re.search(
            r"Chamada FAPESP\s+(\d{1,2})/2026",
            texto,
            re.IGNORECASE
        )

        if not match:
            continue

        numero = int(match.group(1))

        # ======================================================
        # SOBE NA ÁRVORE HTML
        # ======================================================

        elemento = texto_chamada.parent

        # Em vez de limitar a 5 níveis,
        # sobe até encontrar links relacionados.
        for _ in range(10):

            if not elemento:
                break

            links = elemento.find_all(
                "a",
                href=True
            )

            links_validos = []

            for link_tag in links:

                href = link_tag.get(
                    "href",
                    ""
                ).strip()

                titulo = link_tag.get_text(
                    " ",
                    strip=True
                )

                if not href or not titulo:
                    continue

                link = urljoin(
                    url_base,
                    href
                )

                # Somente FAPESP
                if not link.startswith(
                    "https://fapesp.br/"
                ):
                    continue

                # Não pegar páginas de anos anteriores
                if "/chamadas-de-propostas-" in link.lower():
                    continue

                # Não pegar resultados
                if titulo.lower() == "resultado":
                    continue

                links_validos.append(
                    (titulo, link)
                )

            # ==================================================
            # SE ENCONTROU LINK, GUARDA
            # ==================================================

            if links_validos:

                # Normalmente o primeiro link é a chamada
                titulo, link = links_validos[0]

                chamadas_encontradas[numero] = {
                    "titulo": titulo,
                    "link": link
                }

                break

            elemento = elemento.parent

    # ==========================================================
    # TRANSFORMA EM LISTA
    # ORDENADA DA 41/2026 ATÉ 01/2026
    # ==========================================================

    for numero in sorted(
        chamadas_encontradas.keys(),
        reverse=True
    ):

        dados.append(
            chamadas_encontradas[numero]
        )

    # ==========================================================
    # DIAGNÓSTICO
    # ==========================================================

    numeros_encontrados = set(
        chamadas_encontradas.keys()
    )

    numeros_esperados = set(
        range(1, 42)
    )

    faltando = sorted(
        numeros_esperados - numeros_encontrados,
        reverse=True
    )

    print(
        f"\nTotal encontrado: {len(dados)}"
    )

    if faltando:

        print(
            "Chamadas que não foram encontradas:"
        )

        for numero in faltando:

            print(
                f" - Chamada FAPESP "
                f"{numero:02d}/2026"
            )

    else:

        print(
            "Todas as 41 chamadas foram encontradas!"
        )

    return dados

