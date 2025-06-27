from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, USUARIO, FUNCAO, NOME):
        self.id = id
        self.USUARIO = USUARIO
        self.FUNCAO = FUNCAO
        self.NOME = NOME

    def get_id(self):
        return str(self.id)