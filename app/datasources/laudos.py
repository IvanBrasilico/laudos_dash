"""Este módulo carrega as estatísticas do sistema Laudos.

Este módulo acessa o Banco de Dados do sistema Laudos e
carrega dataframes com estatísticas destes dados.

No caso do sistema Laudos, há uma tabela que já contém algumas
intruções SQL contendo estatísticas/agregações interessantes,
que será carregada para uma lista, podendo ser exibida em uma 
lista(Select Combo) para o usuário escolher.

A variável descricao informa origem dos dados e todos os dataframes
começam com df_, facilitando sua utilização com code completion.

"""
from collections import defaultdict

import pandas as pd
import MySQLdb

db = MySQLdb.connect('localhost', 'root', 'ivan1234')
db.select_db('LAUDOS')

descricao = "Fonte: base de dados do sistema Laudos, produção"

# Laudos: qtde por capítulo NCM
sql = 'SELECT SUBSTRING(ncm, 1, 2) AS codcapncm, COUNT(*) as total ' + \
    'FROM LAUDOS.itenssat ' + \
    'GROUP BY SUBSTRING(ncm, 1, 2) ' + \
    'ORDER BY total DESC; '
df_qtdelaudos = pd.read_sql(sql, db)
df_qtdelaudos['codcapncm'] = pd.to_numeric(df_qtdelaudos['codcapncm'], downcast='integer')
#print(df_qtdelaudos)

# Recupera relatórios gravados no Banco de Dados
lista_sql = pd.read_sql('SELECT * FROM relatorios ORDER BY ID', db)
# sql = lista_sql['sql'][1]
queries = defaultdict(list)
for index, name in enumerate(lista_sql['nome']):
    queries[lista_sql['tipo'][index]].append({'label': name, 'value': index})

class Tabela:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        df = pd.read_sql('SELECT count(*) as cont FROM ' + nome, db)
        self.valor = int(df['cont'])

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
