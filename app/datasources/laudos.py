"""Este módulo carrega as estatísticas do sistema Laudos.

Este módulo acessa o Banco de Dados do sistema Laudos e
carrega dataframes com estatísticas destes dados.

No caso do sistema Laudos, há uma tabela que já contém algumas
intruções SQL contendo estatísticas/agregações interessantes,
que será carregada para uma lista, podendo ser exibida em uma
lista(Select Combo) para o usuário escolher.

A variável descricao informa origem dos dados e todos os dataframes
começam com df_, facilitando sua utilização com code completion.

No Servidor, usar as variáveis de ambiente
LAUDOS, USER_LAUDOS e PASS_LAUDOS para conectar ao Servidor
de Banco de Dados.

"""
import os
from collections import defaultdict

"""
import platform
if platform == 'win32':
    import mysql.connector as MySQLdb
else:
    import MySQLdb
"""
import mysql.connector as MySQLdb
import pandas as pd
from app.datasources import Data, SqlSource, QtdeLaudosSource

# Primeiro tenta pegar do ambiente
host = os.environ.get('LAUDOS')
user = os.environ.get('USER_LAUDOS')
password = os.environ.get('PASS_LAUDOS')

# Depois de arquivo
path = os.path.basename(__file__)
filename = os.path.join(path, 'conf.csv')
try:
    with open(filename) as in_file:
        line = in_file.readline()
        host, user, password = line.split(',')
    print(host, user, password)
except FileNotFoundError:
    print('########Arquivo de conf não encontrado: %s' % filename)
    pass

if host:
    db = MySQLdb.connect(host=host, user=user, password=password, db='LAUDOS')
else:
    db = MySQLdb.connect(host='localhost', user='root', password='sala123')

# db.select_db('LAUDOS')

data = Data('Fonte: base de dados do sistema Laudos, produção', db)

years = \
    [
        {'label': '2016', 'value': '2016'},
        {'label': '2017', 'value': '2017'},
        {'label': '2018', 'value': '2018'}
    ]

# Laudos: anos contendo pedido de Laudo
sql = 'SELECT DISTINCT YEAR(DataPedido) as year FROM LAUDOS.sats;'
df_years = pd.read_sql(sql, db)
df_years = df_years.dropna()
years = [{'label': '{:0}'.format(int(year)),
          'value': '{:0}'.format(int(year))} for year in df_years['year']]

unidades = \
    [
        {'label': 'ALFSTS', 'value': '1'},
        {'label': 'ALF3', 'value': '91'},
        {'label': 'ALF10', 'value': '100'}
    ]

# Laudos: unidades contendo pedido de Laudo
sql = 'SELECT DISTINCT unidade, nome FROM LAUDOS.sats s ' \
      'INNER JOIN LAUDOS.unidades u ON s.unidade=u.ID;'
df_unidades = pd.read_sql(sql, db)
unidades = [{'label': linha.nome,
             'value': linha.unidade} for _, linha in df_unidades.iterrows()]

# Laudos: qtde por capítulo NCM
sql = 'SELECT SUBSTRING(ncm, 1, 2) AS codcapncm, COUNT(*) as total ' + \
      'FROM LAUDOS.itenssat ' + \
      'GROUP BY SUBSTRING(ncm, 1, 2) ' + \
      'ORDER BY total DESC; '
data.add_source(QtdeLaudosSource('qtdelaudos', sql))
sql_dict = {}
# Laudos: qtde por país
sql_dict['qtdelaudospais'] = 'SELECT origemid as codpais, COUNT(*) as total ' + \
                             'FROM LAUDOS.itenssat ' + \
                             'GROUP BY origemid ' + \
                             'ORDER BY total DESC; '
# Laudos: qtde por estado
sql_dict['estados'] = \
    'SELECT e.id as num, e.TipoEventoSAT as Estado, count(*) as Quantidade ' + \
    'FROM sats s INNER JOIN enumerado e ON e.id = s.estado ' + \
    'WHERE e.id != 6 ' + \
    'GROUP BY e.id, e.TipoEventoSAT ' + \
    'ORDER BY e.id'
