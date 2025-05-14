from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from models.database import db, Usuarios
from decorators import role_required

blueprint_gestao_usuarios = Blueprint('blueprint_gestao_usuarios', __name__)

@blueprint_gestao_usuarios.route('/')
@login_required
@role_required('ADMIN')
def pagina_gestao_usuarios():
    return render_template('pagina_gestao_usuarios.html', usuario_logado=current_user.USUARIO)

@blueprint_gestao_usuarios.route('/cadastrar-usuario', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def cadastrar_usuario():
    if request.method == 'POST':
        usuario_form = request.form['usuario'].upper()
        usuario_existente = Usuarios.select().where(Usuarios.USUARIO == usuario_form).exists()
        senha_form = request.form['senha']
        confirma_senha_form = request.form['confirma_senha']
        nome_form = request.form['nome']
        cpf_form = request.form['cpf']
        funcao_form = request.form['funcao']
        empresa_form = request.form['empresa']
        revenda_form = request.form['revenda']
        
        if len(usuario_form) <= 3:
            flash('O usuário inserido deve ter mais de 3 caracteres! Tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.pagina_gestao_usuarios'))
        elif usuario_existente == True:
            flash('O usuário inserido já existe! Tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.pagina_gestao_usuarios'))
        elif senha_form != confirma_senha_form:
            flash('As duas senhas inseridas não são iguais! Tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.pagina_gestao_usuarios'))
        elif len(senha_form) <= 2:
            flash('A senha deve conter no minimo 2 caracteres! Tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.pagina_gestao_usuarios'))
        elif len(cpf_form) != 14:
            flash('O CPF deve ter exatamente 11 números! tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.pagina_gestao_usuarios'))
        else:
            flash('Cadastro realizado com sucesso!', 'success')

            Usuarios.create(
                USUARIO=usuario_form,
                SENHA=senha_form,
                NOME=nome_form,
                CPF=cpf_form,
                FUNCAO=funcao_form,
                EMPRESA=empresa_form,
                REVENDA=revenda_form
            )

            return redirect(url_for('blueprint_gestao_usuarios.pagina_gestao_usuarios'))
            
    
    return render_template('pagina_gestao_usuarios.html', usuario_logado=current_user.USUARIO)