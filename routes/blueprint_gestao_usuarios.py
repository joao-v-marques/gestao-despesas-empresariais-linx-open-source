from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from database.connect_db import Usuarios
from decorators import role_required

blueprint_gestao_usuarios = Blueprint('blueprint_gestao_usuarios', __name__)

@blueprint_gestao_usuarios.route('/')
@login_required
@role_required('ADMIN')
def gestao_usuarios():
    query = Usuarios.select().order_by(Usuarios.id)

    return render_template('gestao_usuarios.html', usuario_logado=current_user.USUARIO, usuarios=query)

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
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
        elif usuario_existente == True:
            flash('O usuário inserido já existe! Tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
        elif senha_form != confirma_senha_form:
            flash('As duas senhas inseridas não são iguais! Tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
        elif len(senha_form) <= 2:
            flash('A senha deve conter no minimo 3 caracteres! Tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
        elif len(cpf_form) != 14:
            flash('O CPF deve ter exatamente 11 números! tente novamente.', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
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

            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
            
    
    return render_template('gestao_usuarios.html', usuario_logado=current_user.USUARIO)

# Rota para editar um usuário
@blueprint_gestao_usuarios.route('/editar-usuario/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def editar_usuario(id):
    usuario = Usuarios.get_or_none(Usuarios.id == id)
    if not usuario:
        flash('Usuário não encontardo.', 'error')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    
    if request.method == 'POST':
        usuario.USUARIO = request.form['usuario']
        usuario.SENHA = request.form['senha']
        usuario.NOME = request.form['nome']
        usuario.CPF = request.form['cpf']
        usuario.FUNCAO = request.form['funcao']
        usuario.EMPRESA = request.form['empresa']
        usuario.REVENDA = request.form['revenda']
        usuario.save()
        flash('Usuário atualizado com sucesso!', 'success')
    return render_template('pagina_editar.html', usuario_logado=current_user.USUARIO, usuario=usuario)

# Rota para deletar um usuário
@blueprint_gestao_usuarios.route('/deletar-usuario/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('ADMIN')
def deletar_usuario(id):
    usuario = Usuarios.get_or_none(Usuarios.id == id)
    if not usuario:
        flash('Usuário não foi encontrado!', 'error')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    if current_user.id == id:
        flash('Você não pode deletar a si mesmo enquanto estiver logado!', 'error')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    
    if request.method == 'POST':
        usuario_deletado = Usuarios.get(Usuarios.id == id)
        usuario_deletado.delete_instance()
        flash('Usuário deletado com sucesso!', 'success')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
