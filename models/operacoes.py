from database import db, Usuarios, Solicitacoes

# Usuarios.delete_by_id(2)

Usuarios.create(USUARIO='ADMIN', SENHA='123', NOME='ADMINISTRATOR', CPF='000.000.000-00', FUNCAO='ADMIN', EMPRESA=1, REVENDA=1)

# Usuarios.create(USUARIO='FUNCIONARIO', SENHA='123', NOME='FUNCIONARIO', CPF='000.000.000-00', FUNCAO='FUNCIONARIO', EMPRESA=1, REVENDA=1)

# Usuarios.create(USUARIO='DIRETORIA', SENHA='123', NOME='DIRETORIA', CPF='000.000.000-00', FUNCAO='DIRETORIA', EMPRESA=1, REVENDA=1)

# Usuarios.create(USUARIO='TESTE01', SENHA='123', NOME='TESTE01', CPF='000.000.000-00', FUNCAO='FUNCIONARIO', EMPRESA=1, REVENDA=1)

# Usuarios.create(USUARIO='TESTE02', SENHA='123', NOME='TESTE02', CPF='000.000.000-00', FUNCAO='FUNCIONARIO', EMPRESA=1, REVENDA=1)

# Usuarios.create(USUARIO='TESTE03', SENHA='123', NOME='TESTE03', CPF='000.000.000-00', FUNCAO='FUNCIONARIO', EMPRESA=1, REVENDA=1)

# Usuarios.create(USUARIO='TESTE04', SENHA='123', NOME='TESTE04', CPF='000.000.000-00', FUNCAO='FUNCIONARIO', EMPRESA=1, REVENDA=1)

# Usuarios.create(USUARIO='TESTE05', SENHA='123', NOME='TESTE05', CPF='000.000.000-00', FUNCAO='FUNCIONARIO', EMPRESA=1, REVENDA=1)


# usuario_form = 'ADMIN'
# usuario_existente = Usuarios.select().where(Usuarios.USUARIO == usuario_form)

# print(usuario_existente.exists())

# Solicitacoes.create(
#                 EMPRESA=1,
#                 REVENDA=1,
#                 USUARIO_SOLICITANTE = 'ADMIN',
#                 DEPARTAMENTO='400',
#                 TIPO_DESPESA='5138',
#                 DESCRICAO='TESTEEEEEEEE',
#                 VALOR=578,
#                 STATUS='PENDENTE'
#             )

# query = Solicitacoes.select().where(Solicitacoes.STATUS == 'PENDENTE').order_by(Solicitacoes.USUARIO_SOLICITANTE)

# for solicitacao in query:
#     print(solicitacao.USUARIO_SOLICITANTE, solicitacao.STATUS)