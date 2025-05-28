import requests
from bs4 import BeautifulSoup

def obter_titulos_finep():
    dados = []
    url_base = "http://www.finep.gov.br"
    url = f"{url_base}/chamadas-publicas/chamadaspublicas?pchave=&situacao=aberta&d1=01-01-2025"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    elementos = soup.select("div.item h3 a")

    for el in elementos:
        titulo = el.get_text(strip=True)
        link = el["href"].strip()
        if not link.startswith("http"):
            link = url_base + link

        # acessa página individual
        try:
            detalhe_res = requests.get(link)
            detalhe_soup = BeautifulSoup(detalhe_res.text, "html.parser")
            campos = detalhe_soup.select_one("div.item_fields")

            descricao = ""
            prazo_envio = ""
            publico_alvo = ""
            data_publicacao = ""

            desc = campos.select_one("div.group.desc .text") if campos else None
            if desc:
                descricao = desc.get_text(separator="\n", strip=True)

            for grupo in campos.select("div.group") if campos else []:
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
            print(f"Erro ao acessar detalhes: {link} - {e}")
    return dados
