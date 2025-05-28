import requests
from bs4 import BeautifulSoup

def obter_titulos_cnpq():
    dados = []
    url = "http://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas&ano=2025"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    elementos = soup.select("div.content h4")

    for h4 in elementos:
        titulo = h4.get_text(strip=True)
        link_tag = h4.find_parent("a")
        link = link_tag["href"] if link_tag and link_tag.has_attr("href") else url

        paragrafo = ""
        p_tag = h4.find_next_sibling("p")
        if not p_tag:
            parent_div = h4.find_parent("div", class_="content")
            if parent_div:
                p_tag = parent_div.find("p")
        if p_tag:
            paragrafo = p_tag.get_text(strip=True)

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
    return dados
