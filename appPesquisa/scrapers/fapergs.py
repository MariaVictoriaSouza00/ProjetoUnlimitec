from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def obter_titulos_fapergs():
    dados = []
    url = "https://fapergs.rs.gov.br/abertos"

    # Configuração do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Espera para carregar a lista

    # Seleciona os artigos da lista
    elementos = driver.find_elements(By.CSS_SELECTOR, "div.matriz-ui-pagedlist-body article.conteudo-lista__item")

    for el in elementos:
        try:
            titulo_tag = el.find_element(By.CSS_SELECTOR, "h2.conteudo-lista__item__titulo a")
            titulo = titulo_tag.text.strip()
            link = titulo_tag.get_attribute("href")

            # Abre o link do edital
            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            try:
                texto_tag = driver.find_element(By.CSS_SELECTOR, "div.artigo__texto")
                texto = texto_tag.text.strip()
            except:
                texto = ""

            # Fecha a aba do edital e volta para a lista
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            dados.append({
                "titulo": titulo,
                "link": link,
                "resumo": texto
            })

        except:
            continue

    driver.quit()
    return dados
