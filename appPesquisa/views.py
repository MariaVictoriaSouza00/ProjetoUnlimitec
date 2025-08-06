from django.shortcuts import render
from django.http import JsonResponse
import threading
import requests
from django.conf import settings
from functools import lru_cache
from appPesquisa.utils.resumo import resumir_texto_com_gemini  # <- usando a função corretamente
import markdown

# Scrapers
from appPesquisa.scrapers.finep import obter_titulos_finep
from appPesquisa.scrapers.cnpq import obter_titulos_cnpq
from appPesquisa.scrapers.fundect import obter_titulos_fundect

# ========================== Scrapers ==========================
# View para verificar a saúde da aplicação
def health_check(request):
    return JsonResponse({"status": "ok"})

def obter_todos_titulos():
    resultados = []

    def run_scraper(scraper_func):
        try:
            titulos = scraper_func()
            resultados.extend(titulos)
        except Exception as e:
            print(f"Erro no scraper {scraper_func.__name__}: {e}")

    scrapers = [obter_titulos_finep, obter_titulos_cnpq, obter_titulos_fundect]
    threads = []

    for scraper in scrapers:
        thread = threading.Thread(target=run_scraper, args=(scraper,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return resultados

# ========================== Views ==========================
def tela_index(request):
    return render(request, 'pesquisa/index.html')

def fomento(request):
    return render(request, 'pesquisa/fomento.html')

def definicao(request):
    return render(request, 'pesquisa/definicao.html')

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
def buscar_titulos_ajax(request):
    termo_pesquisa = request.GET.get("termo", "").lower()

    if request.method == "GET" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        titulos = obter_todos_titulos()
        sinonimos = obter_sinonimos_api(termo_pesquisa)

        if termo_pesquisa:
            titulos = [
                titulo for titulo in titulos
                if any(
                    termo in titulo.get('titulo', '').lower() or termo in titulo.get('resumo', '').lower()
                    for termo in sinonimos
                )
            ]


        # Aplica a função Gemini para resumir
        for titulo in titulos:
            resumo_original = titulo.get("resumo", "")
            if resumo_original:
                titulo["resumo"] = resumir_texto_com_gemini(resumo_original)

        return JsonResponse({'titulos': titulos})

    return JsonResponse({'erro': 'Requisição inválida'}, status=400)


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


import json
import requests
from django.conf import settings

def chamar_api_gemini_para_definicao(termo):
    if not termo.strip():
        return ""

    prompt = f"Defina  o termo: '{termo}'"

    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    api_key = settings.GEMINI_API_KEY
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(f"{url}?key={api_key}", headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        resposta = response.json()

        partes = resposta.get("candidates", [])[0].get("content", {}).get("parts", [])
        if partes and "text" in partes[0]:
            return partes[0]["text"].strip()

        return "Não foi possível obter a definição."

    except requests.exceptions.HTTPError as http_err:
        return f"Erro HTTP: {http_err}"
    except Exception as err:
        return f"Erro ao obter definição: {str(err)}"