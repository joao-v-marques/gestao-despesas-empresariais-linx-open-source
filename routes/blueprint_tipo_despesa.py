from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from decorators import role_required
from database.database import Tipo_Despesa

blueprint_tipo_despesa = Blueprint('blueprint_tipo_despesa', __name__)

@blueprint_tipo_despesa.route('/')
@login_required
@role_required('ADMIN')
def tipo_despesa():
    query = Tipo_Despesa.select().order_by(Tipo_Despesa.CODIGO)

    return render_template('tipo_despesa.html', usuario_logado=current_user.USUARIO, tipo_despesa=query)

@blueprint_tipo_despesa.route('/cadastrar', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def cadastrar():
    if request.method == 'POST':
        codigo_form = request.form['codigo']
        descricao_form = request.form['descricao'].upper()

        if not codigo_form or not descricao_form:
            flash('Nenhum campo pode estar vazio!', 'error')
            return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
        else:
            Tipo_Despesa.create(
                CODIGO = codigo_form,
                DESCRICAO = descricao_form
            )
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
        
    return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))

@blueprint_tipo_despesa.route('/deletar/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def deletar(id):
    tipo_despesa = Tipo_Despesa.select().where(Tipo_Despesa.id == id)
    if not tipo_despesa:
        flash('Tipo Despesa não foi encontrado!', 'error')
        return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
    
    if request.method == 'POST':
        tipo_despesa_deletado = Tipo_Despesa.get(Tipo_Despesa.id == id)
        tipo_despesa_deletado.delete_instance()
        flash('Tipo de Despesa deletado com sucesso!', 'success')
        return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
    
    return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
    

@blueprint_tipo_despesa.route('/editar/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def editar(id):
    tipo_despesa = Tipo_Despesa.get_or_none(Tipo_Despesa.id == id)
    if not tipo_despesa:
        flash('Tipo Despesa não foi encontrado!', 'error')
        return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
    
    if request.method == 'POST':
        tipo_despesa.CODIGO = request.form['edit_codigo']
        tipo_despesa.DESCRICAO = request.form['edit_descricao']
        tipo_despesa.save()
        flash('Tipo de Despesa editado com sucesso!', 'success')
        return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
    
    return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
