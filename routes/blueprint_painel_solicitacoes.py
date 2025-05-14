from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.database import Solicitacoes

blueprint_painel_solicitacoes = Blueprint('blueprint_painel_solicitacoes', __name__)

@blueprint_painel_solicitacoes.route('/')
@login_required
def pagina_painel_solicitacoes():
    # lista_pendentes = Solicitacoes.select().where(Solicitacoes.STATUS == 'PENDENTE')
    # lista_autorizadas = Solicitacoes.select().where(Solicitacoes.STATUS == 'AUTORIZADA')
    # lista_compra = Solicitacoes.select().where(Solicitacoes.STATUS == 'PROCESSO DE COMPRA')

    return render_template('pagina_painel_solicitacoes.html', usuario_logado=current_user.USUARIO)