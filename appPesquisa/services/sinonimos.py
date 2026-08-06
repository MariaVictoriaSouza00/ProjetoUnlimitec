import requests


def obter_sinonimos_api(termo):

    url = f"https://api.datamuse.com/words?rel_syn={termo}&max=3"

    response = requests.get(url)

    sinonimos = []

    if response.status_code == 200:

        resultado = response.json()

        sinonimos = [
            palavra["word"]
            for palavra in resultado
        ]

    return [termo] + sinonimos