from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from database.database import Solicitacoes, db, Departamento, Tipo_Despesa

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
        return render_template('painel_solicitacoes.html', solicitacoes=query, filtro=filtro, usuario_logado=current_user.USUARIO)

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>')
@login_required
def mais_info_sol(id):
        solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
        select_solicitacoes = Solicitacoes.select().order_by(Solicitacoes.CODIGO_DEPARTAMENTO)
        departamento = Departamento.select().order_by(Departamento.CODIGO)
        tipo_despesa = Tipo_Despesa.select().order_by(Tipo_Despesa.CODIGO)
        return render_template('mais_info_sol.html', usuario_logado=current_user.USUARIO, solicitacao=solicitacao, departamento=departamento, tipo_despesa=tipo_despesa, select_solicitacoes=select_solicitacoes)

@blueprint_painel_solicitacoes.route('mais_info_sol/<int:id>/dowload-pdf', methods=['GET'])
@login_required
def download_pdf(id):
        solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
        if not solicitacao or not solicitacao.PDF_PATH:
                flash('PDF não encontrado!', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol'))
        return send_file(solicitacao.PDF_PATH, as_attachment=True)

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/salvar', methods=['POST', 'GET'])
@login_required
def salvar_edicao(id):
        solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
        if not solicitacao:
                flash('Solicitação não foi encontrada!', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
                
        solicitacao.CODIGO_DEPARTAMENTO = request.form['departamento']
        solicitacao.CODIGO_TIPO_DESPESA = request.form['tipo_despesa']
        solicitacao.DESCRICAO = request.form.get('descricao')
        solicitacao.VALOR = float(request.form.get('valor').replace('R$', '').replace('.', '').replace(',', '.').strip())

        solicitacao.save() 
        db.commit()
        flash('Alterações realizadas com sucesso!', 'success')
        return redirect(url_for('blueprint_painel_solicitacoes.mais_info_sol', id=id))

@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/excluir', methods=['POST', 'GET'])
@login_required
def excluir_solicitacao(id):
        solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
        if not solicitacao:
                flash('Nenhuma Solicitação foi encontrada!', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
        
        if request.method == 'POST':
                solicitacao_deletada = Solicitacoes.get(Solicitacoes.id == id)
                solicitacao_deletada.delete_instance()
                flash('Solicitação Excluida com sucesso!', 'success')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user.USUARIO))
        return render_template('mais_info_sol.html', usuario_logado=current_user.USUARIO)


@blueprint_painel_solicitacoes.route('/mais_info_sol/<int:id>/reenviar', methods=['POST', 'GET'])
@login_required
def reenviar_solicitacao(id):
        solicitacao = Solicitacoes.get_or_none(Solicitacoes.id == id)
        if not solicitacao:
                flash('Nenhuma Solicitação foi encontrada!', 'error')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user))
        
        if request.method == 'POST':
                solicitacao.STATUS = 'PENDENTE'
                solicitacao.save()
                flash('Solicitação Reenviada com sucesso!', 'success')
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes', usuario_logado=current_user))
        return render_template('painel_solicitacoes.html')