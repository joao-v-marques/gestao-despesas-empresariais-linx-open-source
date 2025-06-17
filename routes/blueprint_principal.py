import logging
from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from flask_login import current_user, login_required, logout_user
from database.connect_db import abrir_cursor
from decorators import role_required

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
    if request.method == 'POST':
        nova_senha_form = request.form['nova_senha'].strip()
        confirma_nova_senha_form = request.form['confirma_nova_senha'].strip()

        if nova_senha_form != confirma_nova_senha_form:
            flash('As duas senhas devem ser iguais!', 'error')
            return redirect(url_for('blueprint_principal.principal'))
        elif not nova_senha_form or not confirma_nova_senha_form:
            flash('Nenhum campo pode estar vazio!', 'error')
            return redirect(url_for('blueprint_principal.principal'))
        elif len(nova_senha_form) <= 2:
            flash('A senha deve conter no minimo 3 caracteres! Tente novamente.', 'error')
            return redirect(url_for('blueprint_principal.principal'))
        else:
            sql = "UPDATE LIU_USUARIO SET SENHA = :1 WHERE USUARIO = :2"
            valores = [nova_senha_form, current_user]
            cursor, conn = abrir_cursor()
            try:
                cursor.execute(sql, valores)
                logging.info('Atualizou Certin')
                logging.info(f'Usuário atualizado com sucesso!')
                return redirect(url_for('blueprint_principal.principal'))
            except Exception as e:
                logging.error(f'Erro as atualizar o usuário: {e}')
                flash('Erro ao atualizar o usuário!', 'error')
                return redirect(url_for('blueprint_principal.principal'))
            finally:
                cursor.close()
                conn.close()
    else:
        return redirect(url_for('blueprint_principal.principal'))