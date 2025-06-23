from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from decorators import role_required
from database.connect_db import abrir_cursor
import logging

blueprint_departamento = Blueprint('blueprint_departamento', __name__)

@blueprint_departamento.route('/')
@login_required
@role_required('ADMIN')
def departamento():
    try:
        cursor, conn = abrir_cursor()
        sql = "SELECT * FROM LIU_DEPARTAMENTO ORDER BY CODIGO"
        cursor.execute(sql)
        retorno = cursor.dict_fetchall()
    except Exception as e:
        flash('Erro interno ao realizar a consulta!', 'error')
        logging.error(f'Deu erro na consulta: {e}')
        return redirect(url_for('blueprint_controle_diretoria.mais_info_cd'))
    finally:
        cursor.close()
        conn.close()

    return render_template('departamento.html', usuario_logado=current_user.USUARIO, departamento=retorno)

@blueprint_departamento.route('/cadastrar', methods=['POST'])
@login_required
@role_required('ADMIN')
def cadastrar():
    codigo_form = request.form['codigo'].strip()
    descricao_form = request.form['descricao'].strip()

    if not codigo_form or not descricao_form:
        flash('Nenhum campo pode estar vazio!', 'error')
        return redirect(url_for('blueprint_departamento.departamento'))
    else:
        try:
            cursor, conn = abrir_cursor()
            sql = "INSERT INTO LIU_DEPARTAMENTO (CODIGO, DESCRICAO) VALUES (:1, :2)"
            valores = [codigo_form, descricao_form]
            cursor.execute(sql, valores)
            conn.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('blueprint_departamento.departamento'))
        except Exception as e:
            flash('Erro interno ao realizar a consulta!', 'error')
            logging.error(f'Deu erro na consulta: {e}')
            return redirect(url_for('blueprint_departamento.departamento'))
        finally:
            cursor.close()
            conn.close()

@blueprint_departamento.route('/deletar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def deletar(id):
    try:
        cursor, conn = abrir_cursor()
        sql = "DELETE FROM LIU_DEPARTAMENTO WHERE ID = :1"
        cursor.execute(sql, id)
        conn.commit()
        flash('Departamento excuido com sucesso!', 'success')
        return redirect(url_for('blueprint_departamento.departamento'))
    except Exception as e:
        flash('Erro interno ao realizar a consulta!', 'error')
        logging.error(f'Deu erro na consulta: {e}')
        return redirect(url_for('blueprint_departamento.departamento'))
    finally:
        cursor.close()
        conn.close()

@blueprint_departamento.route('/editar/<int:id>', methods=['POST'])
@login_required
@role_required('ADMIN')
def editar(id):
    return render_template('departamento.html')


