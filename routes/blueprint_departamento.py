from flask import Blueprint, render_templatem, redirect, url_for, request

blueprint_departamento = Blueprint('blueprint_departamento', __name__)

@blueprint_departamento.route('/')
def departamento():
    return render_templatem('departamento.html')