from django.shortcuts import render


def tela_index(request):
    return render(request, "pesquisa/index.html")


def tela_conatenos(request):
    return render(request, "pesquisa/contatenos.html")


def fomento(request):
    return render(request, "pesquisa/fomento.html")


def definicao(request):
    return render(request, "pesquisa/definicao.html")


def conhecaPlataforma(request):
    return render(request, "base/navbar/conhecaPlataforma.html")


def contatenos(request):
    return render(request, "base/navbar/contatenos.html")


def pagina_definicao(request):
    return render(request, "pesquisa/definicao.html")