import time
import requests
from functools import lru_cache

from django.conf import settings

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1/models/"
    "gemini-2.0-flash:generateContent"
)


@lru_cache(maxsize=200)
def chamar_api_gemini_para_definicao(termo: str) -> str:
    termo = termo.strip().lower()

    if not termo:
        return ""

    prompt = f"Defina o termo '{termo}' de forma clara e objetiva."

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )

        if response.status_code == 429:
            time.sleep(2)
            return "Definição temporariamente indisponível."

        response.raise_for_status()

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception:
        return "Erro ao obter definição."


@lru_cache(maxsize=500)
def resumir_texto_com_gemini(texto: str) -> str:
    if not texto.strip():
        return ""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Resuma o texto abaixo em até 3 linhas:\n\n"
                            f"{texto}"
                        )
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )

        if response.status_code == 429:
            time.sleep(2)
            return "Resumo temporariamente indisponível."

        response.raise_for_status()

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        return f"Erro ao resumir: {str(e)}"