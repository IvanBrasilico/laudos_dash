"""Este módulo carrega as estatísticas históricas do NCM.

Este módulo acessa o Banco de Dados contendo as estatísticas
históricas de importação por NCM e carrega dataframes com estes
dados.

# TODO: Atualizar base e registrar em alguma variável a fonte
# dos dados e sua data

"""
import pandas as pd

from .laudos import db, df_qtdelaudos, df_qtdelaudospais

descricao = 'Fonte: DW Aduaneiro. Data: verificar (os dados de valor estão simulados)'

# Movimentação importação: peso por país de Origem
sql = 'SELECT c.codpais as codpais, p.nompais as PaisOrigem, truncate(sum(pesoliqmercimp) /  ' + \
    '(SELECT sum(pesoliqmercimp) FROM LAUDOS.CapNCMImpPaisOrigem)*100, 2) ' +\
    'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem c ' + \
    'INNER JOIN paises p ON p.codpais = c.codpais ' + \
    'GROUP BY codpais, PaisOrigem ' + \
    'ORDER BY pesototal DESC; '
df_pesopais = pd.read_sql(sql, db)
df_pais_x_peso = df_qtdelaudospais.merge(df_pesopais, on='codpais')

# Movimentação importação: peso por capítulo NCM
sql = 'SELECT codcapncm, truncate(sum(pesoliqmercimp) /  ' + \
    '(SELECT sum(pesoliqmercimp) FROM LAUDOS.CapNCMImpPaisOrigem)*100, 2) ' +\
    'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem ' +\
    'GROUP BY codcapncm ' + \
    'ORDER BY pesototal DESC; '
df_pesoncm = pd.read_sql(sql, db)
df_laudos_x_peso = df_qtdelaudos.merge(df_pesoncm, on='codcapncm')


# Movimentação importação: peso por capítulo NCM
sql = 'SELECT codcapncm, codpais, sum(pesoliqmercimp) ' + \
    'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem ' +\
    'GROUP BY codcapncm, codpais ' + \
    'ORDER BY pesototal DESC; '
df_pesoncmpais = pd.read_sql(sql, db)

# US$/kg importação capítulo NCM - dados simulados, extrair...
import numpy as np
capsncm = set(df_pesoncm['codcapncm'])
dict_valorncm = {cap: np.random.normal(8, 2.5, 1000) for cap in capsncm}