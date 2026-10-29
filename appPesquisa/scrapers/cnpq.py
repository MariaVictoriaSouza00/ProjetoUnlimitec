
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def obter_titulos_cnpq():
    dados = []

    urls = [
        "https://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas&ano=2026",
        "https://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=encerradas&ano=2026"
    ]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    }

    with requests.Session() as sessao:
        sessao.headers.update(headers)

        for url in urls:
            try:
                res = sessao.get(url, timeout=20)
                res.raise_for_status()

            except requests.RequestException as erro:
                print(f"Erro ao consultar CNPq: {erro}")
                continue

            soup = BeautifulSoup(res.text, "html.parser")
            elementos = soup.select("div.content h4")

            for h4 in elementos:
                titulo = h4.get_text(strip=True)

                link_tag = h4.find_parent("a")

                link = (
                    urljoin(res.url, link_tag["href"])
                    if link_tag and link_tag.has_attr("href")
                    else res.url
                )

                paragrafo = ""
                p_tag = h4.find_next_sibling("p")

                if not p_tag:
                    parent_div = h4.find_parent(
                        "div", class_="content"
                    )

                    if parent_div:
                        p_tag = parent_div.find("p")

                if p_tag:
                    paragrafo = p_tag.get_text(strip=True)

                data_inscricao = ""
                parent_div = h4.find_parent(
                    "div", class_="content"
                )

                if parent_div:
                    inscricao_div = parent_div.find(
                        "div", class_="inscricao"
                    )

                    if inscricao_div:
                        li_tag = inscricao_div.find("li")

                        if li_tag:
                            data_inscricao = li_tag.get_text(
                                strip=True
                            )

                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": paragrafo,
                    "prazo_envio": data_inscricao
                })

    print(f"Total encontrado CNPq: {len(dados)}")
    return dados
