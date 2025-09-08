import logging
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from decorators import role_required
from database.connect_db import abrir_cursor

blueprint_gestao_usuarios = Blueprint('blueprint_gestao_usuarios', __name__)

# Rota que renderiza a pagina de gestão de usuários
@blueprint_gestao_usuarios.route('/')
@login_required
@role_required('Administrador')
def gestao_usuarios():
    cursor = None
    conn = None
    try:
        cursor, conn = abrir_cursor()
        sql = "SELECT * FROM SCHEMA.TABELA ORDER BY CAMPO"
        cursor.execute(sql)
        retorno = cursor.dict_fetchall()
    except Exception as e:
        flash(f'Erro interno ao realizar a consulta: {e}', 'error')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))    
    finally:
        cursor.close()
        conn.close()

    return render_template('gestao_usuarios.html', usuario_logado=current_user.USUARIO, usuarios=retorno)

# Rota para cadastrar um novo usuário
@blueprint_gestao_usuarios.route('/cadastrar-usuario', methods=['POST'])
@login_required
@role_required('Administrador')
def cadastrar_usuario():
    cod_apollo_form = request.form['codigo_apollo'].strip()
    usuario_form = request.form['usuario'].upper()
    senha_form = request.form['senha'].strip()
    confirma_senha_form = request.form['confirma_senha'].strip()
    nome_form = request.form['nome'].strip()
    funcao_form = request.form['funcao']
    empresa_form = request.form['empresa']
    revenda_form = request.form['revenda']

    if len(usuario_form) <= 3:
        flash('O usuário inserido deve ter mais de 3 caracteres!', 'error')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    elif senha_form != confirma_senha_form:
        flash('As duas senhas inseridas não são iguais!', 'error')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    elif len(senha_form) <= 2:
        flash('A senha deve conter no minimo 3 caracteres!', 'error')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    elif cod_apollo_form == '':
        flash('O campo "Cód. Apollo" não pode estar vazio!', "error")
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    else:
        try:
            cursor, conn = abrir_cursor()

            sql_cod_apollo = "SELECT CAMPO, CAMPO, CAMPO FROM SCHEMA.TABELA WHERE CAMPO = :1"
            valores_cod_apollo = [cod_apollo_form]
            cursor.execute(sql_cod_apollo, valores_cod_apollo)
            retorno_cod_apollo = cursor.dict_fetchall()

            if retorno_cod_apollo:
                sql = "INSERT INTO SCHEMA.TABELA (CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO, CAMPO) VALUES (:1, :2, :3, :4, :5, :6, :7)"
                valores = [
                    usuario_form,
                    senha_form,
                    nome_form,
                    funcao_form,
                    empresa_form,
                    revenda_form,
                    cod_apollo_form
                    ]
                cursor.execute(sql, valores)
                conn.commit()
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
            else:
                flash("O campo 'Cód. Apollo' Inserido não existe!", "error")
                logging.info("O campo 'Cód. Apollo' Inserido não existe!")
                return redirect(url_for("blueprint_gestao_usuarios.gestao_usuarios"))
        except Exception as e:
            conn.rollback()
            flash(f'Erro interno ao realizar a consulta: {e}', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))    
        finally:
            cursor.close()
            conn.close()

# Rota para editar um usuário
@blueprint_gestao_usuarios.route('/editar-usuario/<int:id>', methods=['POST'])
@login_required
@role_required('Administrador')
def editar_usuario(id):
    novo_usuario = request.form['usuario'].strip()
    novo_senha = request.form['senha'].strip()
    confirma_senha = request.form['confirma_senha'].strip()
    novo_nome = request.form['nome'].strip()
    novo_funcao = request.form['funcao']
    novo_empresa = request.form['empresa']
    novo_revenda = request.form['revenda']
    cod_apollo = request.form['codigo_apollo'].strip()
    if novo_senha != confirma_senha:
        flash('As senhas não são iguais!')
        return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
    else:
        try:
            cursor, conn = abrir_cursor()
            sql = "UPDATE SCHEMA.TABELA SET CAMPO = :1, CAMPO = :2, CAMPO = :3, CAMPO = :4, CAMPO = :5, CAMPO = :6, CAMPO = :7 WHERE CAMPO = :8"
            valores = [novo_usuario, novo_senha, novo_nome, novo_funcao, novo_empresa, novo_revenda, cod_apollo, id]
            cursor.execute(sql, valores)
            conn.commit()
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
        except Exception as e:
            flash(f'Erro interno ao realizar a consulta: {e}', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))    
        finally:
            cursor.close()
            conn.close()

# Rota que deleta um usuários
@blueprint_gestao_usuarios.route('/deletar-usuario/<int:id>', methods=['POST'])
@login_required
@role_required('Administrador')
def deletar_usuario(id):
        if current_user.id == id:
            flash('Você não pode deletar você mesmo!', 'error')
            return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
        else:
            try:
                cursor, conn = abrir_cursor()
                sql = "DELETE FROM SCHEMA.TABELA WHERE CAMPO = :1"
                cursor.execute(sql, [id])
                conn.commit()
                flash('Usuário deletado com sucesso!', 'success')
                return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))
            except Exception as e:
                conn.rollback()
                flash(f'Erro interno ao realizar a consulta: {e}', 'error')
                return redirect(url_for('blueprint_gestao_usuarios.gestao_usuarios'))    
            finally:
                cursor.close()
                conn.close()