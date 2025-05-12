from flask import Blueprint, render_template, url_for, redirect

blueprint_principal = Blueprint('blueprint_principal', __name__)

@blueprint_principal.route('/')
def pagina_principal():
    return render_template('pagina_principal.html')
