from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

@blueprint_lancar_solicitacao.route('/')
@login_required
def pagina_lancar_solicitacao():
    return render_template('pagina_lancar_solicitacao.html', usuario_logado=current_user.USUARIO)