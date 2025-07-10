import logging, os
from datetime import date
from gerar_relatorio import gerar_relatorio
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
                s.VALOR, 
                s.STATUS,
                s.NRO_PROCESSO
            FROM 
                LIU_SOLICITACOES s
            JOIN 
                GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
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
                   'ID', 'NRO_PROCESSO', 'EMPRESA', 'REVENDA', 'USUARIO_SOLICITANTE', 'DEPARTAMENTO_CODIGO', 'DEPARTAMENTO_DESCRICAO', 'VALOR', 'STATUS'
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
                                    s.NRO_PROCESSO,
                                    s.EMPRESA,
                                    s.REVENDA,
                                    u.LOGIN AS USUARIO_SOLICITANTE,
                                    d.DEPARTAMENTO AS CODIGO,
                                    d.NOME AS NOME,
                                    s.DESCRICAO AS DESCRICAO,
                                    s.VALOR,
                                    s.STATUS,
                                    s.MOTIVO_REPROVA,
                                    s.FORNECEDOR,
                                    s.USUARIO_AUTORIZANTE
                                FROM
                                    LIU_SOLICITACOES s
                                JOIN 
                                    GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
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

            sql_autorizante = "SELECT USUARIO, LOGIN FROM GER_USUARIO WHERE USUARIO = :1"
            valores_autorizante = [retorno_solicitacao['usuario_autorizante']]
            cursor.execute(sql_autorizante, valores_autorizante)
            retorno_autorizante = cursor.dict_fetchone()

            return render_template('mais_info_sol.html', usuario_logado=current_user.USUARIO, solicitacao=retorno_solicitacao, departamento=retorno_departamento, usuario_autorizante=retorno_autorizante)
        except Exception as e:
                flash(f'Erro interno ao realizar a consulta: {e}', 'error')
                logging.info(f'{e}')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
                cursor.close()
                conn.close()

@blueprint_painel_solicitacoes.route('/download-relatorio', methods=['GET'])
@login_required
def download_relatorio():
    try:
        cursor, conn = abrir_cursor()
        sql = """
        SELECT
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            u.LOGIN AS USUARIO_SOLICITANTE,
            d.DEPARTAMENTO AS DEPARTAMENTO_CODIGO,
            d.NOME AS DEPARTAMENTO_DESCRICAO,
            s.VALOR,
            s.STATUS
        FROM
            LIU_SOLICITACOES s
        JOIN
            GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
        JOIN
            GER_USUARIO u on s.USUARIO_SOLICITANTE = u.USUARIO
    """   
        cursor.execute(sql)

        dados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]

        dia_atual = date.today()
        dia_formatado = dia_atual.strftime("%d_%m_%Y")

        caminho = f"static/relatorios/relatorio_solicitacoes_{dia_formatado}.xlsx"

        gerar_relatorio(dados, colunas, caminho)

        return send_file(caminho, as_attachment=True)
    
    except Exception as e:
            flash(f'Erro na consulta: {e}', 'error')
            logging.error(f"Erro na consulta: {e}")
            return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
    finally:
        cursor.close()
        conn.close()

@blueprint_painel_solicitacoes.route('mais_info_sol/<int:id>/download-pdf', methods=['GET'])
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
            novo_descricao = request.form.get('descricao').strip()
            novo_valor = float(request.form.get('valor').replace('R$', '').replace('.', '').replace(',', '.').strip())
            
            if len(novo_departamento) != 3:
                    flash('O departamento deve ter exatamente 3 caracteres!')
                    return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
            else:
                try:
                    cursor, conn = abrir_cursor()
                    sql = """
                            UPDATE 
                                LIU_SOLICITACOES
                            SET 
                                DEPARTAMENTO = :1,
                                DESCRICAO = :2,
                                VALOR = :3 
                            WHERE 
                                ID = :4
                            """
                    valores = [novo_departamento, novo_descricao, novo_valor, id]
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
                logging.info('Solicitação excluida com sucesso!')
                flash('Solitação excluida com sucesso!', 'success')

                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
            except Exception as e:
                logging.info(e)                
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
                    valores = [
                        'PENDENTE',
                        id
                        ]
                    cursor.execute(sql, valores)
                    conn.commit()
                    return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                except Exception as e:
                    flash(f'Erro na consulta: {e}', 'error')
                    logging.info(e)
                    return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                finally:
                    cursor.close()
                    conn.close()

@blueprint_painel_solicitacoes.route('mais_info_sol/<int:id>/desautorizar', methods=['POST'])
@login_required
def desautorizar_solicitacao(id):
    try:
        cursor, conn = abrir_cursor()
        sql_solicitacao = "SELECT ID, NRO_PROCESSO FROM LIU_SOLICITACOES WHERE ID = :1"
        valores_solicitacao = [id]
        cursor.execute(sql_solicitacao, valores_solicitacao)
        retorno_solicitacao = cursor.dict_fetchone()
        logging.info(f'Select da solicitação atual feito. NRO_PROCESSO: {retorno_solicitacao['nro_processo']}')

        sql_deletar = "DELETE FROM FAT_PROCESSO_DESPESA WHERE NRO_PROCESSO = :1"
        valores_deletar = [retorno_solicitacao['nro_processo']]
        cursor.execute(sql_deletar, valores_deletar)
        conn.commit()
        logging.info('Solicitação excluida no FAT_PROCESSO_DESPESA')

        sql_update = "UPDATE LIU_SOLICITACOES SET STATUS = :1, NRO_PROCESSO = :2, USUARIO_AUTORIZANTE = :3 WHERE ID = :4"
        valores_update = ['PENDENTE', None, None, id]
        cursor.execute(sql_update, valores_update)
        conn.commit()
        logging.info('Solicitação alterada para STATUS PENDENTE, NRO_PROCESSO NULL e USUARIO_AUTORIZANTE NULL')

        pdf_path = os.path.join('static', 'pdf', f'solicitacao_{id}.pdf')
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            logging.info(f'PDF removido: {pdf_path}')
        else:
            logging.info(f'PDF não encontrado para remoção: {pdf_path}')

        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
    except Exception as e:
        logging.info(e)
        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
    finally:
        cursor.close()
        conn.close()
