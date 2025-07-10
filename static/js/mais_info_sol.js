document.addEventListener('DOMContentLoaded', function() {
    const btnEditar = document.getElementById('btn-editar');
    const btnCancelar = document.getElementById('btn-cancelar');
    const botoesVisualizacao = document.querySelector('.botoes');
    const form = document.querySelector('.formulario');
    const botoesEdicao = document.getElementById('botoes_edicao_id');

    // Campos editáveis
    const camposEditaveis = [
        'descricao',
        'valor'
    ];
    const inputs = form.querySelectorAll('input[type="text"], textarea');
    const selects = [
        document.getElementById('departamento_id'),
    ];

    let valoresOriginais = {};

    if (botoesEdicao) {
        botoesEdicao.style.display = 'none';
    }
    
    if (btnEditar) {
        btnEditar.addEventListener('click', function() {
            // Salva valores originais
            inputs.forEach(input => {
                valoresOriginais[input.name] = input.value;
                if (camposEditaveis.includes(input.name)) {
                    input.removeAttribute('readonly');
                }
            });
            selects.forEach(select => {
                select.disabled = false;
                valoresOriginais[select.name] = select.value;
            });
            if (botoesVisualizacao) botoesVisualizacao.style.display = 'none';
            if (botoesEdicao) botoesEdicao.style.display = 'flex';
        });
    }

    if (btnCancelar) {
        btnCancelar.addEventListener('click', function(event) {
            event.preventDefault();
            // Restaura valores originais e bloqueia campos novamente
            inputs.forEach(input => {
                input.value = valoresOriginais[input.name];
                input.setAttribute('readonly', true);
            });
            selects.forEach(select => {
                select.value = valoresOriginais[select.name];
                select.disabled = true;
            });
            if (botoesVisualizacao) botoesVisualizacao.style.display = 'block';
            if (botoesEdicao) botoesEdicao.style.display = 'none';
        });
    }

    if (form) {
        form.addEventListener('submit', function() {
            // Remove o disabled dos selects antes do submit
            selects.forEach(select => select.disabled = false);
            // O submit padrão do HTML será executado normalmente
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const solicitacaoId = document.getElementById('codigo_apollo_solicitacao_id').value;
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