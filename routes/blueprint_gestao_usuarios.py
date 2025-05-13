from flask import Blueprint, render_template, redirect, request, flash, url_for
from models.database import db, Usuarios

blueprint_gestao_usuarios = Blueprint('blueprint_gestao_usuarios', __name__)

@blueprint_gestao_usuarios.route('/')
def pagina_gestao_usuarios():
    return render_template('pagina_gestao_usuarios.html')

@blueprint_gestao_usuarios.route('/cadastrar-usuario', methods=['POST', 'GET'])
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
            flash('O CPF deve ter exatamente 11 números! tente novamente.')
            return redirect(url_for('blueprint_gestao_usuarios.pagina_gestao_usuarios'))
        else:
            flash('Cadastro realizado com sucesso!')

            Usuarios.create(USUARIO=usuario_form,
                            SENHA=senha_form,
                            NOME=nome_form,
                            CPF=cpf_form,
                            FUNCAO=funcao_form,
                            EMPRESA=empresa_form,
                            REVENDA=revenda_form)
            return render_template('pagina_gestao_usuarios.html')
            
    
    return render_template('pagina_gestao_usuarios.html')