from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.database import Solicitacoes

blueprint_painel_solicitacoes = Blueprint('blueprint_painel_solicitacoes', __name__)

@blueprint_painel_solicitacoes.route('/', methods=['POST', 'GET'])
@login_required
def painel_solicitacoes():
    filtro = request.args.get('filtro', 'todos')

    status_banco = {
        'pendente': 'PENDENTE',
        'autorizada': 'AUTORIZADA',
        'processo_compra': 'PROCESSO_COMPRA'
    }

    query = Solicitacoes.select().where(Solicitacoes.USUARIO_SOLICITANTE == current_user.id)
    if filtro in status_banco:
        query = query.where(Solicitacoes.STATUS == status_banco[filtro])

    return render_template(
        'painel_solicitacoes.html',
        usuario_logado=current_user,
        solicitacoes=query,
        filtro=filtro
    )


