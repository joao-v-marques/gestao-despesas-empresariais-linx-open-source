from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from database.database import Departamento
from decorators import role_required

blueprint_departamento = Blueprint('blueprint_departamento', __name__)

@blueprint_departamento.route('/')
@login_required
@role_required('ADMIN')
def departamento():
    query = Departamento.select().order_by(Departamento.CODIGO)

    return render_template('departamento.html', usuario_logado=current_user.USUARIO, departamento=query)

@blueprint_departamento.route('/cadastrar', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def cadastrar():
    if request.method == 'POST':
        codigo_form = request.form['codigo']
        descricao_form = request.form['descricao'].upper()

        if not codigo_form or not descricao_form:
            flash('Nenhum campo pode estar vazio!', 'error')
            return redirect(url_for('blueprint_departamento.departamento'))
        else:
            Departamento.create(
                CODIGO = codigo_form,
                DESCRICAO = descricao_form
            )
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('blueprint_departamento.departamento'))
    
    return redirect(url_for('blueprint_departamento.departamento'))

@blueprint_departamento.route('/deletar/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def deletar(id):
    departamento = Departamento.select().where(Departamento.id == id)
    if not departamento:
        flash('O departamento não foi encontrado!' 'error')
        return redirect(url_for('blueprint_departamento.departamento'))
    
    if request.method == 'POST':
        departamento_deletado = Departamento.get(Departamento.id == id)
        departamento_deletado.delete_instance()
        flash('Departamento deletado com sucesso!', 'success')
        return redirect(url_for('blueprint_departamento.departamento'))
    
    return redirect(url_for('blueprint_departamento.departamento'))

@blueprint_departamento.route('/editar/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def editar(id):
    departamento = Departamento.get_or_none(Departamento.id == id)
    if not departamento:
        flash('Departamento não encontrado!', 'error')
        return redirect(url_for('blueprint_departamento.departamento'))

    if request.method == 'POST':
        departamento.CODIGO = request.form['edit_codigo']
        departamento.DESCRICAO = request.form['edit_descricao']
        departamento.save()
        flash('Departamento editado com sucesso!', 'success')
        return redirect(url_for('blueprint_departamento.departamento'))
    
    return redirect(url_for('blueprint_departamento.departamento'))


