from flask import Blueprint, render_template, url_for, redirect, flash, session, request
from flask_login import current_user, login_required, logout_user
from database.connect_db import abrir_cursor
from decorators import role_required

blueprint_principal = Blueprint('blueprint_principal', __name__)

# Rota que renderiza a pagina principal (Desativada)
@blueprint_principal.route('/')
@login_required
@role_required('Administrador')
def principal():
    return render_template('principal.html', usuario_logado=current_user.USUARIO)

# Rota para deslogar do sistema (Substituir por JWT)
@blueprint_principal.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash('Você deslogou da sua conta com sucesso!', 'success')
    return redirect(url_for('blueprint_login.pagina_login'))

# Rota para trocar a senha do usuário
@blueprint_principal.route('/troca-senha/<int:id>', methods=['POST'])
@login_required
def troca_senha(id):
    session.pop('_flashes', None)
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
        sql = "UPDATE SCHEMA.TABELA SET CAMPO = :1 WHERE CAMPO = :2"
        valores = [nova_senha_form, current_user]
        try:
            cursor, conn = abrir_cursor()
            cursor.execute(sql, valores)
            conn.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('blueprint_principal.principal'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro ao atualizar o usuário: {e}', 'error')
            return redirect(url_for('blueprint_principal.principal'))
        finally:
            cursor.close()
            conn.close()