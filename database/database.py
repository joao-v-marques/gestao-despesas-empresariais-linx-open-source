from peewee import PostgresqlDatabase, CharField, IntegerField, Model, FloatField
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

class Solicitacoes(Model):
    EMPRESA = IntegerField(null=False)
    REVENDA = IntegerField(null=False)
    USUARIO_SOLICITANTE = CharField(null=False)
    DEPARTAMENTO = IntegerField(null=False)
    TIPO_DESPESA = IntegerField(null=False)
    DESCRICAO = CharField()
    VALOR = FloatField(null=False)
    STATUS = CharField(null=False)
    MOTIVO_REPROVA = CharField()
    PDF_PATH = CharField()

    class Meta:
        database = db

class Departamento(Model):
    CODIGO = IntegerField(null=False, unique=True)
    DESCRICAO = CharField(null=False)

    class Meta:
        database = db

class Tipo_Despesa(Model):
    CODIGO = IntegerField(null=False, unique=True)
    DESCRICAO = CharField(null=False)

    class Meta:
        database = db

