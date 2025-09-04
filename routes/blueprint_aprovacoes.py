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
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            s.NRO_OS,
            u.LOGIN AS USUARIO_SOLICITANTE,
            d.DEPARTAMENTO AS DEPARTAMENTO_CODIGO,
            d.NOME  AS DEPARTAMENTO_DESCRICAO,
            s.VALOR,
            s.STATUS,
            s.NRO_PROCESSO
        FROM
            LIU.LIU_SOLICITACOES s
        JOIN 
            PONTAL.GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
        JOIN
            PONTAL.GER_USUARIO u on s.USUARIO_SOLICITANTE = u.USUARIO
        WHERE
            s.STATUS = :1
        """
        if current_user.FUNCAO == 'Gerente':
            alcada = 'Gerente'
            sql += " AND s.ALCADA = :2"
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
            s.ID,
            s.EMPRESA,
            s.REVENDA,
            s.NRO_OS,
            u.LOGIN AS USUARIO_SOLICITANTE,
            d.DEPARTAMENTO AS DEPARTAMENTO,
            d.NOME AS NOME,
            s.DESCRICAO,
            s.VALOR,
            s.STATUS,
            s.FORNECEDOR,
            s.NRO_PROCESSO
        FROM 
            LIU.LIU_SOLICITACOES s
        JOIN 
            PONTAL.GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
        JOIN
            PONTAL.GER_USUARIO u on s.USUARIO_SOLICITANTE = u.USUARIO
        WHERE 
            s.ID = :1
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
                s.ID,
                s.EMPRESA,
                s.REVENDA,
                s.FORNECEDOR,
                s.DESCRICAO,
                s.VALOR,
                s.ORCAMENTO,
                s.NRO_OS,
                s.DATA_SOLICITACAO,
                d.DEPARTAMENTO AS DEPARTAMENTO_CODIGO,
                d.NOME AS DEPARTAMENTO_DESCRICAO,
                u.NOME AS NOM_USUARIO_SOLICITANTE,
                u.LOGIN AS USUARIO_SOLICITANTE,
                u.USUARIO AS COD_USUARIO_SOLICITANTE,
                o.ORIGEM AS ORIGEM_CODIGO,
                o.DES_ORIGEM AS ORIGEM_DESCRICAO
            FROM
                LIU.LIU_SOLICITACOES s
                LEFT JOIN PONTAL.GER_DEPARTAMENTO d ON s.DEPARTAMENTO = d.DEPARTAMENTO
                LEFT JOIN PONTAL.GER_USUARIO u ON s.USUARIO_SOLICITANTE = u.USUARIO
                LEFT JOIN PONTAL.FIN_ORIGEM o ON s.ORIGEM = o.ORIGEM 
            WHERE
                ID = :1
            """
            cursor.execute(sql_solicitacao, [id])
            solicitacao = cursor.dict_fetchone()

            codFornecedor = str(solicitacao['fornecedor'])

            sql_fornecedor = "SELECT CLIENTE, NOME, CGCCPF FROM PONTAL.FAT_CLIENTE WHERE CLIENTE = :1"
            cursor.execute(sql_fornecedor, [codFornecedor])
            fornecedor = cursor.dict_fetchone()

            sql_nome_revenda = "SELECT EMPRESA, REVENDA, NOME_FANTASIA FROM PONTAL.GER_REVENDA WHERE EMPRESA = :1 AND REVENDA = :2"
            valores_nome_revenda = [solicitacao['empresa'], solicitacao['revenda']]
            cursor.execute(sql_nome_revenda, valores_nome_revenda)
            nome_revenda = cursor.dict_fetchone()

            if solicitacao['fornecedor'] == None or solicitacao['fornecedor'] == '':
                logging.info('Você deve cadastrar um fornecedor antes de aprovar uma solicitação!')
                flash('Você deve cadastrar um fornecedor antes de aprovar uma solicitação!', 'error')
                return redirect(url_for('blueprint_aprovacoes.aprovacoes'))
            else:
                pdf_path = gerar_pdf(solicitacao, fornecedor, str(fornecedor['cgccpf']), str(solicitacao['id']), nome_revenda)

                sql_max_processo = "SELECT MAX(NRO_PROCESSO) FROM PONTAL.FAT_PROCESSO_DESPESA"
                cursor.execute(sql_max_processo)
                max_processo = cursor.fetchone()[0]

                if max_processo is None:
                    proximo_numero_processo = 1
                else:
                    proximo_numero_processo = max_processo + 1
                
                # Validacao = Se a origem do codigo for 5121 não devemos mexer nos orcamentos (Pois nao existe)
                if solicitacao['origem_codigo'] != 5121:
                    # Ano e mes utilizado na SELECT dos orcamentos
                    ano_mes = datetime.now().strftime("%Y%m")

                    # SELECT nos orcamentos que retorna apenas o valor para calcular
                    sql_origens = "SELECT VALOR FROM LIU.GD_ORCAMENTO WHERE EMPRESA = :1 AND REVENDA = :2 AND ORIGEM = :3 AND ANO_MES = :4 AND CENTRO_CUSTO = :5"
                    valores_origens = [solicitacao['empresa'], solicitacao['revenda'], solicitacao['origem_codigo'], ano_mes, solicitacao['departamento_codigo']]
                    cursor.execute(sql_origens, valores_origens)
                    retorno_origem = cursor.dict_fetchone()

                    if retorno_origem:
                        # Declarado o novo valor da origem: novo_valor = valor_origem - valor_solicitacao
                        novo_valor = retorno_origem['valor'] - solicitacao['valor']

                        # Fazer um UPDATE nos orcamentos com esse novo valor
                        sql_update_origens = "UPDATE LIU.GD_ORCAMENTO SET VALOR = :1 WHERE EMPRESA = :2 AND REVENDA = :3 AND ORIGEM = :4 AND ANO_MES = :5 AND CENTRO_CUSTO = :6"
                        valores_update_origens = [novo_valor, solicitacao['empresa'], solicitacao['revenda'], solicitacao['origem_codigo'], ano_mes, solicitacao['departamento_codigo']]
                        cursor.execute(sql_update_origens, valores_update_origens)
                        # Retirei um commit aqui para testar o conn.rollback()
                    else:
                        logging.error("Não foi localizado registro de orçamento para atualizar.")
                else:
                    logging.error(f"Origem {solicitacao['origem_codigo']} ignorada na atualização do orçamento")

                sql_aprovado = "UPDATE LIU.LIU_SOLICITACOES SET STATUS = 'APROVADO', PDF_PATH = :1, USUARIO_AUTORIZANTE = :2, NRO_PROCESSO = :3 WHERE ID = :4"
                valores = [pdf_path, current_user.CODIGO_APOLLO, proximo_numero_processo, id]
                cursor.execute(sql_aprovado, valores)
                # Retirei um commit aqui para testar o conn.rollback()

                data_atual = datetime.now().replace(microsecond=0)

                sql_inserir = "INSERT INTO PONTAL.FAT_PROCESSO_DESPESA (EMPRESA, REVENDA, NRO_PROCESSO, DTA_EMISSAO, DESCRICAO, VAL_PROCESSO, SITUACAO, USUARIO, DEPARTAMENTO, USUARIO_AUTORIZANTE, CLIENTE) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)"
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
            sql = "UPDATE LIU.LIU_SOLICITACOES SET STATUS = 'REPROVADO', MOTIVO_REPROVA = :1 WHERE ID = :2"
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