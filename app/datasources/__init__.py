"""Módulo para carregar as estatísticas e agregações.

Este módulo acessa os Banco de Dados e
carrega dataframes com estes dados.

A variável descricao informa origem dos dados e todos os dataframes
começam com df_, facilitando sua utilização com code completion.

Recomenda-se ser criado um módulo por fonte de informação a adicionar,
por questões de organização.

"""
import pandas as pd
class Data():
    def __init__(self, descricao='', db=None):
        self.db = db
        self.descricao = descricao
        self.sources = {}

    def load(self):
        for name, src in self.sources.items():
            print('Loading %s ' % name)
            src.load(self.db)

    def load_source(self, name):
        src = self.sources[name]
        src.load(self.db)

    def add_source(self, source):
        self.sources[source.name] = source
    
    def rm_source(self, name):
        self.sources.pop(name)

    def df(self, name):
        return self.sources[name].df

class Source():
    def __init__(self, name):
        self.df = None
        self.name = name
    def load(self, conn):
        raise NotImplemented('Não implementado!')

class SqlSource(Source):

    def __init__(self, name, sql):
        Source.__init__(self, name)
        self.sql = sql

    def load(self, db):
        self.df = pd.read_sql(self.sql, db)
    
class QtdeLaudosSource(SqlSource):
    def load(self, db):
        SqlSource.load(self, db)
        self.df['codcapncm'] = pd.to_numeric(
            self.df['codcapncm'], downcast='integer'
        )

class FunctionSource(Source):

    def __init__(self, name, function):
        Source.__init__(self, name)
        self.function = function

    def load(self, conn):
        self.df = self.function(conn)