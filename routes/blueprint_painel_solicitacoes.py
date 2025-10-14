import logging, os
from io import BytesIO
from datetime import date
from gerar_relatorio import gerar_relatorio
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor
from datetime import datetime

blueprint_painel_solicitacoes = Blueprint('blueprint_painel_solicitacoes', __name__)

# Rota que renderiza a pagina do painel de solicitações
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
        s.CAMPO,
        s.CAMPO,
        s.CAMPO,
        s.CAMPO,
        s.CAMPO,
        s.CAMPO, 
        s.CAMPO,
        s.CAMPO,
        s.CAMPO,
        s.CAMPO,
        s.CAMPO,
        s.CAMPO,
        u.CAMPO AS CAMPO,
        d.CAMPO AS CAMPO,
        d.CAMPO AS CAMPO
    FROM 
        SCHEMA.TABELA s
        LEFT JOIN SCHEMA.TABELA d ON s.CAMPO = d.CAMPO
        LEFT JOIN SCHEMA.TABELA u ON s.CAMPO = u.CAMPO
"""
                
            if filtro != 'TODOS':
                sql = base_sql + " WHERE s.CAMPO = :1 AND s.CAMPO = :2"
                valores = [filtro, current_user.CODIGO_APOLLO]
            else:
                sql = base_sql + " WHERE s.CAMPO = :1"
                valores = [current_user.CODIGO_APOLLO]

            colunas_permitidas = [  
                'ID', 'NRO_PROCESSO', 'EMPRESA', 'REVENDA', 'USUARIO_SOLICITANTE', 'DEPARTAMENTO_CODIGO', 'DEPARTAMENTO_DESCRICAO', 'VALOR', 'STATUS', 'FORNECEDOR', 'NRO_OS', 'DATA_APROVACAO', 'DATA_SOLICITACAO', 'DATA_ENCERRAMENTO'
            ]

            if sort_by not in colunas_permitidas:
                   sort_by = 'ID'
            if sort_dir not in ['ASC', 'DESC']:
                   sort_dir = 'ASC'

            sql += f"ORDER BY {sort_by} {sort_dir}"

            cursor.execute(sql, valores)
            retorno = cursor.dict_fetchall()

            return render_template('painel_solicitacoes.html', solicitacoes=retorno, filtro=filtro, usuario_logado=current_user.USUARIO, sort_by=sort_by, sort_dir=sort_dir)
        except Exception as e:
                flash(f'Erro ao realizar a consulta: {e}', 'error')
                logging.error(f'erro: {e}')
                return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
        finally:
                cursor.close()
                conn.close()

# Rota que direciona para a pagina de mais_info_sol (Mais informações das solicitações)
@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>')
@login_required
def mais_info_sol(id):
        try:
            cursor, conn = abrir_cursor()
            sql_solicitacao = """SELECT
                                    s.CAMPO,
                                    s.CAMPO,
                                    s.CAMPO,
                                    s.CAMPO,
                                    s.CAMPO,
                                    s.CAMPO,
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
                                    s.CAMPO AS CAMPO,
                                    o.CAMPO AS CAMPO,
                                    o.CAMPO AS CAMPO
                                FROM
                                    SCHEMA.TABELA s
                                LEFT JOIN 
                                    SCHEMA.TABELA d ON s.CAMPO = d.CAMPO
                                LEFT JOIN
                                    SCHEMA.TABELA u on s.CAMPO = u.CAMPO
                                LEFT JOIN
                                    SCHEMA.TABELA o ON s.CAMPO = o.CAMPO
                                WHERE 
                                    CAMPO = :1
                                    """
            cursor.execute(sql_solicitacao, [id])
            retorno_solicitacao = cursor.dict_fetchone()

            lista_departamentos = [100, 200, 300, 400, 500, 600]

            # ! Cria placeholders dinamicos dentro da lista [:1, :2, :3 ...]
            placeholders_lista = ", ".join([f":{i+1}" for i in range(len(lista_departamentos))])
                
            sql_departamento = f"SELECT DISTINCT CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO IN ({placeholders_lista}) ORDER BY CAMPO"
            cursor.execute(sql_departamento)
            retorno_departamento = cursor.dict_fetchall()

            sql_origem = "SELECT DISTINCT CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1 AND CAMPO = :2 AND CAMPO = 'N' AND CAMPO != 'LIVRE'"
            valores_origem = [
                retorno_solicitacao['empresa'],
                retorno_solicitacao['revenda']
            ]
            cursor.execute(sql_origem, valores_origem)
            retorno_origem = cursor.dict_fetchall()

            sql_autorizante = "SELECT CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1"
            valores_autorizante = [retorno_solicitacao['usuario_autorizante']]
            cursor.execute(sql_autorizante, valores_autorizante)
            retorno_autorizante = cursor.dict_fetchone()

            return render_template('mais_info_sol.html', usuario_logado=current_user.USUARIO, solicitacao=retorno_solicitacao, departamento=retorno_departamento, origem=retorno_origem, usuario_autorizante=retorno_autorizante)
        except Exception as e:
                flash(f'Erro interno ao realizar a consulta: {e}', 'error')
                logging.info(f'{e}')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
                cursor.close()
                conn.close()

# Rota que atualiza os fornecedores (Não é a rota para inserir um novo fornecedor no sistema)
@blueprint_painel_solicitacoes.route('/inserir-fornecedor/<int:id>', methods=['POST'])
@login_required
def inserir_fornecedor(id):
    session.pop('_flashes', None)
    cod_fornecedor = request.form['inserir-fornecedor-modal'].strip()
    desc_fornecedor = request.form['desc-inserir-fornecedor-modal'].strip()

    if desc_fornecedor == 'Erro na busca':
        logging.error('Você inseriu um fornecedor inválido!')
        flash('Você inseriu um fornecedor inválido!', 'error')
        return redirect(url_for("blueprint_painel_solicitacoes.mais_info_sol", id=id))
    elif desc_fornecedor == 'Fornecedor não encontrado':
        logging.error('Você inseriu um fornecedor inválido!')
        flash('Você inseriu um fornecedor inválido!', 'error')
        return redirect(url_for("blueprint_painel_solicitacoes.mais_info_sol", id=id))
    else:
        try:
            cursor, conn = abrir_cursor()
            sql = "UPDATE SCHEMA.TABELA SET CAMPO = :1 WHERE CAMPO = :2"
            valores = [cod_fornecedor, id]
            cursor.execute(sql, valores)
            conn.commit()

            flash('Fornecedor inserido com sucesso!', 'success')

            return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erro interno ao realizar a consulta: {e}', 'error')
            logging.error(f'{e}')
            return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
            cursor.close()
            conn.close()

# Rota para baixar um relatório do painel de solicitações
@blueprint_painel_solicitacoes.route('/download-relatorio', methods=['GET'])
@login_required
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
            sql += "WHERE s.CAMPO = :1 AND s.CAMPO = :2"
            valores = [filtro, current_user.CODIGO_APOLLO]
        else:
            sql += "WHERE s.CAMPO = :1"
            valores = [current_user.CODIGO_APOLLO]
        
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
            logging.error(f"Erro na consulta: {e}")
            return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
    finally:
        cursor.close()
        conn.close()

# Rota para baixar o PDF de comprovante para solicitações aprovadas
@blueprint_painel_solicitacoes.route('mais_info_sol/<int:id>/download-pdf', methods=['GET'])
@login_required
def download_pdf(id):
        try:
            cursor, conn = abrir_cursor()
            sql = "SELECT CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1"
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

# Rota para editar uma solicitação
@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/salvar', methods=['POST'])
@login_required
def salvar_edicao(id):
            novo_departamento = request.form['departamento']
            novo_origem = request.form['origem']
            novo_descricao = request.form.get('descricao').strip()
            novo_valor = float(request.form.get('valor').replace('R$', '').replace('.', '').replace(',', '.').strip())
                        
            if len(novo_departamento) != 3:
                flash('O departamento deve ter exatamente 3 caracteres!')
                return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
            elif len(novo_origem) != 4:
                flash('A origem deve ter exatamente 3 caracteres!')
                return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
            else:
                try:
                    cursor, conn = abrir_cursor()
                    sql = """
                            UPDATE 
                                SCHEMA.TABELA
                            SET 
                                CAMPO = :1,
                                CAMPO = :2,
                                CAMPO = :3,
                                CAMPO = :4 
                            WHERE 
                                CAMPO = :5
                            """
                    valores = [novo_departamento, novo_descricao, novo_valor, novo_origem, id]
                    cursor.execute(sql, valores)
                    conn.commit()
                    flash('Alteração realizada com sucesso!', 'success')
                    return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
                except Exception as e:
                    conn.rollback()
                    flash(f'Erro ao salvar edição: {e}', 'error')
                    return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))
                finally:
                    cursor.close()
                    conn.close()
        
# Rota para excluir uma solicitação
@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_solicitacao(id):
            try:
                cursor, conn = abrir_cursor()

                sql_solicitacao = "SELECT ID, NRO_PROCESSO, EMPRESA, REVENDA, ORIGEM, VALOR, DATA_SOLICITACAO, DEPARTAMENTO FROM LIU.LIU_SOLICITACOES WHERE ID = :1"
                cursor.execute(sql_solicitacao, [id])
                retorno_solicitacao = cursor.dict_fetchone()

                if retorno_solicitacao['origem'] != 5121:
                    # Ano e mes utilizado na SELECT dos orcamentos
                    data_solicitacao = retorno_solicitacao['data_solicitacao']
                    data_obj = datetime.strptime(data_solicitacao, "%d/%m/%Y")
                    ano_mes = data_obj.strftime("%Y%m")

                    # SELECT nos orçamentos que retorna apenas o valor para calcular
                    sql_orcamento = "SELECT VALOR FROM LIU.GD_ORCAMENTO WHERE EMPRESA = :1 AND REVENDA = :2 AND ANO_MES = :3 AND ORIGEM = :4 AND CENTRO_CUSTO = :5"
                    valores_orcamento = [
                        retorno_solicitacao['empresa'],
                        retorno_solicitacao['revenda'],
                        ano_mes,
                        retorno_solicitacao['origem'],
                        retorno_solicitacao['departamento']
                    ]
                    cursor.execute(sql_orcamento, valores_orcamento)
                    retorno_orcamento = cursor.dict_fetchone()

                    if retorno_orcamento:
                        # Declarando o novo valor da origem: novo_valor = valor_origem + valor_solicitacao (Agora é adição pois está devolvendo)
                        novo_valor = retorno_orcamento['valor'] + retorno_solicitacao['valor']

                        # Fazer um UPDATE nos orcamentos com esse novo valor
                        update_orcamento = "UPDATE LIU.GD_ORCAMENTO SET VALOR = :1 WHERE EMPRESA = :2 AND REVENDA = :3 AND ANO_MES = :4 AND ORIGEM = :5 AND CENTRO_CUSTO = :6"
                        valores_update_orcamento = [
                            novo_valor,
                            retorno_solicitacao['empresa'],
                            retorno_solicitacao['revenda'],
                            ano_mes,
                            retorno_solicitacao['origem'],
                            retorno_solicitacao['departamento']
                        ]
                        cursor.execute(update_orcamento, valores_update_orcamento)
                    else:
                        logging.error("Não foi localizado registro de orçamento para atualizar.")
                else:
                    logging.error(f"Origem {retorno_solicitacao['origem']} ignorada na atualização do orçamento")

                sql = "DELETE FROM SCHEMA.TABELA WHERE CAMPO = :1"
                cursor.execute(sql, [id])
                flash('Solitação excluida com sucesso!', 'success')

                conn.commit()

                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
            except Exception as e:
                conn.rollback()
                logging.info(e)
                flash(f"Erro ao excluir solicitação: {e}", "error")        
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
            finally:
                cursor.close()
                conn.close()

# Rota para reenviar uma solicitação reprovada
@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/reenviar', methods=['POST'])
@login_required
def reenviar_solicitacao(id):
                try:
                    cursor, conn = abrir_cursor()

                    sql = "UPDATE SCHEMA.TABELA SET CAMPO = :1, CAMPO = :2 WHERE CAMPO = :3"
                    valores = [
                        'PENDENTE',
                        None,
                        id
                        ]
                    cursor.execute(sql, valores)
                    conn.commit()
                    return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                except Exception as e:
                    conn.rollback()
                    flash(f'Erro na consulta: {e}', 'error')
                    logging.info(e)
                    return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                finally:
                    cursor.close()
                    conn.close()

# Rota para desautorizar uma solicitação aprovada
@blueprint_painel_solicitacoes.route('mais_info_sol/<int:id>/desautorizar', methods=['POST'])
@login_required
def desautorizar_solicitacao(id):
    try:
        cursor, conn = abrir_cursor()
        sql_solicitacao = "SELECT CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1"
        valores_solicitacao = [id]
        cursor.execute(sql_solicitacao, valores_solicitacao)
        retorno_solicitacao = cursor.dict_fetchone()

        sql_deletar = "DELETE FROM SCHEMA.TABELA WHERE CAMPO = :1"
        valores_deletar = [retorno_solicitacao['nro_processo']]
        cursor.execute(sql_deletar, valores_deletar)

        sql_update = "UPDATE SCHEMA.TABELA SET CAMPO = :1, CAMPO = :2, CAMPO = :3, CAMPO = :4 WHERE CAMPO = :5"
        valores_update = ['PENDENTE', None, None, None, id]
        cursor.execute(sql_update, valores_update)

        conn.commit() # Apenas 1 commit para todas as alterações, assim fazendo com que o conn.rollback funcione corretamente

        pdf_path = os.path.join('static', 'pdf', f'solicitacao_{id}.pdf')
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            logging.info(f'PDF removido: {pdf_path}')
        else:
            logging.info(f'PDF não encontrado para remoção: {pdf_path}')

        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
    except Exception as e:
        conn.rollback()
        logging.info(f"Erro: {e}")
        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
    finally:
        cursor.close()
        conn.close()