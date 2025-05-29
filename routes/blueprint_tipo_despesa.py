from flask import Blueprint, render_template, redirect, url_for, request

blueprint_tipo_despesa = Blueprint('blueprint_tipo_despesa', __name__)

@blueprint_tipo_despesa.route('/')
def tipo_despesa():
    return render_template('tipo_despesa.html')