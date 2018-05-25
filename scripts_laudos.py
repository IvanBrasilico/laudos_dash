"""
Scripts para acertar a base Laudos:

Origens e embalagens.

"""
import os 

import MySQLdb
import pandas as pd
import unicodedata

host = os.environ.get('LAUDOS')
user = os.environ.get('USER_LAUDOS')
password = os.environ.get('PASS_LAUDOS')

if host:
    db = MySQLdb.connect(host, user, password)
else:
    db = MySQLdb.connect('localhost', 'root', 'ivan1234')

db.select_db('LAUDOS')

def ascii_sanitizar(text):
    """Remove marcas de diacríticos (acentos e caracteres especiais).

    Retorna NFC normalizado ASCII
    """
    return unicodedata.normalize('NFKD', text) \
        .encode('ASCII', 'ignore') \
        .decode('ASCII')

def sanitizar(text, norm_function=ascii_sanitizar):
    """Faz uma sequência de acões de normalização/sanitização de texto.

    Remove espaços à direita e esquerda, passa para "casefold"(caixa baixa),
    usa função normalização norm_function para retirar marcas de diacríticos
    (acentos e caracteres especiais), remove espaços adicionais entre palavras.
    Retorna texto sanitizado e normalizado
    Depois desse produto, suas buscas nunca mais serão as mesmas!!! :-p
    """
    if text is None or text == '':
        return text
    text = text.strip()
    text = text.casefold()
    text = norm_function(text)
    word_list = text.split()
    text = ' '.join(word.strip() for word in word_list
                    if len(word.strip()))
    return text


def processa_origens():
    # Laudos: qtde por capítulo NCM
    sql = 'SELECT * FROM LAUDOS.origens;'
    df_origens = pd.read_sql(sql, db)
    descricoes = [sanitizar(pais) for index, pais in enumerate(df_origens['descricao'])]
    df_origens['compare'] = descricoes
    print(df_origens)
    sql = 'SELECT * FROM LAUDOS.paises;'
    df_paises = pd.read_sql(sql, db)
    descricoes = [sanitizar(pais) for index, pais in enumerate(df_paises['nompais'])]
    df_paises['compare'] = descricoes
    print(df_paises)

    df_merged = df_paises.merge(df_origens, on='compare')
    df_merged = df_merged[['codpais','descricao','id']]
    print(df_merged)
    with open('updatecodigo.sql', 'w') as sql_file:
        for index, linha in df_merged.iterrows():
            sql = (f'UPDATE LAUDOS.origens SET codigo={linha["codpais"]}' +
                f' WHERE ID={linha["id"]};\n')
            print(sql)
            sql_file.write(sql)

    # print(descricoes)





processa_origens()