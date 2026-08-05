

// BOTÃO LIMPAR
document.getElementById("btn-limpar").addEventListener("click", () => {
    conteudo.innerHTML = `
        <div class="text-center p-4">
            <img src="https://i.ibb.co/gMBpcgDV/image.png"
                class="img-fluid"
                style="max-width:100%;width:100%;height:auto;">
        </div>
    `;
    barraPesquisa.value = "";
});


// FILTRO
barraPesquisa.addEventListener("input", () => {
    const termo = barraPesquisa.value.toLowerCase();
    const itens = document.querySelectorAll(".accordion-item");

    itens.forEach(item => {
        item.style.display = item.innerText.toLowerCase().includes(termo)
            ? ""
            : "none";
    });
});