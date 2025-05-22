from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.database import Solicitacoes
from decorators import role_required

blueprint_controle_diretoria = Blueprint('blueprint_controle_diretoria', __name__)

@blueprint_controle_diretoria.route('/')
@login_required
@role_required('ADMIN', 'DIRETORIA')
def controle_diretoria():
    query = Solicitacoes.select().where(Solicitacoes.STATUS == 'PENDENTE')
    return render_template('controle_diretoria.html', query=query, usuario_logado=current_user.USUARIO)

@blueprint_controle_diretoria.route('/pagina-reprova/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN', 'DIRETORIA')
def pagina_reprova(id):
    solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
    return render_template('pagina_reprova.html', usuario_logado=current_user.USUARIO, solicitacao=solicitacao)



@blueprint_controle_diretoria.route('/mudar-status', methods=['POST'])
@login_required
@role_required('ADMIN', 'DIRETORIA')
def mudar_status():
    if request.method == 'POST':
        solicitacao_id = request.form['id']
        novo_status = request.form['status']
        if novo_status == 'APROVADO':
            solicitacao = Solicitacoes.get(Solicitacoes.id == solicitacao_id)
            solicitacao.STATUS = novo_status
            solicitacao.save()
            flash('Solicitação Aprovada!')
        else:
            novo_motivo_reprova = request.form['motivo_reprova']
            solicitacao = Solicitacoes.get(Solicitacoes.id == solicitacao_id)
            solicitacao.STATUS = novo_status
            solicitacao.MOTIVO_REPROVA = novo_motivo_reprova
            solicitacao.save()
            flash('Solicitação Reprovada!')
            return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))
    
    return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))