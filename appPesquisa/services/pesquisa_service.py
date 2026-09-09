
import unicodedata
from appPesquisa.scrapers.finep import obter_titulos_finep
from appPesquisa.scrapers.cnpq import obter_titulos_cnpq
from appPesquisa.scrapers.fapesp import obter_titulos_fapesp
#from appPesquisa.scrapers.fapergs import obter_titulos_fapergs

from appPesquisa.services.sinonimos import obter_sinonimos_api

from appPesquisa.services.gemini import resumir_texto_com_gemini

MAX_RESUMOS_COM_GEMINI = 3


# def pesquisar_editais(termo):

#     titulos = []

#     # titulos.extend(obter_titulos_finep())

#     # titulos.extend(obter_titulos_cnpq())

#     titulos.extend(obter_titulos_fapesp())
#    # titulos.extend(obter_titulos_fapergs())

#     print(titulos)
#     print({len(titulos)})
#     return titulos


def remover_acentos(texto):
    texto = str(texto)

    return ''.join(
        caractere
        for caractere in unicodedata.normalize('NFD', texto)
        if unicodedata.category(caractere) != 'Mn'
    ).lower()

  
def pesquisar_editais(termo):

    titulos = []

    # titulos.extend(obter_titulos_finep())
    titulos.extend(obter_titulos_cnpq())
    titulos.extend(obter_titulos_fapesp())
    # titulos.extend(obter_titulos_fapergs())

    # Remove acentos do termo pesquisado
    termo = remover_acentos(termo.strip())

    resultados = [
        edital
        for edital in titulos
        if any(
            termo in remover_acentos(edital.get(campo, ""))
            for campo in ["titulo", "link", "resumo", "prazo_envio"]
        )
    ]

    print(f"Total encontrados: {len(resultados)}")

    return resultados