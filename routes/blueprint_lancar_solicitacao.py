from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor
from datetime import datetime
from decorators import role_required
import logging

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

# Rota que renderiza o HTML da pagina
@blueprint_lancar_solicitacao.route('/')
@role_required('Administrador', 'Gerente', 'Diretoria', 'Solicitante')
@login_required
def lancar_solicitacao():
    try:
        cursor, conn = abrir_cursor()
        sql_departamento = "SELECT DEPARTAMENTO, NOME FROM PONTAL.GER_DEPARTAMENTO WHERE EMPRESA = :1 AND REVENDA = :2 ORDER BY DEPARTAMENTO"
        valores = [
            current_user.EMPRESA,
            current_user.REVENDA
        ]
        cursor.execute(sql_departamento, valores)
        retorno_departamento = cursor.dict_fetchall()

        return render_template('lancar_solicitacao.html', usuario_logado=current_user.USUARIO, departamento=retorno_departamento)
    except Exception as e:
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        logging.error(f'Erro: {e}')
        return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
    finally:
        cursor.close()
        conn.close()

# Rota que fica constantemente atualizando as Origens utilizando Javascript
@blueprint_lancar_solicitacao.route('/buscar-origens')
@role_required('Administrador', 'Gerente', 'Diretoria', 'Solicitante')
@login_required
def buscar_origens():
    empresa = int(request.args.get('empresa'))
    revenda = int(request.args.get('revenda'))
    try:
        cursor, conn = abrir_cursor()
        sql_origem = "SELECT ORIGEM, DES_ORIGEM FROM PONTAL.FIN_ORIGEM WHERE EMPRESA = :1 AND REVENDA = :2 AND UTILIZACAO = :3 AND DES_ORIGEM != :4"
        valores = [
            empresa,
            revenda,
            'N',
            'LIVRE'
        ]
        cursor.execute(sql_origem, valores)
        retorno = cursor.dict_fetchall()
        return jsonify(retorno)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Rota que fica constantemente atualizando o Fornecedor utilizando Javascript
