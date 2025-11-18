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

// Força letras maiúsculas no campo de usuário dos modais de edição, sem bloquear números ou outros caracteres
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[id^="usuario_id_edit_"]').forEach(function(input) {
        input.addEventListener('input', function(e) {
            this.value = this.value.toUpperCase();
        });
    });
});


// Função para garantir que não seja cadastrado diversos usuários de uma só vez
const formCad = document.getElementById("formCad");
const btnCad = document.getElementById("btnCad");

formCad.addEventListener("submit", function () {
    if (btnCad.disabled) return;

    btnCad.disabled = true;
    btnCad.value = "Cadastrando..."
})

const formEditar = document.getElementById("formEditar");
const btnEditar = document.getElementById("btnEditar");

formEditar.addEventListener("submit", function () {
    if (btnEditar.disabled) return;

    btnEditar.disabled = true;
    btnEditar.value = "Fazendo Alterações..."
})

const formDeletar = document.getElementById("formDeletar");
const btnDeletar = document.getElementById("btnDeletar");

formDeletar.addEventListener("submit", function () {
    if (btnDeletar.disabled) return;

    btnDeletar.disabled = true;
    btnDeletar.textContent = "Deletando..."; 
})

// ! FUNCAO PARA FILTAR A TABELA

linhas = document.querySelectorAll("#tabela-corpo tr");
const filtroId = document.getElementById("filtro-id");
const filtroApollo = document.getElementById("filtro-apollo")
const filtroEmpRev = document.getElementById("filtro-emp-rev");
const filtroUsuario = document.getElementById("filtro-usuario");
const filtroNome = document.getElementById("filtro-nome");
const filtroFuncao = document.getElementById("filtro-funcao");


function filtrarTabela() {
    const tabelaId = filtroId.value;
    const tabelaApollo = filtroApollo.value;
    const tabelaEmpresa = filtroEmpRev.value;
    const tabelaUsuario = filtroUsuario.value;
    const tabelaNome = filtroNome.value;
    
    const tabelaFuncao = filtroFuncao.value;

    linhas.forEach(linha => {
        colunas = linha.getElementsByTagName('td');
        const colId = colunas[0].textContent;
        const colApollo = colunas[1].textContent;
        const colEmpRev = colunas[2].textContent;
        const colUsuario = colunas[3].textContent;
        const colNome = colunas[5].textContent;
        const colFuncao = colunas[6].textContent;

        const exibir = 
            (!tabelaId || colId.includes(tabelaId)) &&
            (!tabelaApollo || colApollo.includes(tabelaApollo)) &&
            (!tabelaEmpresa || colEmpRev.includes(tabelaEmpresa)) &&
            (!tabelaUsuario || colUsuario.includes(tabelaUsuario)) &&
            (!tabelaNome || colNome.includes(tabelaNome)) &&
            (tabelaFuncao === "todos" || !tabelaFuncao || colFuncao.includes(tabelaFuncao));

        linha.style.display = exibir ? '' : 'none';
    })
}

[filtroId, filtroApollo, filtroEmpRev, filtroUsuario, filtroNome, filtroFuncao].forEach(input => {
    input.addEventListener('input', filtrarTabela);
});