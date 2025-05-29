from peewee import PostgresqlDatabase, CharField, IntegerField, Model, FloatField, Check
from dotenv import load_dotenv
import os
from flask_login import UserMixin

load_dotenv()

db = PostgresqlDatabase(None)
db.init(os.getenv('DATABASE_URI'))

class Usuarios(UserMixin, Model):
    USUARIO = CharField(unique=True, null=False, constraints=[Check('NOME <> \'\'')])
    SENHA = CharField(null=False, constraints=[Check('NOME <> \'\'')])
    NOME = CharField()
    CPF = CharField()
    FUNCAO = CharField(null=False, constraints=[Check('NOME <> \'\'')])
    EMPRESA = IntegerField(null=False, constraints=[Check('NOME <> \'\'')])
    REVENDA = IntegerField(null=False, constraints=[Check('NOME <> \'\'')])

    class Meta:
        database = db

class Solicitacoes(Model):
    EMPRESA = IntegerField(null=False, constraints=[Check('NOME <> \'\'')])
    REVENDA = IntegerField(null=False, constraints=[Check('NOME <> \'\'')])
    USUARIO_SOLICITANTE = CharField(null=False, constraints=[Check('NOME <> \'\'')])
    DEPARTAMENTO = CharField(null=False, constraints=[Check('NOME <> \'\'')])
    TIPO_DESPESA = CharField(null=False, constraints=[Check('NOME <> \'\'')])
    DESCRICAO = CharField()
    VALOR = FloatField(null=False, constraints=[Check('NOME <> \'\'')])
    STATUS = CharField(null=False, constraints=[Check('NOME <> \'\'')])
    MOTIVO_REPROVA = CharField()

    class Meta:
        database = db

class Departamento(Model):
    CODIGO = IntegerField(null=False, constraints=[Check('NOME <> \'\'')], unique=True)
    DESCRICAO = CharField(null=False, constraints=[Check('NOME <> \'\'')])

    class Meta:
        database = db

class Tipo_Despesa(Model):
    CODIGO = IntegerField(null=False, constraints=[Check('NOME <> \'\'')], unique=True)
    DESCRICAO = CharField(null=False, constraints=[Check('NOME <> \'\'')])

    class Meta:
        database = db

