
import time
from functools import lru_cache

import requests
from django.conf import settings


# ============================================================
# CONFIGURAÇÃO DO GEMINI
# ============================================================

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-3.8-flash:generateContent"
)

TIMEOUT_CONEXAO = 10
TIMEOUT_RESPOSTA = 60
MAX_TENTATIVAS = 2


# ============================================================
# FUNÇÃO CENTRAL PARA CHAMAR A API DO GEMINI
# ============================================================

def chamar_gemini(prompt: str) -> str:
    """
    Envia um prompt para a API do Gemini
    e retorna o texto da resposta.
    """

    # Verifica a chave da API
    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key or not api_key.strip():
        print("ERRO: GEMINI_API_KEY não configurada.")
        return "Chave da API do Gemini não configurada."

    # Verifica o prompt
    if not prompt or not prompt.strip():
        return ""

    # Monta a requisição
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt.strip()
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key.strip(),
    }

    # Envia a requisição, com uma nova tentativa em caso de 429
    for tentativa in range(MAX_TENTATIVAS):

        try:
            inicio = time.monotonic()

            response = requests.post(
                GEMINI_URL,
                json=payload,
                headers=headers,
                timeout=(TIMEOUT_CONEXAO, TIMEOUT_RESPOSTA),
            )

            duracao = time.monotonic() - inicio

            print("=" * 50)
            print("GEMINI STATUS:", response.status_code)
            print(f"TEMPO DE RESPOSTA: {duracao:.2f} segundos")
            print("=" * 50)

            # Limite de requisições
            if response.status_code == 429:
                if tentativa < MAX_TENTATIVAS - 1:
                    print("Limite de requisições. Tentando novamente em 3 segundos...")
                    time.sleep(3)
                    continue

                print("ERRO 429:", response.text[:1000])
                return "Limite de requisições do Gemini atingido."

            # Erro de autenticação
            if response.status_code == 401:
                print("ERRO 401 - Autenticação Gemini:", response.text[:1000])
                return "Erro de autenticação com a API do Gemini."

            # Erro de permissão
            if response.status_code == 403:
                print("ERRO 403 - Permissão Gemini:", response.text[:1000])
                return "A API do Gemini recusou a permissão para esta requisição."

            # Outros erros HTTP
            if response.status_code != 200:
                print("ERRO HTTP GEMINI:", response.status_code)
                print("DETALHES:", response.text[:1000])
                return "Não foi possível obter resposta do Gemini."

            # Converte a resposta para JSON
            data = response.json()

            # Verifica se a API retornou candidatos
            candidates = data.get("candidates", [])

            if not candidates:
                print("ERRO: Gemini não retornou candidatos.")
                print("RESPOSTA:", str(data)[:1000])

                feedback = data.get("promptFeedback", {})
                if feedback:
                    print("PROMPT FEEDBACK:", feedback)

                return "O Gemini não retornou uma resposta válida."

            # Obtém o conteúdo da resposta
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])

            if not parts:
                print("ERRO: Resposta do Gemini sem conteúdo.")
                print("RESPOSTA:", str(data)[:1000])
                return "O Gemini não retornou um texto válido."

            # Junta as partes textuais, se houver mais de uma
            textos = [
                parte["text"]
                for parte in parts
                if isinstance(parte, dict) and parte.get("text")
            ]

            texto = "\n".join(textos).strip()

            if not texto:
                print("ERRO: Gemini retornou texto vazio.")
                return "O Gemini retornou uma resposta vazia."

            return texto

        except requests.exceptions.Timeout as e:
            print("=" * 50)
            print("ERRO: TIMEOUT GEMINI")
            print("TIPO:", type(e).__name__)
            print("DETALHES:", repr(e))
            print("URL UTILIZADA:", GEMINI_URL)
            print("=" * 50)

            return (
                "O Gemini demorou muito para responder. "
                "Tente novamente em alguns instantes."
            )

        except requests.exceptions.ConnectionError as e:
            print("=" * 50)
            print("ERRO DE CONEXÃO COM GEMINI")
            print("DETALHES:", repr(e))
            print("=" * 50)

            return "Não foi possível conectar ao Gemini. Verifique sua conexão."

        except requests.exceptions.RequestException as e:
            print("=" * 50)
            print("ERRO NA REQUISIÇÃO GEMINI")
            print("TIPO:", type(e).__name__)
            print("DETALHES:", repr(e))
            print("=" * 50)

            return "Erro na comunicação com o Gemini."

        except ValueError as e:
            print("=" * 50)
            print("ERRO AO INTERPRETAR RESPOSTA GEMINI")
            print("DETALHES:", repr(e))
            print("=" * 50)

            return "O Gemini retornou uma resposta inválida."

        except Exception as e:
            print("=" * 50)
            print("ERRO INESPERADO GEMINI")
            print("TIPO:", type(e).__name__)
            print("DETALHES:", repr(e))
            print("=" * 50)

            return "Erro inesperado ao obter resposta do Gemini."

    return "Não foi possível obter resposta do Gemini."


# ============================================================
# DEFINIÇÃO DE TERMOS
# ============================================================

@lru_cache(maxsize=200)
def chamar_api_gemini_para_definicao(termo: str) -> str:
    """
    Gera uma definição clara e objetiva para um termo.
    """

    if not termo:
        return ""

    termo = termo.strip().lower()

    if not termo:
        return ""

    prompt = (
        f"Defina o termo '{termo}' "
        "de forma clara, objetiva e fácil de entender. "
        "Responda em português do Brasil. "
        "Evite informações desnecessárias. "
        "Dê preferência a uma explicação curta e direta."
    )

    return chamar_gemini(prompt)


# ============================================================
# RESUMO DE TEXTO
# ============================================================

@lru_cache(maxsize=500)
def resumir_texto_com_gemini(texto: str) -> str:
    """
    Resume um texto utilizando o Gemini.
    """

    if not texto:
        return ""

    texto = texto.strip()

    if not texto:
        return ""

    prompt = (
        "Resuma o texto abaixo em até 3 linhas. "
        "Mantenha apenas as informações mais importantes. "
        "Escreva em português do Brasil. "
        "Não invente informações que não estejam no texto. "
        "Preserve nomes de instituições, programas, "
        "editais, datas e informações relevantes.\n\n"
        "TEXTO:\n"
        f"{texto}"
    )

    return chamar_gemini(prompt)
