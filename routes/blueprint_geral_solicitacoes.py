from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from decorators import role_required
from database.connect_db import abrir_cursor

blueprint_geral_solicitacoes = Blueprint('blueprint_geral_solicitacoes', __name__)

@blueprint_geral_solicitacoes.route('/')
@login_required
@role_required('Administrador', 'Aprovador')
def geral_solicitacoes():
    filtro = request.args.get('filtro', 'PENDENTE')
    usuario_solicitante = request.args.get('usuario_solicitante', '')
    try:
        cursor, conn = abrir_cursor()
        base_sql = """
        SELECT DISTINCT
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            u.LOGIN AS USUARIO_SOLICITANTE,
            d.DEPARTAMENTO AS DEPARTAMENTO_CODIGO,
            d.NOME AS DEPARTAMENTO_DESCRICAO,
            s.VALOR,
            s.DESCRICAO,
            s.MOTIVO_REPROVA,
            s.STATUS,
            s.NRO_PROCESSO,
            s.FORNECEDOR
        FROM
            LIU_SOLICITACOES s
        JOIN
            GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
        JOIN
            GER_USUARIO u ON s.USUARIO_SOLICITANTE = u.USUARIO
        """
        
        if filtro != 'TODOS':
            sql = base_sql + "WHERE s.STATUS = :1"
            valores = [filtro]
        else:
            sql = base_sql + "ORDER BY USUARIO_SOLICITANTE"
            valores = []

        cursor.execute(sql, valores)
        retorno = cursor.dict_fetchall()

        return render_template('geral_solicitacoes.html', solicitacoes=retorno, filtro=filtro, usuario_logado=current_user.USUARIO, usuario_solicitante=usuario_solicitante)              
    except Exception as e:
            flash(f'Erro ao realizar a consulta: {e}', 'error')
            return render_template(
                'geral_solicitacoes.html',
                solicitacoes=retorno,
                filtro=filtro,
                usuario_logado=current_user.USUARIO,
                usuario_solicitante=usuario_solicitante
            )
    finally:
            cursor.close()
            conn.close()