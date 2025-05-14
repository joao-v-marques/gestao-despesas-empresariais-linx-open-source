from peewee import *
from flask_login import UserMixin

db = SqliteDatabase('gestao_processos_kato.db')

class Usuarios(UserMixin, Model):
    USUARIO = CharField(unique=True)
    SENHA = CharField()
    NOME = CharField()
    CPF = CharField()
    FUNCAO = CharField()
    EMPRESA = IntegerField()
    REVENDA = IntegerField()

    class Meta:
        database = db

class Solicitacoes(Model):
    USUARIO_SOLICITANTE = ForeignKeyField(Usuarios, backref='solicitacoes', on_delete='CASCADE')
    DEPARTAMENTO = CharField()
    TIPO_DESPESA = CharField()
    DESCRICAO = CharField()
    VALOR = FloatField()
    STATUS = CharField()
    EMPRESA = IntegerField()
    REVENDA = IntegerField()

    class Meta:
        database = db