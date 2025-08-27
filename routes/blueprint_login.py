from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from flask_login import login_user
from database.connect_db import abrir_cursor
from database.models import User
import logging

blueprint_login = Blueprint('blueprint_login', __name__)

# Rota que renderiza a pagina de login
@blueprint_login.route('/')
def pagina_login():
    return render_template('login.html')

# Rota para realizar o login
@blueprint_login.route('/fazer-login', methods=['POST'])
def fazer_login():
    session.pop('_flashes', None)
    usuario_form = request.form['usuario'].strip()
    senha_form = request.form['senha']
    try:
        cursor, conn = abrir_cursor()
        sql = "SELECT ID, USUARIO, SENHA, NOME, FUNCAO, CODIGO_APOLLO, EMPRESA, REVENDA FROM LIU.LIU_USUARIO WHERE USUARIO = :1"
        valores = [usuario_form]

        cursor.execute(sql, valores)
        retorno = cursor.dict_fetchone()

        if not retorno:
            flash('Usuário não encontrado!', 'error')
            return redirect(url_for('blueprint_login.pagina_login'))
        if retorno['senha'] == senha_form:
            user = User(id=retorno['id'], USUARIO=retorno['usuario'], FUNCAO=retorno['funcao'], NOME=retorno['nome'], CODIGO_APOLLO=retorno['codigo_apollo'], EMPRESA=retorno['empresa'], REVENDA=retorno['revenda'])
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        else:
            flash('Senha Incorreta! Tente novamente.', 'error')
            return redirect(url_for('blueprint_login.pagina_login'))
    except Exception as e:
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        logging.error(f'Erro: {e}')
        return redirect(url_for('blueprint_login.pagina_login'))
    finally:
        cursor.close()
        conn.close()