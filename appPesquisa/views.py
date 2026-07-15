from django.shortcuts import render
from django.http import JsonResponse
import threading
import requests
from django.conf import settings
from functools import lru_cache
from appPesquisa.utils.resumo import resumir_texto_com_gemini
  # <- usando a função corretamente
import markdown

# Scrapers
from appPesquisa.scrapers.finep import obter_titulos_finep
from appPesquisa.scrapers.cnpq import obter_titulos_cnpq
from appPesquisa.scrapers.fundect import obter_titulos_fundect
from appPesquisa.scrapers.fapergs import obter_titulos_fapergs
from appPesquisa.scrapers.fapesp import obter_titulos_fapesp

# ========================== Scrapers ==========================
# View para verificar a saúde da aplicação
def health_check(request):
    return JsonResponse({"status": "ok"})

def obter_todos_titulos():
    resultados = []
    scrapers = [
        obter_titulos_finep,
        obter_titulos_cnpq
       # obter_titulos_fapergs
    ]

    for scraper in scrapers:
        print(f"Iniciando scraper: {scraper.__name__}")
        try:
            titulos = scraper()
            print(f"OK: {scraper.__name__} → {len(titulos)} resultados")
            resultados.extend(titulos)
        except Exception as e:
            print(f"ERRO: {scraper.__name__}: {e}")

    print("FINALIZADO TODOS OS SCRAPERS")
    return resultados

# ========================== Views ==========================
def tela_index(request):
    return render(request, 'pesquisa/index.html')

def tela_conatenos(request):
    return render(request, 'pesquisa/contatenos.html')

def fomento(request):
    return render(request, 'pesquisa/fomento.html')

def definicao(request):
    return render(request, 'pesquisa/definicao.html')


def conhecaPlataforma(request):
    return render(request, 'base/navbar/conhecaPlataforma.html')

def contatenos(request):
    return render(request, 'base/navbar/contatenos.html')

def pagina_definicao(request):
    return render(request, "pesquisa/definicao.html")

# ========================== Sinonímia ==========================
def obter_sinonimos_api(termo):
    url = f"https://api.datamuse.com/words?rel_syn={termo}&max=3"
    response = requests.get(url)
    sinonimos = []

    if response.status_code == 200:
        resultado = response.json()
        sinonimos = [word['word'] for word in resultado]

    return [termo] + sinonimos

# ========================== Busca AJAX ==========================

from django.http import JsonResponse
from appPesquisa.scrapers.finep import obter_titulos_finep
from appPesquisa.scrapers.cnpq import obter_titulos_cnpq

MAX_RESUMOS_COM_GEMINI = 3  # 🔥 limite duro


def buscar_titulos_ajax(request):
    termo_pesquisa = request.GET.get("termo", "").lower()

    if request.method != "GET":
        return JsonResponse({"erro": "Método inválido"}, status=405)

    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        return JsonResponse({"erro": "Requisição inválida"}, status=400)

    # 1️⃣ Buscar títulos
    titulos = []
    titulos.extend(obter_titulos_finep())
    titulos.extend(obter_titulos_cnpq())
    titulos.extend(obter_titulos_fapesp())

    # 2️⃣ Filtrar por termo + sinônimos
    if termo_pesquisa:
        sinonimos = obter_sinonimos_api(termo_pesquisa)

        titulos = [
            t for t in titulos
            if any(
                termo in t.get("titulo", "").lower()
                or termo in t.get("resumo", "").lower()
                for termo in sinonimos
            )
        ]

    # 3️⃣ Resumir SOMENTE alguns (controlado)
    resumidos = 0
    for titulo in titulos:
        if resumidos >= MAX_RESUMOS_COM_GEMINI:
            break

        resumo = titulo.get("resumo", "")
        if resumo:
            titulo["resumo"] = resumir_texto_com_gemini(resumo)
            resumidos += 1

    return JsonResponse({"titulos": titulos})



def pesquisar_definicao(request):
    termo = request.GET.get("termo", "").strip()
    if not termo:
        return JsonResponse({'erro': 'Termo de pesquisa não informado'}, status=400)

    try:
        definicao = chamar_api_gemini_para_definicao(termo)
        definicao_html = markdown.markdown(definicao) 
        return JsonResponse({'definicao': definicao_html}, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        return JsonResponse({'erro': 'Erro ao obter definição: ' + str(e)}, status=500)

from functools import lru_cache
import time
import requests
from django.conf import settings

@lru_cache(maxsize=200)
def chamar_api_gemini_para_definicao(termo: str) -> str:
    termo = termo.strip().lower()
    if not termo:
        return ""

    prompt = f"Defina o termo '{termo}' de forma clara e objetiva."

    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{url}?key={settings.GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )

        if response.status_code == 429:
            time.sleep(2)
            return "Definição temporariamente indisponível. Tente novamente em instantes."

        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        return f"Erro ao obter definição."
