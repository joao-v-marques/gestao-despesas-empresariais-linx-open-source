from io import BytesIO
from datetime import date
from gerar_relatorio import gerar_relatorio
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from decorators import role_required
from database.connect_db import abrir_cursor

blueprint_geral_solicitacoes = Blueprint('blueprint_geral_solicitacoes', __name__)

# Rota que renderiza a pagina de Solicitações em geral
@blueprint_geral_solicitacoes.route('/')
@login_required
@role_required('Administrador', 'Gerente', 'Diretoria')
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
            LIU.LIU_SOLICITACOES s
        LEFT JOIN
            PONTAL.GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
        LEFT JOIN
            PONTAL.GER_USUARIO u ON s.USUARIO_SOLICITANTE = u.USUARIO
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

# Rota para fazer download do relatório de solicitações
@blueprint_geral_solicitacoes.route('/download-relatorio')
@login_required
@role_required('Administrador', 'Gerente', 'Diretoria')
def download_relatorio():
    try:
        cursor, conn = abrir_cursor()
        sql = """
        SELECT DISTINCT
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            s.NRO_PROCESSO,
            s.USUARIO_AUTORIZANTE,
            s.DESCRICAO,
            s.FORNECEDOR,
            u.LOGIN AS USUARIO_SOLICITANTE,
            d.DEPARTAMENTO AS DEPARTAMENTO_CODIGO,
            d.NOME AS DEPARTAMENTO_DESCRICAO,
            s.VALOR,
            s.STATUS
        FROM
            LIU.LIU_SOLICITACOES s
        JOIN
            PONTAL.GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
        JOIN
            PONTAL.GER_USUARIO u on s.USUARIO_SOLICITANTE = u.USUARIO
    """
        
        filtro = request.args.get('filtro', 'PENDENTE')
        if filtro != 'TODOS':
            sql += "WHERE s.STATUS = :1"
            valores = [filtro]
        else:
            sql += "ORDER BY s.STATUS"
            valores = []
            
        cursor.execute(sql, valores)

        dados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]

        dia_atual = date.today()
        dia_formatado = dia_atual.strftime("%d_%m_%Y")

        buffer = BytesIO()
        gerar_relatorio(dados, colunas, buffer)
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name=f'relatorio_solicitacoes_{dia_formatado}.xlsx')
    
    except Exception as e:
        flash(f'Erro na consulta: {e}', 'error')
        return redirect(url_for('blueprint_geral_solicitacoes.geral_solicitacoes'))
    finally:
        cursor.close()
        conn.close()
            