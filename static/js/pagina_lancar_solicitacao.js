const empresaInput = document.querySelector('#empresa_id');
const revendaInput = document.querySelector('#revenda_id');

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