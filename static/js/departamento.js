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
});