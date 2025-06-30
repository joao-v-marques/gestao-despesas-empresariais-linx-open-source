from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, USUARIO, FUNCAO, NOME, CODIGO_APOLLO):
        self.id = id
        self.USUARIO = USUARIO
        self.FUNCAO = FUNCAO
        self.NOME = NOME
        self.CODIGO_APOLLO = CODIGO_APOLLO

    def get_id(self):
        return str(self.id)