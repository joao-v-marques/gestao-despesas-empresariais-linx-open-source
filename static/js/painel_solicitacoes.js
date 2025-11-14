const linhas = document.querySelectorAll("#tabela-corpo tr");
const filtroId = document.getElementById("filtro-id");
const filtroFornecedor = document.getElementById("filtro-fornecedor");
const filtroData = document.getElementById("filtro-data");
const filtroValor = document.getElementById("filtro-valor");
const filtroDpto = document.getElementById("filtro-departamento");

// Função para converter a data de DD/MM/AAAA → AAAA-MM-DD
function converteData(dataBr) {
    const partes = dataBr.split("/");
    if (partes.length !== 3) return null;
    const [dia, mes, ano] = partes;
    return `${ano}-${mes.padStart(2, '0')}-${dia.padStart(2, '0')}`; 
}

// Função principal da filtragem
function filtrarTabela() {
    const id = filtroId.value;
    const fornecedor = filtroFornecedor.value.toLowerCase();
    const data = filtroData.value;
    const valor = filtroValor.value;
    const departamento = filtroDpto.value;

    linhas.forEach(linha => {
        const colunas = linha.getElementsByTagName('td');
        const colId = colunas[0].textContent;
        const colFornecedor = colunas[4].textContent;
        const colData = colunas[5].textContent.trim();
        const colValor = colunas[7].textContent;
        const colDpto = colunas[6].textContent;

        const colDataIso = converteData(colData);

        const exibir = 
            (!id || colId.includes(id)) &&
            (!fornecedor || colFornecedor.includes(fornecedor)) &&
            (!data || colDataIso === data) &&
            (!valor || colValor.includes(valor)) &&
            (!departamento || colDpto.includes(departamento));

        linha.style.display = exibir ? '' : 'none';
    });
}


[filtroId, filtroFornecedor, filtroData, filtroValor, filtroDpto].forEach(input => {
    input.addEventListener('input', filtrarTabela);
});