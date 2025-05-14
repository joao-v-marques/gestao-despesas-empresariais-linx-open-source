from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required, logout_user

blueprint_principal = Blueprint('blueprint_principal', __name__)

@blueprint_principal.route('/')
@login_required
def pagina_principal():
    return render_template('pagina_principal.html', usuario_logado=current_user.USUARIO)

@blueprint_principal.route('/logout')
@login_required
def funcao_logout():
    logout_user()
    flash('Você deslogou da sua conta com sucesso!', 'success')
    return redirect(url_for('blueprint_login.pagina_login'))