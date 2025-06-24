from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from decorators import role_required
from database.connect_db import abrir_cursor

blueprint_geral_solicitacoes = Blueprint('blueprint_geral_solicitacoes', __name__)

@blueprint_geral_solicitacoes.route('/')
@login_required
@role_required('DIRETORIA', 'ADMIN')
def geral_solicitacoes():
    filtro = request.args.get('filtro', 'PENDENTE')
    usuario_solicitante = request.args.get('usuario_solicitante', '')
    try:
        cursor, conn = abrir_cursor()
        base_sql = """
        SELECT
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            s.USUARIO_SOLICITANTE,
            d.CODIGO AS DEPARTAMENTO_CODIGO,
            d.DESCRICAO AS DEPARTAMENTO_DESCRICAO,
            t.CODIGO AS TIPO_DESPESA_CODIGO,
            t.DESCRICAO AS TIPO_DESPESA_DESCRICAO,
            s.VALOR,
            s.DESCRICAO,
            s.MOTIVO_REPROVA,
            s.STATUS
        FROM
            LIU_SOLICITACOES s
        JOIN
            LIU_DEPARTAMENTO d ON s.DEPARTAMENTO = d.CODIGO
        JOIN
            LIU_TIPO_DESPESA t ON s.TIPO_DESPESA = t.CODIGO
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