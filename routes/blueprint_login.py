from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from flask_login import login_user
from models.database import Usuarios

blueprint_login = Blueprint('blueprint_login', __name__)

@blueprint_login.route('/')
def pagina_login():
    return render_template('login.html')

@blueprint_login.route('/fazer-login', methods=['POST', 'GET'])
def fazer_login():
    if request.method == 'POST':
        usuario_form = request.form['usuario']
        senha_form = request.form['senha']
        
        try:
            usuario_existente = Usuarios.get(Usuarios.USUARIO == usuario_form)

            if usuario_existente.SENHA == senha_form:
                login_user(usuario_existente)
                return redirect(url_for('blueprint_painel_solicitacoes.painel_solicitacoes'))
            else:
                flash('Senha Incorreta! Tente novamente.', 'error')
        except Usuarios.DoesNotExist:
            flash('Usuário não encontrado! Tente novamente.', 'error')

    return render_template("login.html")