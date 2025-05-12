from flask_login import LoginManager
from models.database import Usuarios
from main import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'blueprint_login.pagina_login'

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.get_or_none(Usuarios.id == int(user_id))