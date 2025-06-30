from flask import Blueprint, render_template, redirect, url_for, request, flash 
from flask_login import login_required, current_user
from decorators import role_required
from gerar_pdf import gerar_pdf
from database.connect_db import abrir_cursor
from datetime import datetime
import logging

blueprint_controle_diretoria = Blueprint('blueprint_controle_diretoria', __name__)

@blueprint_controle_diretoria.route('/')
@login_required
@role_required('ADMIN', 'DIRETORIA')
def controle_diretoria():
    try:
        cursor, conn = abrir_cursor()
        sql = """
        SELECT
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            s.USUARIO_SOLICITANTE,
            d.CODIGO AS DEPARTAMENTO_CODIGO,
            d.DESCRICAO  AS DEPARTAMENTO_DESCRICAO,
            t.CODIGO AS TIPO_DESPESA_CODIGO,
            t.DESCRICAO AS TIPO_DESPESA_DESCRICAO,
            s.VALOR,
            s.STATUS
        FROM
            LIU_SOLICITACOES s
        JOIN
            LIU_DEPARTAMENTO d ON s.DEPARTAMENTO = d.CODIGO
        JOIN
            LIU_TIPO_DESPESA t ON s.TIPO_DESPESA = t.CODIGO
        WHERE
            s.STATUS = 'PENDENTE'
        """

        cursor.execute(sql)
        retorno = cursor.dict_fetchall()

        return render_template('controle_diretoria.html', query=retorno, usuario_logado=current_user.USUARIO)
    except Exception as e:    
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
    finally:
        cursor.close()
        conn.close()

@blueprint_controle_diretoria.route('/mais-info/<int:id>')
@login_required
@role_required('ADMIN', 'DIRETORIA')
def mais_info_cd(id):
    try:
        cursor, conn = abrir_cursor()
        sql = """
        SELECT 
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            s.USUARIO_SOLICITANTE,
            d.CODIGO AS DEPARTAMENTO_CODIGO,
            d.DESCRICAO AS DEPARTAMENTO_DESCRICAO,
            t.CODIGO AS TIPO_DESPESA_CODIGO,
            t.DESCRICAO AS TIPO_DESPESA_DESCRICAO,
            s.DESCRICAO,
            s.VALOR,
            s.STATUS 
        FROM 
            LIU_SOLICITACOES s
        JOIN
            LIU_DEPARTAMENTO d ON s.DEPARTAMENTO = d.CODIGO
        JOIN
            LIU_TIPO_DESPESA t ON s.TIPO_DESPESA = t.CODIGO
        WHERE 
            s.ID = :1
        """
        cursor.execute(sql, [id])
        retorno = cursor.dict_fetchone()
        return render_template('mais_info_cd.html', usuario_logado=current_user.USUARIO, solicitacao=retorno)
    except Exception as e:
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
    finally:
        cursor.close()
        conn.close()

@blueprint_controle_diretoria.route('/mudar-status/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN', 'DIRETORIA')
def mudar_status(id):
    novo_status = request.form['status']
    if novo_status == 'APROVADO':
        try:
            cursor, conn = abrir_cursor()

            sql_solicitacao = "SELECT * FROM LIU_SOLICITACOES WHERE ID = :1"
            cursor.execute(sql_solicitacao, [id])
            solicitacao = cursor.dict_fetchone()

            pdf_path = gerar_pdf(solicitacao, current_user.USUARIO)

            sql_aprovado = "UPDATE LIU_SOLICITACOES SET STATUS = 'APROVADO', PDF_PATH = :1, USUARIO_AUTORIZANTE = :2 WHERE ID = :3"
            valores = [pdf_path, current_user.CODIGO_APOLLO, id]
            cursor.execute(sql_aprovado, valores)
            conn.commit()

            sql_max_processo = "SELECT MAX(NRO_PROCESSO) FROM FAT_PROCESSO_DESPESA"
            cursor.execute(sql_max_processo)
            max_processo = cursor.fetchone()[0]

            if max_processo is None:
                proximo_numero_processo = 1
            else:
                proximo_numero_processo = max_processo + 1
            
            data_atual = datetime.now()

            sql_inserir = "INSERT INTO FAT_PROCESSO_DESPESA (EMPRESA, REVENDA, NRO_PROCESSO, DTA_EMISSAO, DESCRICAO, VAL_PROCESSO, SITUACAO, USUARIO, DEPARTAMENTO, USUARIO_AUTORIZANTE, CLIENTE) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)"
            valores_inserir = [
                solicitacao['empresa'],
                solicitacao['revenda'],
                proximo_numero_processo,
                data_atual,
                f"{solicitacao['descricao']}. Aprovado por: {current_user.NOME}",
                solicitacao['valor'],
                'A',
                solicitacao['usuario_solicitante'],
                solicitacao['departamento'],
                current_user.CODIGO_APOLLO,
                solicitacao['fornecedor']
                ]
            cursor.execute(sql_inserir, valores_inserir)
            conn.commit()
            
            flash('Solicitação Aprovada e PDF gerado com sucesso!', 'success')
            return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
        except Exception as e:
            flash(f'Erro interno ao realizar a consulta: {e}', 'error')
            logging.error(f'Erro ao realizar a consulta: {e}')
            return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
        finally:
            cursor.close()
            conn.close()
    elif novo_status == 'REPROVADO':
        motivo_reprova = request.form['motivo_reprova']
        try:
            cursor, conn = abrir_cursor()
            sql = "UPDATE LIU_SOLICITACOES SET STATUS = 'REPROVADO', MOTIVO_REPROVA = :1 WHERE ID = :2"
            valores = [motivo_reprova, id]
            cursor.execute(sql, valores)
            conn.commit()
            flash('Solicitação Reprovada!', 'success')
            return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
        except Exception as e:
            flash(f'Erro interno ao realizar a consulta: {e}', 'error')
            return redirect(url_for('blueprint_controle_diretoria.mais_info_cd', id=id))
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Status inválido!', 'error')
        return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))