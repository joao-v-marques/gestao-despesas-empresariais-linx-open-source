from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from decorators import role_required
from database.database import Solicitacoes

blueprint_geral_solicitacoes = Blueprint('blueprint_geral_solicitacoes', __name__)

@blueprint_geral_solicitacoes.route('/')
@login_required
@role_required('DIRETORIA', 'ADMIN')
def geral_solicitacoes():
    filtro = request.args.get('filtro', 'PENDENTE')
    query = Solicitacoes.select()
    if filtro == 'PENDENTE':
        query = query.where(Solicitacoes.STATUS == 'PENDENTE')
    elif filtro == 'APROVADO':
        query = query.where(Solicitacoes.STATUS == 'APROVADO')
    elif filtro == 'REPROVADO':
        query = query.where(Solicitacoes.STATUS == 'REPROVADO')
    elif filtro == 'COMPRA':
        query = query.where(Solicitacoes.STATUS == 'COMPRA')
    elif filtro == 'TODOS':
        query = query.order_by(Solicitacoes.STATUS)
    return render_template('geral_solicitacoes.html', solicitacoes=query, filtro=filtro, usuario_logado=current_user.USUARIO)

