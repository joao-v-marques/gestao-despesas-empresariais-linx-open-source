from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor
from datetime import datetime
from decorators import role_required
import logging

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

# Rota que renderiza o HTML da pagina
@blueprint_lancar_solicitacao.route('/')
@role_required('Administrador', 'Gerente', 'Corporativo', 'Solicitante')
@login_required
def lancar_solicitacao():
    lista_departamentos = [100, 200, 300, 400, 500, 600]

    # ! Cria placeholders dinamicos dentro da lista [:1, :2, :3 ...]
    placeholders_lista = ", ".join([f":{i+3}" for i in range(len(lista_departamentos))])

    try:
        cursor, conn = abrir_cursor()
        sql_departamento = f"SELECT CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1 AND CAMPO = :2 AND CAMPO3 IN ({placeholders_lista}) ORDER BY CAMPO"
        valores = [
            current_user.EMPRESA,
            current_user.REVENDA
        ] + lista_departamentos
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
@role_required('Administrador', 'Gerente', 'Corporativo', 'Solicitante')
@login_required
def buscar_origens():
    empresa = int(request.args.get('empresa'))
    revenda = int(request.args.get('revenda'))
    try:
        cursor, conn = abrir_cursor()
        sql_origem = "SELECT CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1 AND CAMPO = :2 AND CAMPO = :3 AND CAMPO != :4"
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
@role_required('Administrador', 'Gerente', 'Corporativo', 'Solicitante')
@login_required
def busca_fornecedor(codigo):
    try:
        cursor, conn = abrir_cursor()
        sql_busca_fornecedor = "SELECT CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1" 
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
@role_required('Administrador', 'Gerente', 'Corporativo', 'Solicitante')
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
        sql_orcamento = "SELECT CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1 AND CAMPO = :2 AND CAMPO = :3 AND CAMPO = :4 AND CAMPO = :5"
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
@role_required('Administrador', 'Gerente', 'Corporativo', 'Solicitante')
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
            sql_os = "SELECT * FROM SCHEMA.TABELA WHERE CAMPO = :1 AND CAMPO = :2 AND CAMPO = :3"
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

    if valor_orcamento <= valor_float:
        alcada = "Corporativo"
    else:
        alcada = "Gerente"

    logging.info(f"Origem: {origem_form}")

    # Insert final
    try:
        cursor, conn = abrir_cursor()
        # Validacao = Se a origem do codigo for 5121 não devemos mexer nos orcamentos (Pois nao existe)
        if origem_form != "5121":
            # Ano e mes utilizado na SELECT dos orcamentos
            ano_mes = datetime.now().strftime("%Y%m")

            # SELECT nos orcamentos que retorna apenas o valor para calcular
            sql_val_orcamento = "SELECT VALOR FROM SCHEMA.TABELA WHERE CAMPO = :1 AND CAMPO = :2 AND CAMPO = :3 AND CAMPO = :4 AND CAMPO = :5"
            valores_val_orcamento = [
                empresa_form,
                revenda_form,
                origem_form,
                ano_mes,
                departamento_form
            ]
            cursor.execute(sql_val_orcamento, valores_val_orcamento)
            retorno_val_orcamento = cursor.dict_fetchone()

            if retorno_val_orcamento:
                # Declarando o novo valor do orçamento: novo_valor = valor_origem - valor_solicitação
                novo_valor_orcamento = retorno_val_orcamento['valor'] - valor_float

                # Fazer um UPDATE nos orcamentos com esse novo valor
                sql_update_orcamento = "UPDATE SCHEMA.TABELA SET CAMPO = :1 WHERE CAMPO = :2 AND CAMPO = :3 AND CAMPO = :4 AND CAMPO = :5 AND CAMPO = :6"
                valores_update_orcamento = [
                    novo_valor_orcamento,
                    empresa_form,
                    revenda_form,
                    origem_form,
                    ano_mes,
                    departamento_form
                ]
                cursor.execute(sql_update_orcamento, valores_update_orcamento)
            else:
                logging.error("Não foi localizado registro de orçamento para atualizar!")
        else:
            logging.error(f"Origem {origem_form} ignorada na atualização do orçamento")

        sql = """INSERT INTO SCHEMA.TABELA
                 (CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, 
                  CAMPO, CAMPO, CAMPO, CAMPO, 
                  CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO)
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