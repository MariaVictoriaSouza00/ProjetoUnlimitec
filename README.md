# 🧠 NomeDoSistema :Desenvolvimento de uma plataforma inteligente para centralizar e facilitar o Acesso a Informações Científicas

Este projeto é uma plataforma web desenvolvida em Django que permite a consulta de termos técnicos por meio de inteligência artificial, extração de informações de documentos públicos e apresentação de dados de forma integrada.

## 🔍 Funcionalidades

- Consulta de termos técnicos com definição contextual gerada por IA (Google Gemini).
- Extração automatizada de conteúdos técnicos de páginas web (web scraping).
- Exibição de resumos e dados organizados para auxiliar pesquisadores, estudantes e interessados.
- Interface responsiva desenvolvida com HTML, CSS e Bootstrap.
- Deploy público para demonstração e testes.

## 🛠️ Tecnologias Utilizadas

### Back-end
- **Django 5.1.7**
- **Django REST Framework**
- **Gunicorn**

### Inteligência Artificial
- **Google Gemini API** (via `google-generativeai`)

### Web Scraping
- **BeautifulSoup 4**
- **Playwright / Selenium** (suporte preparado para scraping de páginas dinâmicas)
- **Requests / HTTPX**
- **Tqdm**

### Front-end
- **HTML5 / CSS3 / JavaScript**
- **Bootstrap 5**
- **WhiteNoise** (servidor de arquivos estáticos)

### Banco de Dados
- **PostgreSQL** (estrutura já preparada, mesmo que o projeto atual não armazene dados)

### Infraestrutura e Deploy
- **GitHub** (controle de versão)
- **Render** (hospedagem gratuita com deploy automático)

## 🚀 Deploy

A aplicação está hospedada gratuitamente na plataforma Render e pode ser acessada através do link abaixo:

🔗 [Acessar sistema online]([https://nome-do-projeto.onrender.com](https://projetounlimitec-1.onrender.com/ )

> *Nota: o deploy foi realizado com integração contínua via GitHub. Alterações no repositório são automaticamente refletidas na versão em produção.*

## 🧪 Como Executar Localmente

### Pré-requisitos

- Python 3.10+
- Git
- PostgreSQL ou SQLite (padrão)
- Ambiente virtual

### Passos para instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/nome-do-projeto.git
cd nome-do-projeto

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Inicie o servidor de desenvolvimento
python manage.py runserver
