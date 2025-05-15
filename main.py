from flask import Flask
from flask_login import LoginManager
from models.database import db, Usuarios, Solicitacoes
from routes.blueprint_lancar_solicitacao import blueprint_lancar_solicitacao
from routes.blueprint_gestao_usuarios import blueprint_gestao_usuarios
from routes.blueprint_principal import blueprint_principal
from routes.blueprint_login import blueprint_login
from routes.blueprint_painel_solicitacoes import blueprint_painel_solicitacoes
from routes.blueprint_controle_diretoria import blueprint_controle_diretoria

app = Flask(__name__)
app.secret_key = '947ff0db41af7a42e2d5fdec73e762d9aa36b15611daac3c5b46646d613c3af6'

with db:
    db.create_tables([Usuarios, Solicitacoes])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'blueprint_login.pagina_login'

login_manager.login_message = 'Por favor, faça login para acessar esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    try:
        return Usuarios.get(Usuarios.id == int(user_id))
    except Usuarios.DoesNotExist:
        return None

app.register_blueprint(blueprint_controle_diretoria, url_prefix="/controle-diretoria")
app.register_blueprint(blueprint_painel_solicitacoes, url_prefix="/painel-solicitacoes")
app.register_blueprint(blueprint_lancar_solicitacao, url_prefix="/lancar-solicitacao")
app.register_blueprint(blueprint_gestao_usuarios, url_prefix="/gestao-usuarios")
app.register_blueprint(blueprint_principal, url_prefix="/home")
app.register_blueprint(blueprint_login, url_prefix="/login")


app.run(debug=True)