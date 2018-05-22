"""Este módulo carrega as estatísticas históricas do NCM.

Este módulo acessa o Banco de Dados contendo as estatísticas
históricas de importação por NCM e carrega dataframes com estes
dados.

# TODO: Atualizar base e registrar em alguma variável a fonte
# dos dados e sua data

"""
import pandas as pd

from .laudos import db, df_qtdelaudos

descricao = 'Fonte: sistema Siscomex Importação. Data: verificar'

# Movimentação importação: peso por país de Origem
sql = 'SELECT p.nompais as PaisOrigem, truncate(sum(pesoliqmercimp) /  ' + \
    '(SELECT sum(pesoliqmercimp) FROM LAUDOS.CapNCMImpPaisOrigem)*100, 2) ' +\
    'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem c ' + \
    'INNER JOIN paises p ON p.codpais = c.codpais ' + \
    'GROUP BY PaisOrigem ' + \
    'ORDER BY pesototal DESC; '
df_pesopais = pd.read_sql(sql, db)

# Movimentação importação: peso por capítulo NCM
sql = 'SELECT codcapncm, truncate(sum(pesoliqmercimp) /  ' + \
    '(SELECT sum(pesoliqmercimp) FROM LAUDOS.CapNCMImpPaisOrigem)*100, 2) ' +\
    'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem ' +\
    'GROUP BY codcapncm ' + \
    'ORDER BY pesototal DESC; '
df_pesoncm = pd.read_sql(sql, db)
df_laudos_x_peso = df_qtdelaudos.merge(df_pesoncm, on='codcapncm')
