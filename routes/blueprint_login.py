from flask import Blueprint, request, redirect, url_for, render_template, session, flash

blueprint_login = Blueprint('blueprint_login', __name__)

@blueprint_login.route('/')
def pagina_login():
    return render_template('pagina_login.html')

@blueprint_login.route('/fazer-login', methods=['POST', 'GET'])
def fazer_login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        # usuario_existente = 

        # Fazer a validação para ver se o usuário/senha inserido existe ou não
        