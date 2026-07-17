
document.getElementById("btn-links").addEventListener("click", async () => {

    if (!validarTermo()) return;

    conteudo.innerHTML = '<div class="accordion" id="lista-chamadas"></div>';

    const lista = document.getElementById("lista-chamadas");

    lista.innerHTML = "🔄 Carregando chamadas...";

    const termoPesquisa = barraPesquisa.value.toLowerCase().trim();

    try {

        const response = await fetch(
            URL_BUSCAR_TITULOS + "?termo=" + encodeURIComponent(termoPesquisa),
            {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        );

        const data = await response.json();

        lista.innerHTML = "";

        if (data.titulos && data.titulos.length > 0) {

            data.titulos.forEach((item, index) => {

                const accordionItem = document.createElement("div");

                accordionItem.className = "accordion-item";

                accordionItem.innerHTML = `
                    <h2 class="accordion-header" id="heading${index}">
                        <button class="accordion-button collapsed"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#collapse${index}">
                            ${item.titulo}
                        </button>
                    </h2>

                    <div id="collapse${index}"
                         class="accordion-body text-start"
                         data-bs-parent="#lista-chamadas">

                        <div class="accordion-body">
                            <p><strong>Resumo:</strong> ${item.resumo || 'Não disponível'}</p>
                            <p><strong>Data de Publicação:</strong> ${item.data_publicacao || 'Não informado'}</p>
                            <p><strong>Prazo de Envio:</strong> ${item.prazo_envio || 'Não informado'}</p>
                            <p><strong>Público Alvo:</strong> ${item.publico_alvo || 'Não informado'}</p>

                            ${item.link
                                ? `<a href="${item.link}" target="_blank">Acesse o edital</a>`
                                : ""
                            }
                        </div>

                    </div>
                `;

                lista.appendChild(accordionItem);

            });

        } else {

            lista.innerHTML =
                "<div class='text-muted'>Nenhuma chamada pública encontrada.</div>";

        }

    } catch (e) {

        lista.innerHTML =
            "<div class='text-danger'>Erro ao carregar os dados.</div>";

    }

});