import pandas as pd
import MySQLdb

db = MySQLdb.connect('localhost', 'root', 'ivan1234')
db.select_db('LAUDOS')


# Movimentação importação: peso por país de Origem
sql = 'SELECT p.nompais as PaisOrigem, truncate(sum(pesoliqmercimp) /  ' + \
    '(SELECT sum(pesoliqmercimp) FROM LAUDOS.CapNCMImpPaisOrigem) * 100, 2) ' + \
    'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem c ' + \
    'INNER JOIN paises p ON p.codpais = c.codpais ' + \
    'GROUP BY PaisOrigem ' + \
    'ORDER BY pesototal DESC; '
df_pesopais = pd.read_sql(sql, db)

# Movimentação importação: peso por capítulo NCM
sql = 'SELECT codcapncm, truncate(sum(pesoliqmercimp) /  ' + \
    '(SELECT sum(pesoliqmercimp) FROM LAUDOS.CapNCMImpPaisOrigem) * 100, 2) ' + \
    'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem ' +\
    'GROUP BY codcapncm ' + \
    'ORDER BY pesototal DESC; '
df_pesoncm = pd.read_sql(sql, db)


# Laudos: qtde por capítulo NCM
sql = 'SELECT SUBSTRING(ncm, 1, 2) AS codcapncm, COUNT(*) as total ' + \
    'FROM LAUDOS.itenssat ' + \
    'GROUP BY SUBSTRING(ncm, 1, 2) ' + \
    'ORDER BY total DESC; '
df_qtdelaudos = pd.read_sql(sql, db)
df_qtdelaudos['codcapncm'] = pd.to_numeric(df_qtdelaudos['codcapncm'], downcast='integer')
#print(df_qtdelaudos)

df_laudos_x_peso = df_qtdelaudos.merge(df_pesoncm, on='codcapncm')

# Recupera relatórios gravados no Banco de Dados
lista_sql = pd.read_sql('SELECT * FROM relatorios ORDER BY ID', db)
sql = lista_sql['sql'][1]
queries = []
for index, name in enumerate(lista_sql['nome']):
    queries.append({'label': name, 'value': index})

class Tabela:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        self.valor = pd.read_sql('SELECT count(*) as cont FROM ' + nome, db)

tabelas = [
    Tabela('sats', 'Pedidos de assistência Laboratorial'),
    Tabela('itenssat', 'Itens de Pedido de assistência Laboratorial'),
    Tabela('resumoslaudo', 'Laudos laboratoriais recebidos'),
    Tabela('usuarios', 'Usuários do Sistema'),
]

# Laudos: qtde por tipo e Ano
sql = 'SELECT YEAR(datapedido) AS ano, Tipo, COUNT(*) as total ' + \
    'FROM LAUDOS.sats ' + \
    'GROUP BY YEAR(datapedido), Tipo ' + \
    'ORDER BY Ano, Tipo; '
df_qtdeporanotipo = pd.read_sql(sql, db)
df_qtdelaudos['codcapncm'] = pd.to_numeric(df_qtdelaudos['codcapncm'], downcast='integer')
