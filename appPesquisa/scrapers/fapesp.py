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

    # Todos os links da página
    for a in soup.select("p > a"):

        titulo = a.get_text(strip=True)

        link = a.get("href")

        if not link:
            continue

        if not link.startswith("http"):
            link = "https://fapesp.br" + link

        resumo = ""
        prazo_envio = ""
        data_publicacao = ""
        publico_alvo = ""
        modalidade = ""

        try:

            detalhe = requests.get(
                link,
                headers=HEADERS,
                timeout=30
            )

            detalhe.raise_for_status()

            pagina = BeautifulSoup(detalhe.text, "html.parser")
            print("=" * 80)
            print("LINK:", link)

            # Salva o HTML da primeira página para inspeção
            with open("teste_fapesp.html", "w", encoding="utf-8") as f:
                f.write(detalhe.text)

            print("Contém 'Sumário'? ", "Sumário" in detalhe.text)
            print("Contém 'Lançamento da Chamada'? ", "Lançamento da Chamada" in detalhe.text)
            print("Contém 'Prazo para submissão'? ", "Prazo para submissão" in detalhe.text)
            print("Contém 'Data limite'? ", "Data limite" in detalhe.text)
            # ===============================
            # RESUMO
            # ===============================

            paragrafos = pagina.find_all("p")

            for p in paragrafos:

                texto = p.get_text(" ", strip=True)

                if len(texto) > 150 and "sumário" not in texto.lower():

                    resumo = texto

                    break

            # ===============================
            # SUMÁRIO
            # ===============================

            for p in pagina.find_all("p"):

                texto = p.get_text(" ", strip=True)

                if "Sumário" not in texto:
                    continue

                span = p.find("span")

                if span is None:
                    continue

                linhas = span.get_text("\n", strip=True).split("\n")

                for linha in linhas:

                    if ":" not in linha:
                        continue

                    chave, valor = linha.split(":", 1)

                    chave = chave.lower().strip()

                    valor = valor.strip()

                    if "lançamento da chamada" in chave:
                        data_publicacao = valor

                    elif "publicado em" in chave:
                        data_publicacao = valor

                    elif "data limite para submissão" in chave:
                        prazo_envio = valor

                    elif "prazo para apresentação" in chave:
                        prazo_envio = valor

                    elif "prazo para submissão" in chave:
                        prazo_envio = valor

                    elif "modalidade de apoio" in chave:
                        modalidade = valor

                    elif "público-alvo" in chave:
                        publico_alvo = valor

                break

        except Exception as e:
            print(e)

        dados.append({
            "titulo": titulo,
            "resumo": resumo,
            "prazo_envio": prazo_envio,
            "publico_alvo": publico_alvo,
            "data_publicacao": data_publicacao,
            "modalidade": modalidade,
            "link": link,
        })

    print(f"FAPESP: {len(dados)} chamadas encontradas")

    return dados