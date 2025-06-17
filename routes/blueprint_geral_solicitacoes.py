from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from decorators import role_required
from database.connect_db import abrir_cursor
import logging

blueprint_geral_solicitacoes = Blueprint('blueprint_geral_solicitacoes', __name__)

@blueprint_geral_solicitacoes.route('/')
@login_required
@role_required('DIRETORIA', 'ADMIN')
def geral_solicitacoes():
    filtro = request.args.get('filtro', 'PENDENTE')
    usuario_solicitante = request.args.get('usuario_solicitante', '')
    try:
        cursor, conn = abrir_cursor()
        if filtro == 'PENDENTE':
            sql = "SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = 'PENDENTE'"
            cursor.execute(sql)
            retorno = cursor.fetchall()
        if filtro == 'APROVADO':
            sql = "SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = 'APROVADO'"
            cursor.execute(sql)
            retorno = cursor.fetchall()
        if filtro == 'REPROVADO':
            sql = "SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = 'REPROVADO'"
            cursor.execute(sql)
            retorno = cursor.fetchall()
        if filtro == 'COMPRA':
            sql = "SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = 'COMPRA'"
            cursor.execute(sql)
            retorno = cursor.fetchall()
        if filtro == 'TODOS':
            sql = "SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES ORDER BY STATUS"
            cursor.execute(sql)
            retorno = cursor.fetchall()

            return render_template(
                'geral_solicitacoes.html',
                solicitacoes=retorno,
                filtro=filtro,
                usuario_logado=current_user.USUARIO,
                usuario_solicitante=usuario_solicitante
            )
    except Exception as e:
            flash('Erro ao realizar a consulta!', 'error')
            logging.error(f'Deu erro na consulta: {e}')
            return redirect(url_for('blueprint_geral_solicitacoes.geral_solicitacoes'))
    finally:
            cursor.close()
            conn.close()