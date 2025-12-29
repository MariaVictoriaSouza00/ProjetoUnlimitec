import time
import requests
from functools import lru_cache
from django.conf import settings

GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"


@lru_cache(maxsize=500)
def resumir_texto_com_gemini(texto: str) -> str:
    if not texto.strip():
        return ""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Resuma o texto abaixo em até 3 linhas:\n\n{texto}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )

        if response.status_code == 429:
            time.sleep(2)
            return "Resumo temporariamente indisponível."

        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except Exception as e:
        return f"Erro ao resumir: {str(e)}"
