from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models.database import Solicitacoes

blueprint_controle_diretoria = Blueprint('blueprint_controle_diretoria', __name__)

@blueprint_controle_diretoria.route('/')
@login_required
def controle_diretoria():
    query = Solicitacoes.select().where(Solicitacoes.STATUS == 'PENDENTE')

    
        

    return render_template('controle_diretoria.html', query=query, usuario_logado=current_user.USUARIO)


@blueprint_controle_diretoria.route('/mudar-status', methods=['POST'])
def mudar_status():
    if request.method == 'POST':
        solicitacao_id = request.form['id']
        novo_status = request.form['status']
        solicitacao = Solicitacoes.get(Solicitacoes.id == solicitacao_id)
        solicitacao.STATUS = novo_status
        solicitacao.save()
        return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
    
    return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))