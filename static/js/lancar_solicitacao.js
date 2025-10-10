// Puxa a empresa e revenda do HTML
const empresaInput = document.querySelector('#empresa_id');
const revendaInput = document.querySelector('#revenda_id');

// ! NOVA FUNCAO PARA ATUALIZAR A REVENDA COM BASE NA EMPRESA
function atualizarOpcoesRevenda() {
    if (empresaInput.value == '1') {
        revendaInput.innerHTML = 
        `
        <option value="1">1 - VALTRA PARANAVAÍ</option>
        <option value="2">2 - VALTRA CAMPO MOURÃO</option>
        <option value="3">3 - VALTRA GOIOERÊ</option>
        <option value="4">4 - VALTRA UBIRATÃ</option>
        <option value="5">5 - VALTRA NAVIRAI</option>
        <option value="6">6 - VALTRA MARINGÁ</option>
        <option value="7">7 - VALTRA UMUARAMA</option>
        <option value="8">8 - FENDT CAMPO MOURÃO</option>
        <option value="9">9 - VALTRA LONDRINA</option>
        <option value="10">10 - VALTRA CORNELIO PROCÓPIO</option>
        <option value="11">11 - VALTRA JARDIM ALEGRE</option>
        <option value="12">12 - VALTRA IRATI</option>
        `
    } else if (empresaInput.value == '4') {
        revendaInput.innerHTML = 
        `
        <option value="1">1 - KATO MAQ. STO ANTONIO DA PLATINA</option>
        <option value="2">2 - KATO MAQ. NAVIRAI</option>
        `
    }
}

// ! ANTIGA FUNCAO DE ATUALIZAR A REVENDA COM BASE NA EMPRESA
// function atualizarOpcoesRevenda() {
//     revendaInput.innerHTML = '';

//     if (empresaInput.value == '1') {
//         for (let i = 1; i <= 11; i++) {
//             const option = document.createElement('option');
//             option.value = i;
//             option.textContent = `${i}`;
//             revendaInput.appendChild(option);
//         }
//     } else if (empresaInput.value == '4') {
//         for (let i = 1; i <= 2; i++) {
//             const option = document.createElement('option');
//             option.value = i;
//             option.textContent = `${i}`;
//             revendaInput.appendChild(option);
//         }
//     }
// }

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

// Função que atualiza os fornecedores -------------------------------------------------------------------
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

// Função que atualiza as origens ------------------------------------------------------------------------
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
                option.text = `${origem.origem} - ${origem.des_origem}`;
                origemSelect.appendChild(option);
            });
        });
}

document.addEventListener('DOMContentLoaded', function () {
    buscarOrigens();
});

const btnEnviar = document.getElementById("btnOpenModal");

btnEnviar.addEventListener('click', function () {
    const empresa = document.getElementById("empresa_id").value;
    const revenda = document.getElementById("revenda_id").value;
    const departamento = document.getElementById("departamento_id").value;
    const origem = document.getElementById("origem_id").value;

    // Listener do botão "Enviar OS" (só precisa ser adicionado uma vez)
    document.getElementById("btnEnviarOS").onclick = function () {
        const nroOSValue = document.getElementById("nroOS_input").value.trim();
        if (!nroOSValue) {
            alert("Por favor, insira o número da O.S.");
            return;
        }

        document.getElementById("nroOS").value = nroOSValue;
        document.getElementById("mainForm").submit();
    };

    if (origem === '5121') {
        // NÃO chama o fetch
        const modal5121 = new bootstrap.Modal(document.getElementById("modal5121"));
        modal5121.show();

    } else {
        // Aqui SIM executa o fetch do orçamento
        fetch('/lancar-solicitacao/fazer-lancamento/confirm', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                empresa_form: empresa,
                revenda_form: revenda,
                departamento_form: departamento,
                origem_form: origem
            })
        })
        .then(response => response.json())
        .then(data => {
            const campo_valor = document.getElementById("valModal");
            const campo_pergunta = document.querySelector(".modalAsk");
            const modalConfirmButton = document.getElementById("modalConfirmButton");
            const modalConfirm = document.getElementById("modalConfirma");

            modalConfirm.addEventListener('hidden.bs.modal', () => {
                campo_valor.classList.remove('green', 'red', 'notFound');
                campo_pergunta.textContent = 'Confirme se deseja solicitar mesmo assim';
                modalConfirmButton.removeAttribute('hidden');
            });

            if (Array.isArray(data) && data.length > 0) {
                const valor = parseFloat(data[0].valor);
                campo_valor.textContent = `R$ ${valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;

                if (valor <= 0) {
                    campo_valor.classList.add("red");
                    campo_valor.classList.remove("green");
                } else {
                    campo_valor.classList.add("green");
                    campo_valor.classList.remove("red");
                }

                // Exibe o modal de confirmação
                const modal = new bootstrap.Modal(document.getElementById("modalConfirma"));
                modal.show();

            } else {
                campo_valor.textContent = "Nenhum valor foi encontrado!";
                campo_pergunta.textContent = "Não é possível lançar uma solicitação sem orçamento.";
                modalConfirmButton.setAttribute("hidden", "true");
                campo_valor.classList.add("notFound");
                campo_valor.classList.remove("green", "red");

                // Ainda exibe o modal para mostrar o erro
                const modal = new bootstrap.Modal(document.getElementById("modalConfirma"));
                modal.show();
            }
        })
        .catch(error => {
            alert("Erro ao buscar orçamento.");
            console.error(error);
        });
    }
});

const btnEnviar5121 = document.getElementById("btnEnviarOS");

btnEnviar5121.addEventListener("click", function () {
    if (btnEnviar5121.disabled) return;

    btnEnviar5121.disabled = true;

    btnEnviar5121.value = "Enviando...";
})

const btnEnviarModalConfirma = document.getElementById("modalConfirmButton");

btnEnviarModalConfirma.addEventListener("click", function () {
    if (btnEnviarModalConfirma.disabled) return;

    btnEnviarModalConfirma.disabled = true;

    btnEnviarModalConfirma.textContent = "Enviando...";
})


document.getElementById("nroOS_input").addEventListener("input", function () {
    this.value = this.value.replace(/\D/g, "");
})

document.getElementById("btnLimpar").addEventListener("click", function () {
    document.querySelector(".formulario").reset();
    buscarOrigens();
});

document.getElementById("modalConfirmButton").addEventListener("click", function () {
    document.querySelector('.formulario').submit();
});