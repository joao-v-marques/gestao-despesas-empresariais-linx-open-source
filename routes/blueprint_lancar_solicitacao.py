from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor
from datetime import datetime
import logging

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

# Rota que renderiza o HTML da pagina
@blueprint_lancar_solicitacao.route('/')
@login_required
def lancar_solicitacao():
    try:
        cursor, conn = abrir_cursor()
        sql_departamento = "SELECT DEPARTAMENTO, NOME FROM GER_DEPARTAMENTO WHERE EMPRESA = :1 AND REVENDA = :2 ORDER BY DEPARTAMENTO"
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
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))    
    finally:
        cursor.close()
        conn.close()

# Rota que fica constantemente atualizando as Origens utilizando Javascript
@blueprint_lancar_solicitacao.route('/buscar-origens')
@login_required
def buscar_origens():
    empresa = int(request.args.get('empresa'))
    revenda = int(request.args.get('revenda'))
    try:
        cursor, conn = abrir_cursor()
        sql_origem = "SELECT ORIGEM, DES_ORIGEM FROM FIN_ORIGEM WHERE EMPRESA = :1 AND REVENDA = :2 AND UTILIZACAO = :3 AND DES_ORIGEM != :4"
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
@login_required
def busca_fornecedor(codigo):
    try:
        cursor, conn = abrir_cursor()
        sql_busca_fornecedor = "SELECT NOME FROM FAT_CLIENTE WHERE CLIENTE = :1" 
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

    try:
        valor_float = valor_form.replace('\xa0', '').replace('.', '').replace(',', '.').replace('R$', '')
    except ValueError as error:
        flash('O valor inserido é inválido!', 'error')
        logging.error(f"O valor inserido é inválido! ERRO: {error}")
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
    

    if not descricao_form or not valor_form:
        flash('Nenhum campo pode estar vazio!', 'error')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
    elif desc_fornecedor_form == 'Erro na busca':
        logging.error('Você inseriu um fornecedor inválido!')
        flash('Você inseriu um fornecedor inválido!', 'error')
        return redirect(url_for("blueprint_lancar_solicitacao.lancar_solicitacao"))
    elif desc_fornecedor_form == 'Fornecedor não encontrado':
        logging.error('Você inseriu um fornecedor inválido!')
        flash('Você inseriu um fornecedor inválido!', 'error')
        return redirect(url_for("blueprint_lancar_solicitacao.lancar_solicitacao"))
    else:
        logging.info(f"Valor Orçamento: {valor_orcamento} <<<>>> Tipo: {type(valor_orcamento)}")
        if valor_orcamento <= 0:
            alcada = "Diretoria"
        else:
            alcada = "Gerente"

        try:
            cursor, conn = abrir_cursor()
            sql = "INSERT INTO LIU_SOLICITACOES (EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, DESCRICAO, VALOR, FORNECEDOR, STATUS, DATA_SOLICITACAO, MOTIVO_REPROVA, PDF_PATH, ORIGEM, ORCAMENTO, ALCADA, NRO_OS) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)"
            valores = [
                int(empresa_form),
                int(revenda_form),
                int(current_user.CODIGO_APOLLO),
                int(departamento_form),
                descricao_form,
                float(valor_float),
                int(fornecedor_form),
                'PENDENTE',
                data_atual,
                '',
                '',
                int(origem_form),
                valor_orcamento,
                alcada,
                nro_os_form
                ]
            cursor.execute(sql, valores)
            conn.commit()
            session.pop('retorno_orcamento', None)
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao', usuario_logado=current_user.USUARIO, ))
        except Exception as e:
                flash(f'Erro interno ao realizar a o cadastro: {e}', 'error')
                logging.error(f'Erro interno ao realizar a cadastro: {e}')
                return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
        finally:
                cursor.close()
                conn.close()