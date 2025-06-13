from peewee import PostgresqlDatabase, CharField, IntegerField, Model, FloatField, ForeignKeyField
from dotenv import load_dotenv
import os
from flask_login import UserMixin

load_dotenv()

db = PostgresqlDatabase(None)
db.init(os.getenv('DATABASE_URI'))

class Usuarios(UserMixin, Model):
    USUARIO = CharField(unique=True, null=False)
    SENHA = CharField(null=False)
    NOME = CharField()
    CPF = CharField()
    FUNCAO = CharField(null=False)
    EMPRESA = IntegerField(null=False)
    REVENDA = IntegerField(null=False)

    class Meta:
        database = db

class Departamento(Model):
    CODIGO = IntegerField(primary_key=True)
    DESCRICAO = CharField(null=False)

    class Meta:
        database = db

class Tipo_Despesa(Model):
    CODIGO = IntegerField(primary_key=True)
    DESCRICAO = CharField(null=False)

    class Meta:
        database = db

class Solicitacoes(Model):
    EMPRESA = IntegerField(null=False)
    REVENDA = IntegerField(null=False)
    USUARIO_SOLICITANTE = CharField(null=False)
    CODIGO_DEPARTAMENTO = ForeignKeyField(Departamento, backref='solicitacoes')
    CODIGO_TIPO_DESPESA = ForeignKeyField(Tipo_Despesa, backref='solicitacoes')
    DESCRICAO = CharField()
    VALOR = FloatField(null=False)
    STATUS = CharField(null=False)
    MOTIVO_REPROVA = CharField()
    PDF_PATH = CharField(null=True)

    class Meta:
        database = db
