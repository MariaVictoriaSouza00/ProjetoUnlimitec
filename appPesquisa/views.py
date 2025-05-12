from django.shortcuts import render
from django.http import JsonResponse
import threading
import requests

from appPesquisa.scrapers.finep import obter_titulos_finep
from appPesquisa.scrapers.cnpq import obter_titulos_cnpq
from appPesquisa.scrapers.fundect import obter_titulos_fundect

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

# View principal que apenas renderiza a página
def tela_index(request):
    return render(request, 'pesquisa/index.html')

def obter_sinonimos_api(termo):
    url = f"https://api.datamuse.com/words?rel_syn={termo}&max=3"
    response = requests.get(url)
    sinonimos = []

    if response.status_code == 200:
        resultado = response.json()
        sinonimos = [word['word'] for word in resultado]

    return [termo] + sinonimos

def buscar_titulos_ajax(request):
    termo_pesquisa = request.GET.get("termo", "").lower()
    if request.method == "GET" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        titulos = obter_todos_titulos()

        # Obtemos os sinônimos da palavra digitada
        sinonimos = obter_sinonimos_api(termo_pesquisa)

        # Filtrar com base no termo e seus sinônimos
        if termo_pesquisa:
            titulos = [titulo for titulo in titulos if any(
                termo in titulo['titulo'].lower() for termo in sinonimos)]

        return JsonResponse({'titulos': titulos})

    return JsonResponse({'erro': 'Requisição inválida'}, status=400)

def fomento(request):
    return render(request, 'pesquisa/fomento.html')  
    
def definicao(request):
    return render(request, 'pesquisa/definicao.html') 