# Laudos: qtde por tipo
sql_dict['qtdeportipo'] = 'SELECT e.TipoSAT as Tipo, COUNT(*) as total ' + \
                          'FROM sats s ' + \
                          'INNER JOIN enumerado e ON e.id = s.Tipo ' + \
                          'WHERE s.estado != 6 ' + \
                          'GROUP BY e.TipoSAT;'
# Laudos: qtde por tipo e Ano
sql_dict['qtdeporanotipo'] = 'SELECT YEAR(datapedido) AS ano, Tipo, COUNT(*) as total ' + \
                             'FROM LAUDOS.sats ' + \
                             'GROUP BY YEAR(datapedido), Tipo ' + \
                             'ORDER BY Ano, Tipo; '
for name, sql in sql_dict.items():
    source = SqlSource(name, sql)
    data.add_source(source)
data.load()

# Recupera relatórios gravados no Banco de Dados
lista_sql = pd.read_sql('SELECT * FROM relatorios ORDER BY ID', db)
# sql = lista_sql['sql'][1]
queries = defaultdict(list)
for index, name in enumerate(lista_sql['nome']):
    queries[lista_sql['tipo'][index]].append({'label': name, 'value': index})


class Tabela:
    """Monta contagem de registros de tabelas."""

    def __init__(self, nome, descricao):
        """Inicializa."""
        self.nome = nome
        self.descricao = descricao
        df = pd.read_sql('SELECT count(*) as cont FROM ' + nome, db)
        self.valor = int(df['cont'])


df_sats = pd.read_sql(
    'SELECT count(*) as cont FROM sats WHERE estado!=6', db)
tabela_sats = Tabela('sats', 'Pedidos de assistência Laboratorial')
tabela_sats.valor = int(df_sats['cont'])
df_itenssat = pd.read_sql(
    'SELECT COUNT(*) as cont FROM itenssat WHERE satid in '
    '(SELECT id FROM LAUDOS.sats WHERE estado !=6)', db)
tabela_itenssat = Tabela(
    'itenssat', 'Itens de Pedido de assistência Laboratorial')
tabela_itenssat.valor = int(df_itenssat['cont'])

tabelas = [
    tabela_sats,
    tabela_itenssat,
    Tabela('resumoslaudo', 'Laudos laboratoriais recebidos'),
    Tabela('usuarios', 'Usuários do Sistema'),
]

cells = defaultdict(list)
for tabela in tabelas:
    # cells['nome'].append(tabela.nome)
    cells['Descrição'].append(tabela.descricao)
    cells['Quantidade'].append(tabela.valor)

print('Loading discordância NCM...')
# Discordância NCM
sql = \
    '''select SUBSTRING(i.ncm, 1, 2) AS Capitulo_NCM, 
     sum(divergente)/ count(r.ID)AS percentual from sats s
     INNER JOIN itenssat i ON s.ID = i.satid
     INNER JOIN setores se ON se.ID = s.setor
     inner join resumoslaudo r on s.id = r.satid
     inner join divergencias d on r.id = d.resumolaudoid
     group by Capitulo_NCM
     ORDER BY percentual DESC;
    '''
df_discordanciancm = pd.read_sql(sql, db)

print('Loading discordância país...')
# Discordância País
sql = \
    '''select o.descricao AS PaisdeOrigem,
 sum(divergente)/ count(r.ID)AS percentual from sats s
 INNER JOIN itenssat i ON s.ID = i.satid
 INNER JOIN origens o ON o.ID = i.origemid
 inner join resumoslaudo r on s.id = r.satid
 inner join divergencias d on r.id = d.resumolaudoid
 group by PaisdeOrigem
 ORDER BY percentual DESC;
    '''
df_discordanciapais = pd.read_sql(sql, db)