@blueprint_lancar_solicitacao.route('/fornecedor/<int:codigo>')
@role_required('Administrador', 'Gerente', 'Diretoria', 'Solicitante')
@login_required
def busca_fornecedor(codigo):
    try:
        cursor, conn = abrir_cursor()
        sql_busca_fornecedor = "SELECT NOME FROM PONTAL.FAT_CLIENTE WHERE CLIENTE = :1" 
        cursor.execute(sql_busca_fornecedor, [codigo])
        retorno = cursor.dict_fetchone()
        conn.close()

        if retorno:
            return jsonify(retorno)
        else:
            return jsonify({"NOME": None}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@blueprint_lancar_solicitacao.route('/fazer-lancamento/confirm', methods=['GET', 'POST'])
@role_required('Administrador', 'Gerente', 'Diretoria', 'Solicitante')
@login_required
def consulta_orcamento():
    dados_form = request.get_json() # Lê o corpo da requisição como JSON
    empresa_form = dados_form.get('empresa_form')
    revenda_form = dados_form.get('revenda_form')
    departamento_form = dados_form.get('departamento_form')
    origem_form = dados_form.get('origem_form')
    ano_mes = datetime.now().strftime("%Y%m")

    try:
        cursor, conn = abrir_cursor()
        sql_orcamento = "SELECT VALOR FROM LIU.GD_ORCAMENTO WHERE EMPRESA = :1 AND REVENDA = :2 AND CENTRO_CUSTO = :3 AND ORIGEM = :4 AND ANO_MES = :5"
        valores_orcamento = [
            empresa_form,
            revenda_form,
            departamento_form,
            origem_form,
            ano_mes
        ]
        cursor.execute(sql_orcamento, valores_orcamento)
        retorno_orcamento = cursor.dict_fetchall()

        session['retorno_orcamento'] = retorno_orcamento[0]["valor"] if retorno_orcamento else None

        if retorno_orcamento:
            return jsonify(retorno_orcamento)
        else:
            return jsonify({"erro": None}), 404
    except Exception as e:
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        return jsonify({"erro": None}), 404
    finally:
        cursor.close()
        conn.close()

# Função que adiciona funcionalidade ao botão de cadastrar
@blueprint_lancar_solicitacao.route('/fazer-lancamento', methods=['POST'])
@role_required('Administrador', 'Gerente', 'Diretoria', 'Solicitante')
@login_required
def fazer_lancamento():
    empresa_form = request.form['empresa']
    revenda_form = request.form['revenda']
    departamento_form = request.form['departamento'].strip()
    descricao_form = request.form['descricao'].strip()
    valor_form = request.form['valor']
    fornecedor_form = request.form['fornecedor'].strip()
    desc_fornecedor_form = request.form['desc-fornecedor'].strip()
    data_atual = datetime.now().strftime("%d/%m/%Y")
    origem_form = request.form['origem'].strip()
    retorno_orcamento = session.get('retorno_orcamento')
    if not retorno_orcamento:
        valor_orcamento = 1
    else:
        valor_orcamento = session.get('retorno_orcamento')    
    nro_os_form = request.form['nroOS']
    
    if valor_orcamento == 1:
        try:
            cursor, conn = abrir_cursor()
            sql_os = "SELECT * FROM PONTAL.OFI_ORDEM_SERVICO WHERE EMPRESA = :1 AND REVENDA = :2 AND NRO_OS = :3"
            cursor.execute(sql_os, [empresa_form, revenda_form, nro_os_form])
            retorno_os = cursor.fetchone()
        except Exception as e:
            flash(f"Erro ao realizar consulta: {e}", "error")
            logging.info("Erro ao realizar consulta!")
            return redirect(url_for("blueprint_lancar_solicitacao.lancar_solicitacao"))
        finally:
            cursor.close()
            conn.close()

        if not retorno_os:
            flash("Erro: A O.S inserida não existe no sistema!", "error")
            logging.info("Atenção: A O.S inserida não existe no sistema!", "error")
            return redirect(url_for("blueprint_lancar_solicitacao.lancar_solicitacao"))

    # Conversão de valor
    try:
        valor_float = valor_form.replace('\xa0', '').replace('.', '').replace(',', '.').replace('R$', '')
        valor_float = float(valor_float)
    except ValueError as error:
        flash('O valor inserido é inválido!', 'error')
        logging.error(f"O valor inserido é inválido! ERRO: {error}")
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))

    # Validações comuns
    if not descricao_form or not valor_form:
        flash('Nenhum campo pode estar vazio!', 'error')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
    if desc_fornecedor_form in ('Erro na busca', 'Fornecedor não encontrado'):
        logging.error('Você inseriu um fornecedor inválido!')
        flash('Você inseriu um fornecedor inválido!', 'error')
        return redirect(url_for("blueprint_lancar_solicitacao.lancar_solicitacao"))

    alcada = "Diretoria" if valor_orcamento <= 0 else "Gerente"

    logging.info(f"Origem: {origem_form}")

    # Insert final
    try:
        cursor, conn = abrir_cursor()
        sql = """INSERT INTO LIU.LIU_SOLICITACOES 
                 (EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, DESCRICAO, 
                  VALOR, STATUS, DATA_SOLICITACAO, MOTIVO_REPROVA, 
                  PDF_PATH, ORIGEM, ORCAMENTO, ALCADA, NRO_OS, FORNECEDOR)
                 VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15)"""
        valores = [
            int(empresa_form),
            int(revenda_form),
            int(current_user.CODIGO_APOLLO),
            int(departamento_form),
            descricao_form,
            valor_float,
            'PENDENTE',
            data_atual,
            '',
            '',
            int(origem_form),
            valor_orcamento,
            alcada,
            nro_os_form
        ]
        if fornecedor_form:
            valores.append(int(fornecedor_form))
        else:
            valores.append(fornecedor_form)
        cursor.execute(sql, valores)
        conn.commit()
        session.pop('retorno_orcamento', None)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao', usuario_logado=current_user.USUARIO))
    except Exception as e:
        conn.rollback()
        flash(f'Erro interno ao realizar o cadastro: {e}', 'error')
        logging.error(f'Erro interno ao realizar a cadastro: {e}')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
    finally:
        cursor.close()
        conn.close()
