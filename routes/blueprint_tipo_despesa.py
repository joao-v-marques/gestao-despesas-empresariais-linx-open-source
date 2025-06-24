from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from decorators import role_required
from database.connect_db import abrir_cursor
import logging

blueprint_tipo_despesa = Blueprint('blueprint_tipo_despesa', __name__)

@blueprint_tipo_despesa.route('/')
@login_required
@role_required('ADMIN')
def tipo_despesa():
    try:
        cursor, conn = abrir_cursor()
        sql = "SELECT * FROM LIU_TIPO_DESPESA ORDER BY CODIGO"
        cursor.execute(sql)
        retorno = cursor.dict_fetchall()
    except Exception as e:
        flash('Erro interno ao realizar a consulta!', 'error')
        logging.error(f'Deu erro na consulta: {e}')
        return redirect(url_for('blueprint_tipo_despesa.tipo_despesa', usuario_logado=current_user.USUARIO))
    finally:
        cursor.close()
        conn.close() 

    return render_template('tipo_despesa.html', usuario_logado=current_user.USUARIO, tipo_despesa=retorno)


@blueprint_tipo_despesa.route('/cadastrar', methods=['POST'])
@login_required
@role_required('ADMIN')
def cadastrar():
    if request.method == 'POST':
        codigo_form = request.form['codigo'].strip()
        descricao_form = request.form['descricao'].upper().strip()

        if not codigo_form or not descricao_form:
            flash('Nenhum campo pode estar vazio!', 'error')
            return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
        else:
            try:
                cursor, conn = abrir_cursor()
                sql = "INSERT INTO LIU_TIPO_DESPESA (CODIGO, DESCRICAO) VALUES (:1, :2)"
                valores = [codigo_form, descricao_form]
                cursor.execute(sql, valores)
                conn.commit()
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
            except Exception as e:
                flash('Erro interno ao realizar a consulta!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
            finally:
                cursor.close()
                conn.close()

@blueprint_tipo_despesa.route('/deletar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def deletar(id):
    if request.method == 'POST':
        try:
            cursor, conn = abrir_cursor()
            sql = "DELETE FROM LIU_TIPO_DESPESA WHERE CODIGO = :1"
            cursor.execute(sql, [id])
            conn.commit()
            flash('Tipo de Despesa excluido com sucesso', 'success')
            return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
        except Exception as e:
                flash('Erro interno ao realizar a consulta!', 'error')
                logging.error(f'Deu erro na consulta: {e}')
                return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
        finally:
            cursor.close()
            conn.close()

@blueprint_tipo_despesa.route('/editar/<int:id>', methods=['POST', 'GET'])
@login_required
@role_required('ADMIN')
def editar(id):
    novo_codigo = request.form['edit_codigo'].strip()
    novo_descricao = request.form['edit_descricao'].strip()

    if len(novo_codigo) != 4:
        flash('O código deve ter 4 caracteres!')
        return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
    else:
        try:
            cursor, conn = abrir_cursor()
            sql_check = "SELECT COUNT(*) FROM LIU_TIPO_DESPESA WHERE CODIGO = :1"
            cursor.execute(sql_check, [novo_codigo])
            existe = cursor.fetchone()[0]
            if existe:
                flash('Já existe um tipo de despesa com esse código!', 'error')
                return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
            else:
                sql = "UPDATE LIU_TIPO_DESPESA SET CODIGO = :1, DESCRICAO = :2 WHERE CODIGO = :3"
                valores = [novo_codigo, novo_descricao, id]
                cursor.execute(sql, valores)
                conn.commit()
                return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
        except Exception as e:
            flash('Erro interno ao realizar a consulta!', 'error')
            logging.error(f'Deu erro na consulta: {e}')
            return redirect(url_for('blueprint_tipo_despesa.tipo_despesa'))
        finally:
            cursor.close()
            conn.close()