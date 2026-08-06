from django.http import JsonResponse

from appPesquisa.services.pesquisa_service import pesquisar_editais


def buscar_titulos_ajax(request):

    termo = request.GET.get("termo", "").lower()

    if request.method != "GET":
        return JsonResponse({"erro": "Método inválido"}, status=405)

    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        return JsonResponse({"erro": "Requisição inválida"}, status=400)

    titulos = pesquisar_editais(termo)

    return JsonResponse({"titulos": titulos})