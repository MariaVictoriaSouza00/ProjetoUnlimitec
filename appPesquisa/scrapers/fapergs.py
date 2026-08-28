# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# import time


# URL = "https://fapergs.rs.gov.br/abertos"
# URL_BASE = "https://fapergs.rs.gov.br"


# def obter_titulos_fapergs():

#     dados = []

#     # ==========================================================
#     # CONFIGURAÇÃO DO CHROME
#     # ==========================================================

#     options = Options()

#     options.add_argument("--headless=new")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     options.add_argument(
#         "--window-size=1920,1080"
#     )

#     options.add_argument(
#         "--disable-blink-features=AutomationControlled"
#     )

#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/151.0.0.0 Safari/537.36"
#     )

#     driver = webdriver.Chrome(
#         options=options
#     )

#     try:

#         print("Acessando FAPERGS...")

#         driver.get(URL)

#         # ======================================================
#         # ESPERA A PÁGINA CARREGAR
#         # ======================================================

#         wait = WebDriverWait(
#             driver,
#             30
#         )

#         # Espera o container da lista
#         wait.until(
#             EC.presence_of_element_located(
#                 (
#                     By.CSS_SELECTOR,
#                     "div.conteudo-lista__body"
#                 )
#             )
#         )

#         print("Container encontrado.")

#         # Dá alguns segundos para a paginação/conteúdo
#         # terminar de ser carregado
#         time.sleep(5)

#         # ======================================================
#         # PEGA O HTML JÁ PROCESSADO PELO NAVEGADOR
#         # ======================================================

#         html = driver.page_source

#         # Salva para debug
#         with open(
#             "fapergs_debug.html",
#             "w",
#             encoding="utf-8"
#         ) as arquivo:

#             arquivo.write(html)

#         print(
#             "HTML salvo em fapergs_debug.html"
#         )

#         # ======================================================
#         # BEAUTIFULSOUP
#         # ======================================================

#         soup = BeautifulSoup(
#             html,
#             "html.parser"
#         )

#         # ======================================================
#         # LOCALIZA OS ARTIGOS
#         # ======================================================

#         artigos = soup.select(
#             "div.conteudo-lista__body "
#             "article.conteudo-lista__item"
#         )

#         print(
#             "Artigos encontrados:",
#             len(artigos)
#         )

#         # ======================================================
#         # PERCORRE OS EDITAIS
#         # ======================================================

#         for artigo in artigos:

#             # --------------------------------------------------
#             # TÍTULO
#             # --------------------------------------------------

#             titulo_tag = artigo.select_one(
#                 "h2 a"
#             )

#             if not titulo_tag:
#                 continue

#             titulo = titulo_tag.get_text(
#                 " ",
#                 strip=True
#             )

#             # --------------------------------------------------
#             # LINK
#             # --------------------------------------------------

#             href = titulo_tag.get(
#                 "href"
#             )

#             if not href:
#                 continue

#             link = urljoin(
#                 URL_BASE,
#                 href
#             )

#             # --------------------------------------------------
#             # STATUS
#             # --------------------------------------------------

#             status_tag = artigo.select_one(
#                 ".lista-categoria a"
#             )

#             status = ""

#             if status_tag:

#                 status = status_tag.get_text(
#                     " ",
#                     strip=True
#                 )

#             # --------------------------------------------------
#             # DESCRIÇÃO
#             # --------------------------------------------------

#             descricao = ""

#             descricao_tag = artigo.select_one(
#                 ".conteudo-lista__item__descricao"
#             )

#             if descricao_tag:

#                 descricao = descricao_tag.get_text(
#                     " ",
#                     strip=True
#                 )

#             # --------------------------------------------------
#             # ADICIONA
#             # --------------------------------------------------

#             dados.append({

#                 "titulo": titulo,

#                 "link": link,

#                 "status": status,

#                 "descricao": descricao

#             })

#         return dados

#     except Exception as e:

#         print(
#             "Erro ao obter editais da FAPERGS:"
#         )

#         print(e)

#         return []

#     finally:

#         driver.quit()

