from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def obter_titulos_cnpq():
    dados = []

    # Configura o Chrome para rodar em modo headless
    options = Options()
    options.add_argument("--headless")  # Modo headless (sem interface gráfica)
    options.add_argument("--disable-gpu")  # Desativa o uso da GPU (reduz o uso de recursos)
    options.add_argument("--no-sandbox")  # Necessário em alguns ambientes de servidor (como Docker)
    options.add_argument("--window-size=1920,1080")  # Definir uma janela "virtual" para o navegador
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")  # Definir um user-agent

    # Inicia o WebDriver com o ChromeDriver automatizado via webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("http://memoria2.cnpq.br/web/guest/chamadas-publicas?p_p_id=resultadosportlet_WAR_resultadoscnpqportlet_INSTANCE_0ZaM&filtro=abertas&ano=2025")

        # Espera até que os elementos necessários carreguem
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.content h4"))
        )

        # Usando BeautifulSoup para processar o HTML da página carregada
        soup = BeautifulSoup(driver.page_source, "html.parser")
        elementos = soup.select("div.content h4")

        for h4 in elementos:
            titulo = h4.get_text(strip=True)

            # Obtendo o link da chamada
            link_tag = h4.find_parent("a")
            link = link_tag["href"] if link_tag and link_tag.has_attr("href") else driver.current_url

            # Obtendo o parágrafo de resumo
            paragrafo = ""
            p_tag = h4.find_next_sibling("p")
            if not p_tag:
                parent_div = h4.find_parent("div", class_="content")
                if parent_div:
                    p_tag = parent_div.find("p")

            if p_tag:
                paragrafo = p_tag.get_text(strip=True)

            # Pegando a data de inscrição
            data_inscricao = ""
            parent_div = h4.find_parent("div", class_="content")
            if parent_div:
                inscricao_div = parent_div.find("div", class_="inscricao")
                if inscricao_div:
                    li_tag = inscricao_div.find("li")
                    if li_tag:
                        data_inscricao = li_tag.get_text(strip=True)

            # Adiciona os dados coletados à lista de resultados
            dados.append({
                "titulo": titulo,
                "link": link,
                "resumo": paragrafo,
                "prazo_envio": data_inscricao
            })

    except Exception as e:
        print("❌ Erro ao buscar dados do CNPq:", e)

    finally:
        driver.quit()  # Garante que o driver seja fechado corretamente

    return dados
