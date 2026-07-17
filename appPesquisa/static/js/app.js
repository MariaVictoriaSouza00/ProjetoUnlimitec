const conteudo = document.getElementById("conteudo-dinamico");
const barraPesquisa = document.getElementById("barra-pesquisa");

function validarTermo() {
    const termo = barraPesquisa.value.trim();

    if (!termo) {
        alert("Digite um termo de pesquisa antes de continuar.");
        return false;
    }

    return true;
}