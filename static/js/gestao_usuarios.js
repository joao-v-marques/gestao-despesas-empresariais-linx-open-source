const empresa_inserida = document.querySelector('#empresa_id');
const revenda_inserida = document.querySelector('#revenda_id');

function  atualizarOpcoesRevenda() {
    revenda_inserida.innerHTML = '';

    if (empresa_inserida.value == '1') {
        for (let i = 1; i <= 11; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            revenda_inserida.appendChild(option);
        }
    } else if (empresa_inserida.value == '4') {
        for (let i = 1; i <= 2; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            revenda_inserida.appendChild(option);
        }
    }
}

empresa_inserida.addEventListener('change', atualizarOpcoesRevenda);

atualizarOpcoesRevenda();

const cpf_form = document.querySelector('#cpf_id');

cpf_form.addEventListener('input', function () {
    let cpf = cpf_form.value;

    cpf = cpf.replace(/\D/g, '');

    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

    cpf_form.value = cpf;
})