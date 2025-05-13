import json
import requests
from django.conf import settings

def resumir_texto_com_gemini(texto):
    if not texto.strip():
        return ""

    # Instrução clara no prompt
    prompt = (
        "Resuma o seguinte texto em no máximo 5 linhas, de forma objetiva e clara:\n\n"
        + texto
    )

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    headers = {
        'Content-Type': 'application/json',
    }

    api_key = settings.GEMINI_API_KEY
    url_with_key = f"{url}?key={api_key}"

    try:
        response = requests.post(url_with_key, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_json = response.json()
            if 'candidates' in response_json:
                parts = response_json['candidates'][0]['content']['parts']
                if parts and 'text' in parts[0]:
                    return parts[0]['text'].strip()
        return ""
    except Exception:
        return ""
