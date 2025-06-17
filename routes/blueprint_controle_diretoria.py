# from flask import Blueprint, render_template, redirect, url_for, request, flash
# from flask_login import login_required, current_user
# from decorators import role_required
# from gerar_pdf import gerar_pdf

# blueprint_controle_diretoria = Blueprint('blueprint_controle_diretoria', __name__)

# @blueprint_controle_diretoria.route('/')
# @login_required
# @role_required('ADMIN', 'DIRETORIA')
# def controle_diretoria():
#     query = Solicitacoes.select().where(Solicitacoes.STATUS == 'PENDENTE')
#     return render_template('controle_diretoria.html', query=query, usuario_logado=current_user.USUARIO)

# @blueprint_controle_diretoria.route('/mais-info/<int:id>', methods=['POST', 'GET'])
# @login_required
# @role_required('ADMIN', 'DIRETORIA')
# def mais_info_cd(id):
#     solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
#     return render_template('mais_info_cd.html', usuario_logado=current_user.USUARIO, solicitacao=solicitacao)


# @blueprint_controle_diretoria.route('/mudar-status', methods=['POST', 'GET'])
# @login_required
# @role_required('ADMIN', 'DIRETORIA')
# def mudar_status():
#     if request.method == 'POST':
#         solicitacao_id = request.form['id']
#         novo_status = request.form['status']
#         if novo_status == 'APROVADO':
#             solicitacao = Solicitacoes.get(Solicitacoes.id == solicitacao_id)
#             solicitacao.STATUS = novo_status
#             pdf_path = gerar_pdf(solicitacao, current_user.USUARIO)
#             solicitacao.PDF_PATH = pdf_path
#             solicitacao.save()
#             flash('Solicitação Aprovada!', 'success')
#         else:
#             novo_motivo_reprova = request.form['motivo_reprova']
#             solicitacao = Solicitacoes.get(Solicitacoes.id == solicitacao_id)
#             solicitacao.STATUS = novo_status
#             solicitacao.MOTIVO_REPROVA = novo_motivo_reprova
#             solicitacao.save()
#             flash('Solicitação Reprovada!', 'error')
#             return redirect(url_for('blueprint_controle_diretoria.controle_diretoria')) 
    
#     return redirect(url_for('blueprint_controle_diretoria.controle_diretoria'))