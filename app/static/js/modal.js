var modal = document.getElementsByClassName('modal-exclusao')[0];
var cancelarModal = document.getElementById('btn-dismiss');
var botaoExcluir = document.getElementById('botao-deletar');

botaoExcluir.addEventListener("click", () => {
    modal.style.display = "block";
});

cancelarModal.addEventListener("click", () => {
    modal.style.display = "none";
});

window.addEventListener("click", (event) => {
    if (event.target == modal) {
        modal.style.display = "none";
    }
})
