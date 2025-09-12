from flask import Blueprint, render_template, redirect, url_for, request, flash 
from flask_login import login_required, current_user
from decorators import role_required
from gerar_pdf import gerar_pdf
from database.connect_db import abrir_cursor
from datetime import datetime
import logging

blueprint_aprovacoes = Blueprint('blueprint_aprovacoes', __name__)

# Rota que renderiza a pagina
@blueprint_aprovacoes.route('/')
@login_required
@role_required('Administrador', 'Gerente', 'Diretoria')
def aprovacoes():
    try:
        cursor, conn = abrir_cursor()
        sql = """
        SELECT DISTINCT
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO AS CAMPO,
            s.CAMPO AS CAMPO,
            s.CAMPO AS CAMPO,
            s.CAMPO,
            s.CAMPO,
            s.CAMPO
        FROM
            SCHEMA.TABELA s
        JOIN 
            SCHEMA.TABELA d ON s.CAMPO = d.CAMPO
        JOIN
            SCHEMA.TABELA u on s.CAMPO = u.CAMPO
        WHERE
            s.CAMPO = :1
        """
        if current_user.FUNCAO == 'Gerente':
            alcada = 'Gerente'
            sql += " AND s.CAMPO = :2"
            valores_sql = ['PENDENTE', alcada]
        elif current_user.FUNCAO == 'Diretoria':
            valores_sql = ['PENDENTE']
        elif current_user.FUNCAO == 'Administrador':
            valores_sql = ['PENDENTE']
        else:
            flash("Você não não pode visualizar essa tela!", 'error')
            logging.info("Você não não pode visualizar essa tela!")
            return redirect(url_for("blueprint_painel_solicitacoes.painel_solicitacoes"))
            
        cursor.execute(sql, valores_sql)
        retorno = cursor.dict_fetchall()

        return render_template('aprovacoes.html', query=retorno, usuario_logado=current_user.USUARIO)
    except Exception as e:    
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        logging.error(e)
        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
    finally:
        cursor.close()
        conn.close()

# Rota para abrir o mais_info_cd (O certo seria mais_info_aprov)
@blueprint_aprovacoes.route('/mais-info/<int:id>')
@login_required
@role_required('Administrador', 'Gerente', 'Diretoria')
def mais_info_cd(id):
    try:
        cursor, conn = abrir_cursor()
        sql = """
        SELECT 
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
            o.CAMPO AS CAMPO,
            o.CAMPO AS CAMPO,
            u.CAMPO AS CAMPO,
            d.CAMPO AS CAMPO,
            d.CAMPO AS CAMPO
        FROM 
            SCHEMA.TABELA s
        JOIN
            SCHEMA.TABELA o ON s.CAMPO = o.CAMPO
        JOIN 
            SCHEMA.TABELA d ON s.CAMPO = d.CAMPO
        JOIN
            SCHEMA.TABELA u on s.CAMPO = u.CAMPO
        WHERE 
            s.CAMPO = :1
        """
        cursor.execute(sql, [id])
        retorno = cursor.dict_fetchone()
        return render_template('mais_info_cd.html', usuario_logado=current_user.USUARIO, solicitacao=retorno)
    except Exception as e:
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        return redirect(url_for('blueprint_aprovacoes.aprovacoes'))
    finally:
        cursor.close()
        conn.close()

