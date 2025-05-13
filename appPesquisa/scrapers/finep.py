from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appPesquisa.scrapers.utils import configurar_driver

def obter_titulos_finep():
    dados = []
    
    # Configura o driver (agora com o webdriver-manager)
    driver = configurar_driver()

    try:
        # Acessa a página principal das chamadas públicas da FINEP
        driver.get("http://www.finep.gov.br/chamadas-publicas/chamadaspublicas?pchave=&situacao=aberta&d1=01-01-2025")

        # Espera até que os títulos estejam carregados
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item h3 a"))
        )

        # Obtém o HTML da página usando BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        elementos = soup.select("div.item h3 a")

        for el in elementos:
            titulo = el.get_text(strip=True)
            link = el["href"].strip()

            # Garantir que o link seja completo
            if not link.startswith("http"):
                link = "http://www.finep.gov.br" + link

            # Acessa a página individual da chamada
            try:
                driver.get(link)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.item_fields"))
                )

                # Obtém o HTML da página individual da chamada
                soup_chamada = BeautifulSoup(driver.page_source, "html.parser")
                campos = soup_chamada.select_one("div.item_fields")

                descricao = ""
                prazo_envio = ""
                publico_alvo = ""
                data_publicacao = ""

                # Obtém a descrição da chamada
                desc = campos.select_one("div.group.desc .text")
                if desc:
                    descricao = desc.get_text(separator="\n", strip=True)

                # Itera sobre os campos adicionais (prazo, público-alvo, etc)
                for grupo in campos.select("div.group"):
                    titulo_campo = grupo.select_one("div.tit")
                    valor_campo = grupo.select_one("div.text")

                    if titulo_campo and valor_campo:
                        chave = titulo_campo.get_text(strip=True).lower()
                        valor = valor_campo.get_text(" ", strip=True)

                        # Identifica os campos pela chave e extrai os valores
                        if "prazo para envio" in chave:
                            prazo_envio = valor
                        elif "público-alvo" in chave:
                            publico_alvo = valor
                        elif "data de publicação" in chave:
                            data_publicacao = valor

                # Adiciona os dados extraídos à lista
                dados.append({
                    "titulo": titulo,
                    "link": link,
                    "resumo": descricao,
                    "prazo_envio": prazo_envio,
                    "publico_alvo": publico_alvo,
                    "data_publicacao": data_publicacao
                })

            except Exception as e:
                print(f"Erro ao acessar detalhes da chamada: {link} - {e}")

    except Exception as e:
        print("Erro geral no FINEP:", e)
    finally:
        driver.quit()  # Garante que o driver seja fechado corretamente

    return dados
