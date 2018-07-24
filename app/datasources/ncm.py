"""Este módulo carrega as estatísticas históricas do NCM.

Este módulo acessa o Banco de Dados contendo as estatísticas
históricas de importação por NCM e carrega dataframes com estes
dados.

# TODO: Atualizar base e registrar em alguma variável a fonte
# dos dados e sua data

"""
import os
import pandas as pd
import numpy as np

from .laudos import db, data
from app.datasources import Data, FunctionSource

CAMINHO = os.path.dirname(__file__)
df_ncm = pd.read_excel(os.path.join(CAMINHO, 'NCM.xlsx'), header=4)
df_ncm['PESO LIQ MERC IMP POR'] = df_ncm['PESO LIQ MERC IMP'] / \
    df_ncm['PESO LIQ MERC IMP'].sum()  # Converter para porcentagem
df_ncm['COD PAIS ORIG DEST'] = pd.to_numeric(
    df_ncm['COD PAIS ORIG DEST'], errors='coerce')


datancm = Data('Fonte: DW Aduaneiro. Data: 24/07/2018 (NCM Peso 2016-2018)' +
               ' (os dados de valor estão simulados)', CAMINHO
               )

print('Loading peso por país de Origem')
# Movimentação importação: peso por país de Origem
df_pesopais = df_ncm.groupby(
    ['COD PAIS ORIG DEST', 'PAIS ORIGEM DESTINO'], as_index=False
)['PESO LIQ MERC IMP POR'].sum()
df_pesopais.columns = ['codpais', 'PaisOrigem', 'pesototal']
df_pesopais = df_pesopais.sort_values(by='pesototal', ascending=False)
df_pais_x_peso = data.df('qtdelaudospais').merge(df_pesopais, on='codpais')


def load_pesopais(caminho):
    return df_pesopais


datancm.add_source(FunctionSource('df_pesopais', load_pesopais))
datancm.load()

# def load_pesoncm(caminho):
df_pesoncm = df_ncm.groupby(
    ['COD CAPIT NCM', 'CAPITULO NCM'], as_index=False
)['PESO LIQ MERC IMP POR'].sum()
df_pesoncm.columns = ['codcapncm', 'CapituloNCM', 'pesototal']
df_pesoncm = df_pesoncm.sort_values(by='pesototal', ascending=False)
df_laudos_x_peso = data.df('qtdelaudos').merge(df_pesoncm, on='codcapncm')


# Movimentação importação: peso por ncm e pais
df_pesoncmpais = df_ncm.groupby(
    ['COD PAIS ORIG DEST',
     'PAIS ORIGEM DESTINO',
     'COD CAPIT NCM',
     'CAPITULO NCM'], as_index=False
)['PESO LIQ MERC IMP'].sum()
df_pesoncmpais.columns = ['codpais', 'PaisOrigem',
                          'codcapncm', 'CapituloNCM', 'pesototal']
df_pesoncmpais = df_pesoncmpais.sort_values(
    by=['codpais', 'pesototal'], ascending=False)

#########################
# US$/kg importação capítulo NCM - dados simulados, extrair...


def get_valor_capncnm(capncm):
    # Retira outliers
    valores = df_valor[df_valor['COD CAPIT NCM'] == capncm]['PRECO DOLAR /Kg IMP']
    valores_sem_outliers = valores[np.abs(valores - valores.mean()) <= (2 * valores.std())]
    return valores_sem_outliers


# US$/kg importação capítulo NCM - dados simulados, extrair...
capsncm = set(df_pesoncm['codcapncm'])
# dict_valorncm = {cap: np.random.normal(8, 2.5, 1000) for cap in capsncm}
df_valor7 = pd.read_excel(os.path.join(CAMINHO, 'valor7b.xlsx'), header=4)
df_valor13 = pd.read_excel(os.path.join(CAMINHO, 'valor1324b.xlsx'), header=4)
df_valor = pd.concat([df_valor7, df_valor13])
dict_valorncm = {cap: get_valor_capncnm(cap) for cap in capsncm}
