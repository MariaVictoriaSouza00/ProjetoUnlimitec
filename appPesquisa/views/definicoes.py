from django.http import JsonResponse

import markdown

from appPesquisa.services.gemini import chamar_api_gemini_para_definicao


def pesquisar_definicao(request):

    termo = request.GET.get("termo", "").strip()

    if not termo:
        return JsonResponse(
            {"erro": "Termo de pesquisa não informado"},
            status=400
        )

    try:

        definicao = chamar_api_gemini_para_definicao(termo)

        definicao_html = markdown.markdown(definicao)

        return JsonResponse(
            {"definicao": definicao_html},
            json_dumps_params={"ensure_ascii": False},
        )

    except Exception as e:

        return JsonResponse(
            {"erro": str(e)},
            status=500,
        )