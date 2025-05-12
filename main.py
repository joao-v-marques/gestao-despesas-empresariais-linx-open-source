from flask import Flask
from models.database import db, Usuarios, Solicitacoes
from routes.blueprint_lancar_solicitacao import blueprint_lancar_solicitacao
from routes.blueprint_gestao_usuarios import blueprint_gestao_usuarios
from routes.blueprint_principal import blueprint_principal
from routes.blueprint_login import blueprint_login

db.connect()
db.create_tables([Usuarios, Solicitacoes])

app = Flask(__name__)
app.secret_key = '578198451578'

app.register_blueprint(blueprint_lancar_solicitacao, url_prefix="/lancar-solicitacao")
app.register_blueprint(blueprint_gestao_usuarios, url_prefix="/gestao-usuarios")
app.register_blueprint(blueprint_principal, url_prefix="/home")
app.register_blueprint(blueprint_login, url_prefix="/login")

app.run(debug=True)