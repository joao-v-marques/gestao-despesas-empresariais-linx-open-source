function setFiltro(valor) {
    document.getElementById('filtroInput').value = valor;
    document.getElementById('filtroForm').submit();
}

document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('show.bs.modal', function () {
        const id = this.id.replace('infoModal', '');
        const codigoInput = document.getElementById(`codigo_fornecedor_id_${id}`);
        const descricaoInput = document.getElementById(`descricao_fornecedor_id_${id}`);
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
});