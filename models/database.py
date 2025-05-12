from peewee import *
from flask_login import UserMixin

db = SqliteDatabase('gestao_processos_kato.db')

class Usuarios(UserMixin, Model):
    USUARIO = CharField(unique=True)
    SENHA = CharField()
    NOME = CharField()
    CPF = CharField(unique=True)
    FUNCAO = CharField()
    EMPRESA = IntegerField()
    REVENDA = IntegerField()

    class Meta:
        database = db

class Solicitacoes(Model):
    DEPARTAMENTO = CharField()
    TIPO_DESPESA = CharField()
    DESCRICAO = CharField()
    VALOR = FloatField()
    STATUS = BooleanField()

    class Meta:
        database = db