# Rota que altera o status para APROVADO ou PENDENTE
@blueprint_aprovacoes.route('/mudar-status/<int:id>', methods=['POST'])
@login_required
@role_required('Administrador', 'Gerente', 'Diretoria')
def mudar_status(id):
    novo_status = request.form['status']
    if novo_status == 'APROVADO':
        try:
            cursor, conn = abrir_cursor()
            sql_solicitacao = """
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
                d.CAMPO AS CAMPO,
                d.CAMPO AS CAMPO,
                u.CAMPO AS CAMPO,
                u.CAMPO AS CAMPO,
                u.CAMPO AS CAMPO,
                o.CAMPO AS CAMPO,
                o.CAMPO AS CAMPO
            FROM
                SHCEMA.TABELA s
                LEFT JOIN SCHEMA.TABELA d ON s.CAMPO = d.CAMPO
                LEFT JOIN SCHEMA.TABELA u ON s.CAMPO = u.CAMPO
                LEFT JOIN SCHEMA.TABELA o ON s.CAMPO = o.CAMPO 
            WHERE
                CAMPO = :1
            """
            cursor.execute(sql_solicitacao, [id])
            solicitacao = cursor.dict_fetchone()

            if not solicitacao['fornecedor']:
                logging.info('Você deve cadastrar um fornecedor antes de aprovar uma solicitação!')
                flash('Você deve cadastrar um fornecedor antes de aprovar uma solicitação!', 'error')
                return redirect(url_for('blueprint_aprovacoes.aprovacoes'))

            codFornecedor = str(solicitacao['fornecedor'])

            sql_fornecedor = "SELECT CAMPO, CAMPO, CAMPO FROM SHCEMA.TABELA WHERE CAMPO = :1"
            cursor.execute(sql_fornecedor, [codFornecedor])
            fornecedor = cursor.dict_fetchone()

            sql_nome_revenda = "SELECT CAMPO, CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1 AND CAMPO = :2"
            valores_nome_revenda = [solicitacao['empresa'], solicitacao['revenda']]
            cursor.execute(sql_nome_revenda, valores_nome_revenda)
            nome_revenda = cursor.dict_fetchone()

            if solicitacao['fornecedor'] == None or solicitacao['fornecedor'] == '':
                logging.info('Você deve cadastrar um fornecedor antes de aprovar uma solicitação!')
                flash('Você deve cadastrar um fornecedor antes de aprovar uma solicitação!', 'error')
                return redirect(url_for('blueprint_aprovacoes.aprovacoes'))
            else:
                pdf_path = gerar_pdf(solicitacao, fornecedor, str(fornecedor['cgccpf']), str(solicitacao['id']), nome_revenda)

                sql_max_processo = "SELECT MAX(CAMPO) FROM SCHEMA.TABELA"
                cursor.execute(sql_max_processo)
                max_processo = cursor.fetchone()[0]

                if max_processo is None:
                    proximo_numero_processo = 1
                else:
                    proximo_numero_processo = max_processo + 1

                sql_aprovado = "UPDATE SCHEMA.TABELA SET CAMPO = 'APROVADO', CAMPO = :1, CAMPO = :2, CAMPO = :3 WHERE CAMPO = :4"
                valores = [pdf_path, current_user.CODIGO_APOLLO, proximo_numero_processo, id]
                cursor.execute(sql_aprovado, valores)
                # Retirei um commit aqui para testar o conn.rollback()

                data_atual = datetime.now().replace(microsecond=0)

                sql_inserir = "INSERT INTO SHEMA.TABELA (CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)"
                valores_inserir = [
                    solicitacao['empresa'],
                    solicitacao['revenda'],
                    proximo_numero_processo,
                    data_atual,
                    f"{solicitacao['descricao']}. Aprovado por: {current_user.NOME}",
                    solicitacao['valor'],
                    'A',
                    solicitacao['cod_usuario_solicitante'],
                    solicitacao['departamento_codigo'],
                    current_user.CODIGO_APOLLO,
                    solicitacao['fornecedor']
                    ]
                cursor.execute(sql_inserir, valores_inserir)

                conn.commit()

                flash('Solicitação Aprovada e PDF gerado com sucesso!', 'success')
                return redirect(url_for('blueprint_aprovacoes.aprovacoes'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro interno ao realizar a aprovação: {e}', 'error')
            logging.error(f'Erro ao realizar a aprovação: {e}')
            return redirect(url_for('blueprint_aprovacoes.aprovacoes'))
        finally:
            cursor.close()
            conn.close()
    elif novo_status == 'REPROVADO':
        motivo_reprova = request.form['motivo_reprova']
        try:
            cursor, conn = abrir_cursor()
            sql = "UPDATE SHEMA.TABELA SET CAMPO = 'REPROVADO', CAMPO = :1 WHERE CAMPO = :2"
            valores = [motivo_reprova, id]
            cursor.execute(sql, valores)
            conn.commit()
            flash('Solicitação Reprovada!', 'success')
            return redirect(url_for('blueprint_aprovacoes.aprovacoes'))
        except Exception as e:
            conn.rollback()
            flash(f'Erro interno ao realizar a consulta: {e}', 'error')
            return redirect(url_for('blueprint_aprovacoes.mais_info_cd', id=id))
        finally:
            cursor.close()
            conn.close()
    else:
        logging.info('Status Inválido!')
        flash('Status inválido!', 'error')
        return redirect(url_for('blueprint_aprovacoes.aprovacoes'))
    
# Rota que atualiza os fornecedores (Não é a rota para inserir um novo fornecedor no sistema)
@blueprint_aprovacoes.route('/inserir-fornecedor/<int:id>', methods=['POST'])
@login_required
def inserir_fornecedor(id):
    cod_fornecedor = request.form['inserir-fornecedor-modal'].strip()
    desc_fornecedor = request.form['desc-inserir-fornecedor-modal'].strip()

    if desc_fornecedor == 'Erro na busca':
        flash('Você inseriu um fornecedor inválido!', 'error')
        return redirect(url_for("blueprint_aprovacoes.mais_info_cd", id=id))
    elif desc_fornecedor == 'Fornecedor não encontrado':
        flash('Você inseriu um fornecedor inválido!', 'error')
        return redirect(url_for("blueprint_aprovacoes.mais_info_cd", id=id))
    else:
        try:
            cursor, conn = abrir_cursor()
            sql = "UPDATE SCHEMA.TABELA SET CAMPO = :1 WHERE CAMPO = :2"
            valores = [cod_fornecedor, id]
            cursor.execute(sql, valores)
            conn.commit()

            flash('Fornecedor inserido com sucesso!', 'success')

            return redirect(url_for('blueprint_aprovacoes.mais_info_cd', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erro interno ao realizar a consulta: {e}', 'error')
            logging.error(f'{e}')
            return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
        finally:
            cursor.close()
            conn.close()