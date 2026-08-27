import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL_BASE = "https://www.finep.gov.br"
URL_OPORTUNIDADES = f"{URL_BASE}/oportunidades"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


def obter_titulos_finep():

    resultados = []

    session = requests.Session()
    session.headers.update(HEADERS)

    try:

        # =====================================================
        # 1. ABRE A PÁGINA PRINCIPAL
        # =====================================================

        response = session.get(
            URL_OPORTUNIDADES,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # =====================================================
        # 2. LOCALIZA "BUSCAR POR OPORTUNIDADES"
        # =====================================================

        link_busca = None

        for a in soup.find_all("a", href=True):

            texto = a.get_text(
                " ",
                strip=True
            ).lower()

            if "buscar por oportunidades" in texto:

                link_busca = urljoin(
                    URL_OPORTUNIDADES,
                    a["href"]
                )

                break

        if not link_busca:

            print(
                "[FINEP] Link 'Buscar por oportunidades' não encontrado."
            )

            return resultados

        print(
            f"[FINEP] Página de busca: {link_busca}"
        )

        # =====================================================
        # 3. ABRE A PÁGINA DE BUSCA
        # =====================================================

        response = session.get(
            link_busca,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # =====================================================
        # 4. LOCALIZA OS CARDS
        # =====================================================

        cards = soup.select(
            "div.produto-card"
        )

        print(
            f"[FINEP] Cards encontrados nesta página: {len(cards)}"
        )

        # =====================================================
        # 5. EXTRAI TÍTULO E LINK
        # =====================================================

        for card in cards:

            # -------------------------------------------------
            # TÍTULO
            # -------------------------------------------------

            titulo_elemento = card.select_one(
                "h2.card-title"
            )

            if not titulo_elemento:
                continue

            titulo = titulo_elemento.get_text(
                " ",
                strip=True
            )

            if not titulo:
                continue

            # -------------------------------------------------
            # LINK
            # -------------------------------------------------

            link_elemento = card.select_one(
                "a[href]"
            )

            if link_elemento:

                href = link_elemento.get(
                    "href",
                    ""
                ).strip()

                link = urljoin(
                    link_busca,
                    href
                )

            else:

                link = None

            # -------------------------------------------------
            # ADICIONA
            # -------------------------------------------------

            resultados.append({
                "titulo": titulo,
                "link": link
            })

        # =====================================================
        # 6. REMOVE DUPLICADOS
        # =====================================================

        resultados_unicos = []

        links_processados = set()

        for item in resultados:

            chave = item["link"] or item["titulo"]

            if chave in links_processados:
                continue

            links_processados.add(chave)

            resultados_unicos.append(item)

        resultados = resultados_unicos

        # =====================================================
        # 7. MOSTRA RESULTADOS
        # =====================================================
       
        print(
            f"[FINEP] Total encontrado: {len(resultados)}"
        )

        for item in resultados:

            print(
                f"- {item['titulo']}"
            )

            print(
                f"  {item['link']}"
            )

    except requests.RequestException as erro:

        print(
            f"[FINEP] Erro HTTP: {erro}"
        )

    except Exception as erro:

        print(
            f"[FINEP] Erro: {erro}"
        )

    return resultados