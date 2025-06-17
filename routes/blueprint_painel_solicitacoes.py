import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor

blueprint_painel_solicitacoes = Blueprint('blueprint_painel_solicitacoes', __name__)

@blueprint_painel_solicitacoes.route('/', methods=['POST', 'GET'])
@login_required
def painel_solicitacoes():
        session.pop('_flashes', None)
        filtro = request.args.get('filtro', 'PENDENTE')

        try:
                cursor, conn = abrir_cursor()
                if filtro == 'PENDENTE':
                        sql = 'SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = :1 AND USUARIO_SOLICITANTE = :2'
                        valores = ['PENDENTE', current_user.USUARIO]
                        cursor.execute(sql, valores)
                        retorno = cursor.fetchall()
                        
                elif filtro == 'APROVADO':
                        sql = 'SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = :1 AND USUARIO_SOLICITANTE = :2'
                        valores = ['APROVADO', current_user.USUARIO]
                        cursor.execute(sql, valores)
                        retorno = cursor.fetchall()

                elif filtro == 'REPROVADO':
                        sql = 'SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = :1 AND USUARIO_SOLICITANTE = :2'
                        valores = ['REPROVADO', current_user.USUARIO]
                        cursor.execute(sql, valores)
                        retorno = cursor.fetchall()

                elif filtro == 'COMPRA':
                        sql = 'SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE STATUS = :1 AND USUARIO_SOLICITANTE = :2'
                        valores = ['COMPRA', current_user.USUARIO]
                        cursor.execute(sql, valores)
                        retorno = cursor.fetchall()

                elif filtro == 'TODOS':
                        sql = 'SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE USUARIO_SOLICITANTE = :1'
                        valores = [current_user.USUARIO]
                        cursor.execute(sql, valores)
                        retorno = cursor.fetchall()
                return render_template('painel_solicitacoes.html', solicitacoes=retorno, filtro=filtro, usuario_logado=current_user.USUARIO)
        except Exception as e:
                flash('Erro ao realizar a consulta!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
                cursor.close()
                conn.close()

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>')
@login_required
def mais_info_sol(id):
        try:
                cursor, conn = abrir_cursor()
                sql_solicitacao = "SELECT ID, EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, TIPO_DESPESA, DESCRICAO, VALOR, STATUS FROM LIU_SOLICITACOES WHERE ID = :1"
                cursor.execute(sql_solicitacao, [id])
                retorno_solicitacao = cursor.fetchone()
                
                sql_departamento = "SELECT * FROM LIU_DEPARTAMENTO ORDER BY CODIGO"
                cursor.execute(sql_departamento)
                retorno_departamento = cursor.fetchall()

                sql_tipo_despesa = "SELECT * FROM LIU_TIPO_DESPESA ORDER BY CODIGO"
                cursor.execute(sql_tipo_despesa)
                retorno_tipo_despesa = cursor.fetchall()

                return render_template('mais_info_sol.html', usuario_logado=current_user.USUARIO, solicitacao=retorno_solicitacao, departamento=retorno_departamento, tipo_despesa=retorno_tipo_despesa)
        except Exception as e:
                flash('Erro interno ao realizar a consulta!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
                cursor.close()
                conn.close()

@blueprint_painel_solicitacoes.route('mais_info_sol/<int:id>/dowload-pdf', methods=['GET'])
@login_required
def download_pdf(id):
        try:
                cursor, conn = abrir_cursor()
                sql = "SELECT PDF_PATH FROM LIU_SOLICITACOES WHERE ID = :1"
                cursor.execute(sql, {id})
                retorno = cursor.fetchone()

                if not retorno:
                        flash('Não foi possivel localizar o PDF!', 'error')
                        return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol'))
                else:
                        flash('PDF localizado!', 'success')
                        return send_file(retorno, as_attachment=True)
        except Exception as e:
                flash('Erro interno!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
                cursor.close()
                conn.close()

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/salvar', methods=['POST', 'GET'])
@login_required
def salvar_edicao(id):
        if request.method == 'POST':
                novo_departamento = request.form['departamento']
                novo_tipo_despesa = request.form['tipo_despesa']
                novo_descricao = request.form.get('descricao').strip()
                novo_valor = float(request.form.get('valor').replace('R$', '').replace('.', '').replace(',', '.').strip()) 
                try:
                        cursor, conn = abrir_cursor()
                        sql = "UPDATE LIU_SOLICITACOES SET DEPARTAMENTO = :1, TIPO_DESPESA = :2, DESCRICAO = :3, VALOR = :4 WHERE ID = :5"
                        valores = [novo_departamento, novo_tipo_despesa, novo_descricao, novo_valor, id]
                        cursor.execute(sql, valores)
                        conn.commit()
                        flash('Alteração realizada com sucesso!', 'success')
                        return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
                except Exception as e:
                        flash('Erro interno!', 'error')
                        logging.error(f'Deu erro na consulta: {e}')
                        return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol'))
                finally:
                        cursor.close()
                        conn.close()
        else:
                return redirect(url_for("blueprint_painel_solicitacoes.painel_solicitacoes"))

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/excluir', methods=['POST', 'GET'])
@login_required
def excluir_solicitacao(id):
        if request.method == 'POST':
                try:
                        cursor, conn = abrir_cursor()
                        sql = "DELETE FROM LIU_SOLICITACOES WHERE ID = :1"
                        cursor.execute(sql, [id])
                        flash('Solitação excluida com sucesso!', 'error')
                        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                except Exception as e:
                        flash('Erro interno!', 'error')
                        logging.error(f'Deu erro na consulta: {e}')
                        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
                finally:
                        cursor.close()
                        conn.close()
        else:
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/reenviar', methods=['POST', 'GET'])
@login_required
def reenviar_solicitacao(id):
        if request.method == 'POST':
                try:
                        cursor, conn = abrir_cursor()

                        sql = "UPDATE LIU_SOLICITACOES SET STATUS = :1 WHERE ID = :2"
                        valores = ['PENDENTE', id]
                        cursor.execute(sql, valores)
                        conn.commit()
                        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                except Exception as e:
                        flash('Erro interno!', 'error')
                        logging.error(f'Deu erro na consulta: {e}')
                        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                finally:
                        cursor.close()
                        conn.close()
        else:
                return render_template('painel_solicitacoes.html')