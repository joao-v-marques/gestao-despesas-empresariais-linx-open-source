from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from database.connect_db import abrir_cursor
import logging

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

@blueprint_lancar_solicitacao.route('/')
@login_required
def lancar_solicitacao():
    try:
        cursor, conn = abrir_cursor()
        sql_departamento = "SELECT * FROM LIU_DEPARTAMENTO ORDER BY CODIGO"
        cursor.execute(sql_departamento)
        retorno_departamento = cursor.fetchall()

        sql_tipo_despesa = "SELECT * FROM LIU_TIPO_DESPESA ORDER BY CODIGO"
        cursor.execute(sql_tipo_despesa)
        retorno_tipo_despesa = cursor.fetchall()

        return render_template('lancar_solicitacao.html', usuario_logado=current_user.USUARIO, departamento=retorno_departamento, tipo_despesa=retorno_tipo_despesa)
    except Exception as e:
                flash('Erro interno ao realizar a consulta!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))    
    finally:
            cursor.close()
            conn.close()

@blueprint_lancar_solicitacao.route('/fazer-lancamento', methods=['POST'])
@login_required
def fazer_lancamento():
    departamento_form = request.form['departamento']
    tipo_despesa_form = request.form['tipo_despesa']
    descricao_form = request.form['descricao']
    valor_form = request.form['valor']
    status_form = 'PENDENTE'

    try:
        valor_float = float(valor_form.replace('R$', ''))
    except ValueError:
        flash('O valor inserido é inválido!', 'error')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
    
    if not descricao_form or not valor_form:
        flash('Nenhum campo pode estar vazio!', 'error')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
    else:
        try:
            
             
              
         


    departamento_form = request.form['departamento']
    tipo_despesa_form = request.form['tipo_despesa']
    descricao_form = request.form['descricao']
    valor_form = request.form['valor']
    status_form = 'PENDENTE'

    try:
        valor_float = float(valor_form.replace('R$', ''))
    except ValueError:
        flash('O valor inserido é inválido! Tente novamente.', 'error')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))

    if not descricao_form or not valor_form:
        flash('Nenhum campo pode estar vazio! Tente novamente.', 'error')
        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao'))
    else:
        flash('Cadastro realizado com sucesso!', 'success')

        Solicitacoes.create(
            EMPRESA=request.form['empresa'],
            REVENDA=request.form['revenda'],
            USUARIO_SOLICITANTE = current_user.USUARIO,
            CODIGO_DEPARTAMENTO=departamento_form,
            CODIGO_TIPO_DESPESA=tipo_despesa_form,
            DESCRICAO=descricao_form.strip(),
            VALOR=valor_float,
            STATUS=status_form,
            MOTIVO_REPROVA='',
            PDF_PATH=''
        )

        return redirect(url_for('blueprint_lancar_solicitacao.lancar_solicitacao', usuario_logado=current_user.USUARIO))
    
