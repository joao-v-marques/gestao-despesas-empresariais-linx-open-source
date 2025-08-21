from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

# Define o decorador das funções: Administrador, Aprovador e Solicitante
def role_required(*roles):
    def decorators(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.FUNCAO not in roles:
                flash('Você não tem permissão para acessar rota!', 'info')
                return redirect(url_for('blueprint_login.pagina_login'))
            return func(*args, **kwargs)
        return wrapper
    return decorators