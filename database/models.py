from flask_login import UserMixin
from database.connect_db import abrir_cursor

def listar_usuarios():
    cursor, conn = abrir_cursor()

    cursor.execute("""
        SELECT USUARIO, NOME FROM GER_USUARIO WHERE NOME = 'DIRETORIA'
""")

    retorno = cursor.fetchall()
    for linha in retorno:
        print(f"""
Usuario: {linha[0]}
Nome:    {linha[1]}
""")
        
    cursor.close()
    conn.close()


def buscar_usuario():
    usuario_form = 'ADMIN'
    senha_form = '123'

    sql = "SELECT LOGIN, SENHA FROM GER_USUARIO WHERE LOGIN = :1"
    valores = [usuario_form]
    cursor, conn = abrir_cursor()
    cursor.execute(sql, valores)
    retorno = cursor.fetchall()

    for linha in retorno:
        print(linha)

class User(UserMixin):
    def __init__(self, id, USUARIO, FUNCAO):
        self.id = id
        self.USUARIO = USUARIO
        self.FUNCAO = FUNCAO

    def get_id(self):
        return str(self.id)