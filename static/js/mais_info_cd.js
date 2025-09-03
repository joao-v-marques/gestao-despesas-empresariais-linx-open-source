document.addEventListener('DOMContentLoaded', function () {
    const solicitacaoId = document.getElementById('id_solicitacao_id').value;
    const codigoInput = document.getElementById(`codigo_fornecedor_id_${solicitacaoId}`);
    const descricaoInput = document.getElementById(`descricao_fornecedor_id_${solicitacaoId}`);
    const codigo = codigoInput.value;
    if (codigo) {
        fetch(`/lancar-solicitacao/fornecedor/${codigo}`)
            .then(response => response.json())
            .then(data => {
                descricaoInput.value = data.nome || 'Fornecedor não encontrado';
            })
            .catch(error => {
                descricaoInput.value = 'Erro na busca';
            });
    } else {
        descricaoInput.value = '';
    }
});

const formAprovar = document.getElementById("formAprovar");
const btnAprovar = document.getElementById("btnAprovar");

formAprovar.addEventListener("submit", function () {
    if (btnAprovar.disabled) return;

    btnAprovar.disabled = true;
    btnAprovar.value = "Aprovando..."
})

const formReprovar = document.getElementById("formReprovar");
const btnReprovar = document.getElementById("btnReprovar");

formReprovar.addEventListener("submit", function () {
    if (btnReprovar.disabled) return;

    btnReprovar.disabled = true;
    btnReprovar.value = "Reprovando..."
})