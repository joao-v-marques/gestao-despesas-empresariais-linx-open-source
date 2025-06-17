from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from decorators import role_required
from gerar_pdf import gerar_pdf
from database.connect_db import abrir_cursor
import logging

blueprint_controle_diretoria = Blueprint('blueprint_controle_diretoria', __name__)

@blueprint_controle_diretoria.route('/')
@login_required
@role_required('ADMIN', 'DIRETORIA')
def controle_diretoria():
    try:
        cursor, conn = abrir_cursor()
        sql = "SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = 'PENDENTE'"
        cursor.execute(sql)
        retorno = cursor.fetchall()

        return render_template('controle_diretoria.html', query=retorno, usuario_logado=current_user.USUARIO)
    except Exception as e:    
        flash('Erro interno ao realizar a consulta!', 'error')
        logging.error(f'Deu erro na consulta: {e}')
        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
    finally:
        cursor.close()
        conn.close()

@blueprint_controle_diretoria.route('/mais-info/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN', 'DIRETORIA')
def mais_info_cd(id):
    try:
        cursor, conn = abrir_cursor()
        sql = 'SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE ID = :1'
        cursor.execute(sql, id)
        retorno = cursor.fetchone()
        return render_template('mais_info_cd.html', usuario_logado=current_user.USUARIO, solicitacao=retorno)
    except Exception as e:
        flash('Erro interno ao realizar a consulta!', 'error')
        logging.error(f'Deu erro na consulta: {e}')
        return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
    finally:
        cursor.close()
        conn.close()

@blueprint_controle_diretoria.route('/mudar-status', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN', 'DIRETORIA')
def mudar_status():
    if request.method == 'POST':
        novo_status = request.form['status']
        if novo_status == 'APROVADO':
            try:
                cursor, conn = abrir_cursor()
                sql = "UPDATE LIU_SOLICITACOES SET STATUS = 'APROVADO' WHERE ID = :1"
                cursor.execute(sql, id)
                conn.commit()
                flash('Solicitação Aprovada!', 'success')
                return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
            except Exception as e:
                flash('Erro interno ao realizar a consulta!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
            finally:
                cursor.close()
                conn.close()
        elif novo_status == 'REPROVADO':
            try:
                cursor, conn = abrir_cursor()
                sql = "UPDATE LIU_SOLICITACOES SET STATUS = 'REPROVADO' WHERE ID = :1"
                cursor.execute(sql, id)
                conn.commit()
                flash('Solicitação Reprovada!', 'success')
                return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
            except Exception as e:
                flash('Erro interno ao realizar a consulta!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_controle_diretoria.mais_info_cd'))
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Status inválido!', 'error')
            return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))

    else:
        return render_template('')