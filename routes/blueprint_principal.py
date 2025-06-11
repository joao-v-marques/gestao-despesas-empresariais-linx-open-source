from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from flask_login import current_user, login_required, logout_user
from decorators import role_required
from database.database import Usuarios

blueprint_principal = Blueprint('blueprint_principal', __name__)

@blueprint_principal.route('/')
@login_required
@role_required('ADMIN')
def principal():
    return render_template('principal.html', usuario_logado=current_user.USUARIO)

@blueprint_principal.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash('Você deslogou da sua conta com sucesso!', 'success')
    return redirect(url_for('blueprint_login.fazer_login'))

@blueprint_principal.route('/troca-senha/<int:id>', methods=['POST', 'GET'])
@login_required
def troca_senha(id):
    usuario = Usuarios.get_or_none(Usuarios.id == id)

    if request.method == 'POST':
        nova_senha_form = request.form['nova_senha'].strip()
        confirma_nova_senha_form = request.form['confirma_nova_senha'].strip()
        if nova_senha_form != confirma_nova_senha_form:
            flash('As duas senhas devem ser iguais!', 'error')
            return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        elif not nova_senha_form or not confirma_nova_senha_form:
            flash('Por favor, insira pelo menos um caractere.', 'error')
            return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        elif len(nova_senha_form) <=2:
            flash('A senha deve conter no minimo 3 caracteres! Tente novamente.', 'error')
            return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        else:
            usuario.SENHA = nova_senha_form
            usuario.save()
            flash('Senha alterada com sucesso!', 'success')
            logout_user()
            return redirect(url_for('blueprint_login.fazer_login'))

    return render_template('blueprint_painel_solicitacoes.painel_solicitacoes')