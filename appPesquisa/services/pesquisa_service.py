from appPesquisa.scrapers.finep import obter_titulos_finep
from appPesquisa.scrapers.cnpq import obter_titulos_cnpq
from appPesquisa.scrapers.fapesp import obter_titulos_fapesp

from appPesquisa.services.sinonimos import obter_sinonimos_api

from appPesquisa.services.gemini import resumir_texto_com_gemini

MAX_RESUMOS_COM_GEMINI = 3


def pesquisar_editais(termo):

    titulos = []

    titulos.extend(obter_titulos_finep())

    titulos.extend(obter_titulos_cnpq())

    titulos.extend(obter_titulos_fapesp())

    if termo:

        sinonimos = obter_sinonimos_api(termo)

        titulos = [
            t
            for t in titulos
            if any(
                palavra in t.get("titulo", "").lower()
                or palavra in t.get("resumo", "").lower()
                for palavra in sinonimos
            )
        ]

    resumidos = 0

    for titulo in titulos:

        if resumidos >= MAX_RESUMOS_COM_GEMINI:
            break

        resumo = titulo.get("resumo", "")

        if resumo:

            titulo["resumo"] = resumir_texto_com_gemini(resumo)

            resumidos += 1

    return titulos