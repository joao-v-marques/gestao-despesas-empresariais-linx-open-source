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
@role_required('Administrador', 'Gerente', 'Corporativo')
def geral_solicitacoes():
    filtro = request.args.get('filtro', 'PENDENTE')
    usuario_solicitante = request.args.get('usuario_solicitante', '')
    try:
        cursor, conn = abrir_cursor()
        base_sql = """
        SELECT DISTINCT
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            u.CAMPO AS CAMPO,
            d.CAMPO AS CAMPO,
            d.CAMPO AS CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO
        FROM
            SCHEMA.TABELA s
        LEFT JOIN
            SCHEMA.TABELA d ON s.CAMPO = d.CAMPO
        LEFT JOIN
            SCHEMA.TABELA u ON s.CAMPO = u.CAMPO
        """
        
        if filtro != 'TODOS':
            sql = base_sql + "WHERE s.CAMPO = :1"
            valores = [filtro]
        else:
            sql = base_sql + "ORDER BY CAMPO"
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
@role_required('Administrador', 'Gerente', 'Corporativo')
def download_relatorio():
    try:
        cursor, conn = abrir_cursor()
        sql = """
        SELECT DISTINCT
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            u.CAMPO AS CAMPO,
            d.CAMPO AS CAMPO,
            d.CAMPO AS CAMPO,
            s.CAMPO,
            s.CAMPO
        FROM
            SCHEMA.TABELA s
        JOIN
            SCHEMA.TABELA d ON s.CAMPO = d.CAMPO
        JOIN
            SCHEMA.TABELA u on s.CAMPO = u.CAMPO
    """
        
        filtro = request.args.get('filtro', 'PENDENTE')
        if filtro != 'TODOS':
            sql += "WHERE s.CAMPO = :1"
            valores = [filtro]
        else:
            sql += "ORDER BY s.CAMPO"
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
            