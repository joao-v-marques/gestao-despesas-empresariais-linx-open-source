from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from database.database import db, Departamento
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
def cadastrar_departamento():
    if request.method == 'POST':
        codigo_form = request.form('codigo')
        descricao_form = request.form('descricao')

        Departamento.create(
            CODIGO = codigo_form,
            DESCRICAO = descricao_form
        )

@blueprint_departamento.route('/deletar')
@login_required
@role_required('ADMIN')
def deletar_departamento(id):
    departamento = Departamento.select().where(Departamento.id == id)

