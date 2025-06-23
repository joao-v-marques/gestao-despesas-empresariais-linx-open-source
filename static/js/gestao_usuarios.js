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

// Preenchimento dinâmico de revendas nos modais de edição
document.addEventListener('DOMContentLoaded', function() {
    // Para cada modal de edição
    document.querySelectorAll('select[id^="empresa_id_edit_"]').forEach(function(empresaSelect) {
        const userId = empresaSelect.id.replace('empresa_id_edit_', '');
        const revendaSelect = document.getElementById('revenda_id_edit_' + userId);
        const revendaAtual = empresaSelect.getAttribute('data-revenda');

        function atualizarOpcoesRevendaEdit() {
            revendaSelect.innerHTML = '';
            let max = empresaSelect.value == '1' ? 11 : 2;
            for (let i = 1; i <= max; i++) {
                const option = document.createElement('option');
                option.value = i;
                option.textContent = i;
                if (String(i) === String(revendaAtual)) option.selected = true;
                revendaSelect.appendChild(option);
            }
        }

        // Atualiza ao abrir o modal e ao trocar empresa
        empresaSelect.addEventListener('change', atualizarOpcoesRevendaEdit);
        atualizarOpcoesRevendaEdit();
    });
});

// Força letras maiúsculas e só permite letras no campo de usuário dos modais de edição
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[id^="usuario_id_edit_"]').forEach(function(input) {
        input.addEventListener('input', function(e) {
            // Só letras, transforma em maiúsculo
            this.value = this.value.replace(/[^A-Za-zÀ-ÿ\s]/g, '').toUpperCase();
        });
    });
});