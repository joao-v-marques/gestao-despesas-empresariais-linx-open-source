from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

def role_required(*roles):
    def decorators(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.FUNCAO not in roles:
                flash('Você não tem permissão para acessar esta página!', 'info')
                return redirect(url_for('blueprint_principal.pagina_principal'))
            return func(*args, **kwargs)
        return wrapper
    return decorators