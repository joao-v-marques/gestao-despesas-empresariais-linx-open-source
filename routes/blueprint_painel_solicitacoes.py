from flask import Blueprint, render_template, request, redirect, url_for, flash
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

@blueprint_painel_solicitacoes.route('/excluir-solicitacao/<int:id>', methods=['POST', 'GET'])
@login_required
def excluir_solicitacao(id):
        solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)

        if request.method == 'POST':
                solicitacao_deletada = Solicitacoes.get(Solicitacoes.id == id)
                solicitacao_deletada.delete_instance()
                flash('Solicitação deletada com sucesso!')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))


@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>')
@login_required
def mais_info_sol(id):
        solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
        return render_template('mais_info_sol.html', usuario_logado=current_user.USUARIO, solicitacao=solicitacao)
