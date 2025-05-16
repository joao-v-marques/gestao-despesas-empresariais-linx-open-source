from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.database import Solicitacoes

blueprint_painel_solicitacoes = Blueprint('blueprint_painel_solicitacoes', __name__)

@blueprint_painel_solicitacoes.route('/', methods=['POST', 'GET'])
@login_required
def painel_solicitacoes():
        filtro = request.args.get('filtro', 'PENDENTE')
        query = Solicitacoes.select().where(Solicitacoes.USUARIO_SOLICITANTE == current_user.USUARIO)
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
        return render_template('painel_solicitacoes.html', solicitacoes=query, filtro=filtro, usuario_logado=current_user)