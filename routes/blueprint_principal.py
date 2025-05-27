from flask import Blueprint, render_template, url_for, redirect, flash, session
from flask_login import current_user, login_required, logout_user

blueprint_principal = Blueprint('blueprint_principal', __name__)

@blueprint_principal.route('/')
@login_required
def principal():
    return render_template('principal.html', usuario_logado=current_user.USUARIO)

@blueprint_principal.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash('Você deslogou da sua conta com sucesso!', 'success')
    return redirect(url_for('blueprint_login.fazer_login'))