from flask_login import UserMixin
from database.connect_db import abrir_cursor

# cursor, conn = abrir_cursor()

# sql = "SELECT * FROM LIU_USUARIO"
# cursor.execute(sql)
# retorno = cursor.dict_fetchall()
# print(retorno)

# sql = "SELECT * FROM LIU_USUARIO WHERE ID = 1"
# cursor.execute(sql)
# retorno = cursor.dict_fetchone()
# print(retorno)

class User(UserMixin):
    def __init__(self, id, USUARIO, FUNCAO):
        self.id = id
        self.USUARIO = USUARIO
        self.FUNCAO = FUNCAO

    def get_id(self):
        return str(self.id)