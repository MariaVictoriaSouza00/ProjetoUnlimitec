// BOTÃO DEFINIÇÃO
document.getElementById("btn-pesquisa").addEventListener("click", async () => {
    if (!validarTermo()) return;

    const termo = barraPesquisa.value.trim();

    conteudo.innerHTML = "🔄 Carregando ...";

    try {
        const resp = await fetch(
            URL_DEFINICAO + "?termo=" + encodeURIComponent(termo),
            { headers: { "X-Requested-With": "XMLHttpRequest" } }
        );

        const data = await resp.json();
        const definicaoHTML = marked.parse(data.definicao);

        conteudo.innerHTML = `
            <div class="card p-4 shadow-sm">
                <h5 class="mb-3 text-start">
                    <span class="titulo-accordion">Definição:</span>
                </h5>
                <div class="text-start">
                    ${definicaoHTML}
                </div>
            </div>
        `;

    } catch (error) {
        conteudo.innerHTML =
            "<div class='text-danger'>Erro ao buscar definição.</div>";
    }
});
