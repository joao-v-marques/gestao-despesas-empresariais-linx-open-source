from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

@blueprint_lancar_solicitacao.route('/')
@login_required
def pagina_lancar_solicitacao():
    return render_template('pagina_lancar_solicitacao.html', usuario_logado=current_user.USUARIO)

@blueprint_lancar_solicitacao.route('/fazer-lancamento')
@login_required
def fazer_lancamento():
    if request.method == 'POST':
        departamento_form = request.form['departamento']
        tipo_despesa_form = request.form['tipo_despesa']
        descricao_form = request.form['descricao']
        valor_form = request.form['valor']
        status_form = 'PENDENTE'

        return redirect(url_for('blueprint_lancar_solicitacoes.pagina_lancar_solicitacoes'))

    