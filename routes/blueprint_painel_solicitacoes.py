import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor

blueprint_painel_solicitacoes = Blueprint('blueprint_painel_solicitacoes', __name__)

@blueprint_painel_solicitacoes.route('/')
@login_required
def painel_solicitacoes():
        session.pop('_flashes', None)
        filtro = request.args.get('filtro', 'PENDENTE')
        sort_by = request.args.get('sort_by', 'ID').upper()
        sort_dir = request.args.get('sort_dir', 'ASC').upper()

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
                t.CODIGO AS TIPO_DESPESA_CODIGO, 
                t.DESCRICAO AS TIPO_DESPESA_DESCRICAO, 
                s.VALOR, 
                s.STATUS
            FROM 
                LIU_SOLICITACOES s
            JOIN 
                GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
            JOIN 
                LIU_TIPO_DESPESA t ON s.TIPO_DESPESA = t.CODIGO
            JOIN
                GER_USUARIO u on s.USUARIO_SOLICITANTE = u.USUARIO
        """
                
            if filtro != 'TODOS':
                sql = base_sql + " WHERE s.STATUS = :1 AND s.USUARIO_SOLICITANTE = :2"
                valores = [filtro, current_user.CODIGO_APOLLO]
            else:
                sql = base_sql + " WHERE s.USUARIO_SOLICITANTE = :1"
                valores = [current_user.CODIGO_APOLLO]

            colunas_permitidas = [
                   'ID', 'EMPRESA', 'REVENDA', 'USUARIO_SOLICITANTE', 'DEPARTAMENTO_CODIGO', 'DEPARTAMENTO_DESCRICAO', 'TIPO_DESPESA_CODIGO', 'TIPO_DESPESA_DESCRICAO', 'VALOR', 'STATUS'
            ]

            if sort_by not in colunas_permitidas:
                   sort_by = 'ID'
            if sort_dir not in ['ASC', 'DESC']:
                   sort_dir = 'ASC'

            sql += f"ORDER BY {sort_by} {sort_dir}"

            cursor.execute(sql, valores)
            retorno = cursor.dict_fetchall()

            return render_template('painel_solicitacoes.html',
                                    solicitacoes=retorno,
                                    filtro=filtro,
                                    usuario_logado=current_user.USUARIO,
                                    sort_by=sort_by,
                                    sort_dir=sort_dir
                                    )
        except Exception as e:
                flash(f'Erro ao realizar a consulta: {e}', 'error')
                logging.error(f'erro: {e}')
                return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
        finally:
                cursor.close()
                conn.close()

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>')
@login_required
def mais_info_sol(id):
        try:
            cursor, conn = abrir_cursor()
            sql_solicitacao = """SELECT
                                    s.ID,
                                    s.EMPRESA,
                                    s.REVENDA,
                                    u.LOGIN AS USUARIO_SOLICITANTE,
                                    d.DEPARTAMENTO AS CODIGO,
                                    d.NOME AS NOME,
                                    t.CODIGO AS CODIGO,
                                    t.DESCRICAO AS CODIGO,
                                    s.DESCRICAO AS DESCRICAO,
                                    s.VALOR,
                                    s.STATUS
                                FROM
                                    LIU_SOLICITACOES s
                                JOIN 
                                    GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
                                JOIN 
                                    LIU_TIPO_DESPESA t ON s.TIPO_DESPESA = t.CODIGO
                                JOIN
                                    GER_USUARIO u on s.USUARIO_SOLICITANTE = u.USUARIO
                                WHERE 
                                    ID = :1
                                    """
            cursor.execute(sql_solicitacao, [id])
            retorno_solicitacao = cursor.dict_fetchone()
                
            sql_departamento = "SELECT * FROM GER_DEPARTAMENTO ORDER BY DEPARTAMENTO"
            cursor.execute(sql_departamento)
            retorno_departamento = cursor.dict_fetchall()

            sql_tipo_despesa = "SELECT * FROM LIU_TIPO_DESPESA ORDER BY CODIGO"
            cursor.execute(sql_tipo_despesa)
            retorno_tipo_despesa = cursor.dict_fetchall()

            return render_template('mais_info_sol.html', usuario_logado=current_user.USUARIO, solicitacao=retorno_solicitacao, departamento=retorno_departamento, tipo_despesa=retorno_tipo_despesa)
        except Exception as e:
                flash(f'Erro interno ao realizar a consulta: {e}', 'error')
                logging.info(f'{e}')
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
            cursor.execute(sql, [id])
            retorno = cursor.dict_fetchone()

            if not retorno:
                flash('Não foi possivel localizar o PDF!', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol'))
            else:
                flash('PDF localizado!', 'success')
                return send_file(retorno['pdf_path'], as_attachment=True)
        except Exception as e:
                flash(f'Erro interno: {e}', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
                cursor.close()
                conn.close()

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/salvar', methods=['POST'])
@login_required
def salvar_edicao(id):
            novo_departamento = request.form['departamento']
            novo_tipo_despesa = request.form['tipo_despesa']
            novo_descricao = request.form.get('descricao').strip()
            novo_valor = float(request.form.get('valor').replace('R$', '').replace('.', '').replace(',', '.').strip())
            
            if len(novo_departamento) != 3:
                    flash('O departamento deve ter exatamente 3 caracteres!')
                    return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
            elif len(novo_tipo_despesa) != 4:
                    flash('O Tipo de Despesa deve ter exatamente 4 caracteres!')
                    return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
            else:
                try:
                    cursor, conn = abrir_cursor()
                    sql = """
                            UPDATE 
                                LIU_SOLICITACOES
                            SET 
                                DEPARTAMENTO = :1,
                                TIPO_DESPESA = :2,
                                DESCRICAO = :3,
                                VALOR = :4 
                            WHERE 
                                ID = :5
                            """
                    valores = [novo_departamento, novo_tipo_despesa, novo_descricao, novo_valor, id]
                    cursor.execute(sql, valores)
                    conn.commit()
                    flash('Alteração realizada com sucesso!', 'success')
                    return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', ixd=id))
                except Exception as e:
                    flash(f'Erro na consulta: {e}', 'error')
                    return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
                finally:
                    cursor.close()
                    conn.close()
        
@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_solicitacao(id):
            try:
                cursor, conn = abrir_cursor()
                sql = "DELETE FROM LIU_SOLICITACOES WHERE ID = :1"
                cursor.execute(sql, [id])
                conn.commit()
                flash('Solitação excluida com sucesso!', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
            except Exception as e:
                flash('Erro na consulta: {e}', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
            finally:
                cursor.close()
                conn.close()

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/reenviar', methods=['POST'])
@login_required
def reenviar_solicitacao(id):
                try:
                    cursor, conn = abrir_cursor()

                    sql = "UPDATE LIU_SOLICITACOES SET STATUS = :1 WHERE ID = :2"
                    valores = ['PENDENTE', [id]]
                    cursor.execute(sql, valores)
                    conn.commit()
                    return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                except Exception as e:
                    flash(f'Erro na consulta: {e}', 'error')
                    return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                finally:
                    cursor.close()
                    conn.close()