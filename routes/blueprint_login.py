import logging
from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from flask_login import login_user
from database.connect_db import abrir_cursor
from database.models import User

blueprint_login = Blueprint('blueprint_login', __name__)

@blueprint_login.route('/')
def pagina_login():
    return render_template('login.html')

@blueprint_login.route('/fazer-login', methods=['POST'])
def fazer_login():
    if request.method == 'POST':
        session.pop('_flashes', None)
        usuario_form = request.form['usuario'].strip()
        senha_form = request.form['senha']
        
        sql = "SELECT ID, USUARIO, SENHA, FUNCAO FROM LIU_USUARIO WHERE USUARIO = :1"
        valores = [usuario_form]
        cursor, conn = abrir_cursor()
        try:
            cursor.execute(sql, valores)
            retorno = cursor.dict_fetchone()
            logging.info(f'Resultado da consulta: {retorno}')

            if not retorno:
                flash('Usuário não encontrado!', 'error')
                return redirect(url_for('blueprint_login.pagina_login'))
            if retorno[2] == senha_form:
                user = User(id=retorno[0], USUARIO=retorno[1], FUNCAO=retorno[3])
                login_user(user)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
            else:
                flash('Senha Incorreta! Tente novamente.', 'error')
                return redirect(url_for('blueprint_login.pagina_login'))
        except Exception as e:
            logging.error(f'Erro ao executar a consulta: {e}')
            flash('Erro interno ao realizar a consulta!', 'error')
            return redirect(url_for('blueprint_login.pagina_login'))
        finally:
            cursor.close()
            conn.close()
