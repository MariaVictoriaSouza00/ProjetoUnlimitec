const conteudo = document.getElementById("conteudo-dinamico");
const barraPesquisa = document.getElementById("barra-pesquisa");

// ---------------------
//  VALIDAÇÃO
// ---------------------
function validarTermo() {
    const termo = barraPesquisa.value.trim();
    if (!termo) {
        alert("Digite um termo de pesquisa antes de continuar.");
        return false;
    }
    return true;
}

// ---------------------
//  BOTÃO — LISTA DE EDITAIS
// ---------------------
document.getElementById("btn-links").addEventListener("click", async () => {
    if (!validarTermo()) return;

    conteudo.innerHTML = '<div class="accordion" id="lista-chamadas"></div>';
    const lista = document.getElementById("lista-chamadas");
    lista.innerHTML = "🔄 Carregando chamadas...";

    const termoPesquisa = barraPesquisa.value.toLowerCase().trim();

    try {
        const response = await fetch(URL_BUSCAR_TITULOS + "?termo=" + encodeURIComponent(termoPesquisa), {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });

        const data = await response.json();
        lista.innerHTML = "";

        if (data.titulos && data.titulos.length > 0) {
            data.titulos.forEach((item, index) => {
                const accordionItem = document.createElement("div");
                accordionItem.className = "accordion-item";

                accordionItem.innerHTML = `
                    <h2 class="accordion-header" id="heading${index}">
                        <button class="accordion-button collapsed" type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#collapse${index}">
                            ${item.titulo}
                        </button>
                    </h2>
                    <div id="collapse${index}" class="accordion-collapse collapse"
                        data-bs-parent="#lista-chamadas">
                        <div class="accordion-body">
                            <p><strong>Resumo:</strong> ${item.resumo || 'Não disponível'}</p>
                            <p><strong>Data de Publicação:</strong> ${item.data_publicacao || 'Não informado'}</p>
                            <p><strong>Prazo de Envio:</strong> ${item.prazo_envio || 'Não informado'}</p>
                            <p><strong>Público Alvo:</strong> ${item.publico_alvo || 'Não informado'}</p>
                            ${item.link ? `<a href="${item.link}" target="_blank" rel="noopener noreferrer">Acesse o edital</a>` : ''}
                        </div>
                    </div>
                `;
                lista.appendChild(accordionItem);
            });
        } else {
            lista.innerHTML = "<div class='text-muted'>Nenhuma chamada pública encontrada.</div>";
        }
    } catch (e) {
        lista.innerHTML = "<div class='text-danger'>Erro ao carregar os dados.</div>";
    }
});

// ---------------------
//  BOTÃO — LIMPAR
// ---------------------
document.getElementById("btn-limpar").addEventListener("click", () => {
    conteudo.innerHTML = `
        <div class="text-center p-4">
            <img src="https://i.ibb.co/Y452ggsR/image.png" 
                alt="Imagem inicial" 
                class="img-fluid" 
                style="max-width: 100%; width: 100%; height: auto;">
        </div>
    `;
    barraPesquisa.value = "";
});

// ---------------------
//  BOTÃO — DEFINIÇÃO
// ---------------------
document.getElementById("btn-pesquisa").addEventListener("click", async () => {
    if (!validarTermo()) return;

    const termo = barraPesquisa.value.trim();

    try {
        const resp = await fetch(URL_DEFINICAO + "?termo=" + encodeURIComponent(termo), {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });

        const data = await resp.json();
        const definicaoHTML = marked.parse(data.definicao);

        conteudo.innerHTML = `
            <div class="card p-4 shadow-sm">
                <h5 class="mb-3">
                    <span class="titulo-accordion">Definição:</span>
                </h5>
                <div class="text-justify">${definicaoHTML}</div>
            </div>
        `;
    } catch (error) {
        conteudo.innerHTML = "<div class='text-danger'>Erro ao buscar definição.</div>";
    }
});

// ---------------------
//  FILTRO AO DIGITAR
// ---------------------
barraPesquisa.addEventListener("input", () => {
    const termo = barraPesquisa.value.toLowerCase();
    const itens = document.querySelectorAll(".accordion-item");

    itens.forEach(item => {
        const texto = item.innerText.toLowerCase();
        item.style.display = texto.includes(termo) ? "" : "none";
    });
});
