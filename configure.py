import logging
from flask_login import LoginManager
from database.connect_db import abrir_cursor
from database.models import User
from routes.blueprint_lancar_solicitacao import blueprint_lancar_solicitacao
from routes.blueprint_gestao_usuarios import blueprint_gestao_usuarios
from routes.blueprint_principal import blueprint_principal
from routes.blueprint_login import blueprint_login
from routes.blueprint_painel_solicitacoes import blueprint_painel_solicitacoes
from routes.blueprint_controle_diretoria import blueprint_controle_diretoria
from routes.blueprint_departamento import blueprint_departamento
from routes.blueprint_tipo_despesa import blueprint_tipo_despesa
from routes.blueprint_geral_solicitacoes import blueprint_geral_solicitacoes

def config_all(app):
    config_bp(app)
    config_login(app)

def config_bp(app):
    app.register_blueprint(blueprint_departamento, url_prefix="/departamento")
    app.register_blueprint(blueprint_controle_diretoria, url_prefix="/controle-diretoria")
    app.register_blueprint(blueprint_painel_solicitacoes, url_prefix="/painel-solicitacoes")
    app.register_blueprint(blueprint_lancar_solicitacao, url_prefix="/lancar-solicitacao")
    app.register_blueprint(blueprint_gestao_usuarios, url_prefix="/gestao-usuarios")
    app.register_blueprint(blueprint_principal, url_prefix="/home")
    app.register_blueprint(blueprint_login, url_prefix="/login")
    app.register_blueprint(blueprint_tipo_despesa, url_prefix="/tipo-despesa")
    app.register_blueprint(blueprint_geral_solicitacoes, url_prefix="/geral-solicitacoes")

def config_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'blueprint_login.pagina_login'

    login_manager.login_message = 'Por favor, faça login para acessar esta página'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        sql = "SELECT ID, USUARIO, FUNCAO, NOME FROM LIU_USUARIO WHERE ID = :1"
        valores = [user_id]

        cursor, conn = abrir_cursor()
        try:
            cursor.execute(sql, valores)
            resultado = cursor.fetchone()
            if resultado:
                return User(id=resultado[0], USUARIO=resultado[1], FUNCAO=resultado[2], NOME=resultado[3])
            else:
                return None
        except Exception as e:
            logging.error(f"Erro ao carregar usuário: {e}")
            return None
        finally:
            cursor.close()
            conn.close()