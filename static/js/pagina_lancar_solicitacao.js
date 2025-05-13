document.addEventListener('DOMContentLoaded', function () {
    const valorInput = document.querySelector('.input-valor');

    valorInput.addEventListener('input', function (e) {
        let valor = e.target.value;

        
        valor = valor.replace(/\D/g, '');

        
        valor = (valor / 100).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });

        
        e.target.value = valor;
    });

    valorInput.addEventListener('focus', function (e) {
        
        e.target.value = e.target.value.replace(/[^\d]/g, '');
    });

    valorInput.addEventListener('blur', function (e) {
        
        let valor = e.target.value;

        if (valor) {
            valor = (parseFloat(valor) / 100).toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            });
            e.target.value = valor;
        }
    });
});
