from flask import Blueprint, render_template, redirect, url_for, request

blueprint_lancar_solicitacao = Blueprint('blueprint_lancar_solicitacao', __name__)

@blueprint_lancar_solicitacao.route('/')
def pagina_lancar_solicitacao():
    return render_template('pagina_lancar_solicitacao.html')