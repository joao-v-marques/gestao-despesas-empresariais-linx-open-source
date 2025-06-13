from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from database.database import Departamento, Solicitacoes
from decorators import role_required

blueprint_departamento = Blueprint('blueprint_departamento', __name__)

@blueprint_departamento.route('/')
@login_required
@role_required('ADMIN')
def departamento():
    query = Departamento.select().order_by(Departamento.CODIGO)

    return render_template('departamento.html', usuario_logado=current_user.USUARIO, departamento=query)

@blueprint_departamento.route('/cadastrar', methods=['POST'])
@login_required
@role_required('ADMIN')
def cadastrar():
    codigo_form = request.form['codigo'].strip()
    descricao_form = request.form['descricao'].upper().strip()

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

@blueprint_departamento.route('/deletar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def deletar(id):
    departamento = Departamento.get_or_none(Departamento.CODIGO == id)
    if not departamento:
        flash('Departamento não encontrado!', 'error')
        return redirect(url_for('blueprint_departamento.departamento'))
    else:
        if request.method == 'POST':
            departamento.delete_instance()
            flash('Departamento deletado com sucesso!')
            return redirect(url_for('blueprint_departamento.departamento'))
        else:
            return redirect(url_for('blueprint_departamento.departamento'))


@blueprint_departamento.route('/editar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def editar(id):
    departamento = Departamento.get_or_none(Departamento.CODIGO == id)
    if not departamento:
        flash('Departamento não encontrado! tente novamente.', 'error')
        return redirect(url_for('blueprint_departamento.departamento'))
    else:
        if request.method == 'POST':
            novo_codigo = request.form['edit_codigo'].strip()
            nova_descricao = request.form['edit_descricao'].strip().upper() 

            if Departamento.get_or_none(Departamento.CODIGO == novo_codigo):
                flash('Já existe um departamento com esse código!', 'error')
                return redirect(url_for('blueprint_departamento.departamento'))
            else:
                Solicitacoes.update(CODIGO_DEPARTAMENTO=999).where(Solicitacoes.CODIGO_DEPARTAMENTO == id).execute()
                
                Departamento.create(
                    CODIGO = novo_codigo,
                    DESCRICAO = nova_descricao
                )
                
                departamento.delete_instance()

                Solicitacoes.update(CODIGO_DEPARTAMENTO = novo_codigo).where(Solicitacoes.CODIGO_DEPARTAMENTO == 999).execute()
                flash('Departamento editado com sucesso!', 'success')
                return redirect(url_for('blueprint_departamento.departamento'))
        else:
            return redirect(url_for('blueprint_departamento.departamento'))


