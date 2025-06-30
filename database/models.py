from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, USUARIO, FUNCAO, NOME, CODIGO_APOLLO, EMPRESA, REVENDA):
        self.id = id
        self.USUARIO = USUARIO
        self.FUNCAO = FUNCAO
        self.NOME = NOME
        self.CODIGO_APOLLO = CODIGO_APOLLO
        self.EMPRESA = EMPRESA
        self.REVENDA = REVENDA

    def get_id(self):
        return str(self.id)