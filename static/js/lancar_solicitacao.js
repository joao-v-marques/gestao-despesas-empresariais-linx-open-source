// Puxa a empresa e revenda do HTML
const empresaInput = document.querySelector('#empresa_id');
const revendaInput = document.querySelector('#revenda_id');

// Função que atualiza as opções da revenda
function atualizarOpcoesRevenda() {
    revendaInput.innerHTML = '';

    if (empresaInput.value == '1') {
        for (let i = 1; i <= 11; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `${i}`;
            revendaInput.appendChild(option);
        }
    } else if (empresaInput.value == '4') {
        for (let i = 1; i <= 2; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = `${i}`;
            revendaInput.appendChild(option);
        }
    }
}

empresaInput.addEventListener('change', atualizarOpcoesRevenda)

atualizarOpcoesRevenda()

document.addEventListener('DOMContentLoaded', function () {
    const valorInput = document.querySelector('.input-valor');
    const formulario = document.querySelector('.formulario');

    valorInput.addEventListener('input', function (e) {
        let valor = e.target.value;

        // Remove tudo que não for número
        valor = valor.replace(/\D/g, '');

        // Formata como moeda (R$)
        valor = (valor / 100).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });

        // Atualiza o valor do campo
        e.target.value = valor;
    });

    valorInput.addEventListener('focus', function (e) {
        // Remove o "R$" ao focar no campo para facilitar a edição
        e.target.value = e.target.value.replace(/[^\d]/g, '');
    });

    valorInput.addEventListener('blur', function (e) {
        // Reaplica a formatação ao sair do campo
        let valor = e.target.value;

        if (valor) {
            valor = (parseFloat(valor.replace(/[^\d]/g, '')) / 100).toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            });
            e.target.value = valor;
        }
    });

    // Antes de enviar o formulário, converte o valor para float
    formulario.addEventListener('submit', function (e) {
        const valorSemFormatacao = valorInput.value.replace(/[^\d]/g, ''); // Remove R$, pontos e vírgulas
        const valorFloat = parseFloat(valorSemFormatacao) / 100; // Converte para float
        valorInput.value = valorFloat; // Atualiza o valor do campo para enviar como float
    });
});

document.getElementById('codigo_fornecedor_id').addEventListener('input', function () {
    const codigo = this.value;

    if (codigo !== '') {
        fetch(`/lancar-solicitacao/fornecedor/${codigo}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('descricao_fornecedor_id').value = data.nome || 'Fornecedor não encontrado';
            })
            .catch(error => {
                console.error('Erro ao buscar fornecedor:', error);
                document.getElementById('descricao_fornecedor_id').value = 'Erro na busca';
            });
    } else {
        document.getElementById('descricao_fornecedor_id').value = '';
    }
});

document.getElementById('empresa_id').addEventListener('change', buscarOrigens);
document.getElementById('revenda_id').addEventListener('change', buscarOrigens);

function buscarOrigens() {
    var empresa = document.getElementById('empresa_id').value;
    var revenda = document.getElementById('revenda_id').value;
    empresa = Number(empresa)
    revenda = Number(revenda)
    fetch(`/lancar-solicitacao/buscar-origens?empresa=${empresa}&revenda=${revenda}`)
        .then(response => response.json())
        .then(data => {
            const origemSelect = document.getElementById('origem_id');
            origemSelect.innerHTML = '';
            data.forEach(origem => {
                const option = document.createElement('option');
                option.value = origem.origem;
                option.text = origem.des_origem;
                origemSelect.appendChild(option);
            });
        });
}

document.addEventListener('DOMContentLoaded', function () {
    buscarOrigens();
});
