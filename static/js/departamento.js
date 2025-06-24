document.addEventListener('DOMContentLoaded', function() {
    const descricaoInput = document.getElementById('descricao_id');
    const form = document.querySelector('.formulario');
    if (descricaoInput && form) {
        descricaoInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
        form.addEventListener('submit', function() {
            descricaoInput.value = descricaoInput.value.toUpperCase();
        });
    }

    // Bloqueia qualquer caractere não numérico nos campos de código (cadastro e edição)
    ['codigo_id', 'edit_codigo_id'].forEach(function(id) {
        document.querySelectorAll('#' + id).forEach(function(input) {
            input.addEventListener('input', function() {
                this.value = this.value.replace(/[^0-9]/g, '');
            });
        });
    });
});