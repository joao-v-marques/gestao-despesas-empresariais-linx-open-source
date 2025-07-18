from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor
import logging

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

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

    try:
        valor_float = float(valor_form.replace('R$', ''))
    except ValueError:
        flash('O valor inserido é inválido!', 'error')
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
        try:
            cursor, conn = abrir_cursor()
            sql = "INSERT INTO LIU_SOLICITACOES (EMPRESA, REVENDA, USUARIO_SOLICITANTE, DEPARTAMENTO, DESCRICAO, VALOR, FORNECEDOR, STATUS, MOTIVO_REPROVA, PDF_PATH) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"
            valores = [
                empresa_form,
                revenda_form,
                current_user.CODIGO_APOLLO,
                departamento_form,
                descricao_form,
                valor_float,
                fornecedor_form,
                'PENDENTE',
                '',
                ''
                ]
            cursor.execute(sql, valores)
            conn.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao', usuario_logado=current_user.USUARIO))
        except Exception as e:
                flash(f'Erro interno ao realizar a consulta: {e}', 'error')
                return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
        finally:
                cursor.close()
                conn.close()
    
