from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from decorators import role_required

blueprint_tipo_despesa = Blueprint('blueprint_tipo_despesa', __name__)

@blueprint_tipo_despesa.route('/')
@login_required
@role_required('ADMIN')
def tipo_despesa():
    return render_template('tipo_despesa.html')