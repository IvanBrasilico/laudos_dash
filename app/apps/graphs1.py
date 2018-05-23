import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app.datasources import laudos, ncm


def update_pesopaises_graph():
    layout = go.Layout(xaxis=dict(type='category', title='País de Origem'),
                       yaxis=dict(title='Percentual em peso nas importações'),
                       margin={'l': 50, 'r': 10, 't': 10, 'b': 150})
    data = []
    data.append(go.Bar({
        'x': ncm.df_pesopais['PaisOrigem'],
        'y': ncm.df_pesopais['pesototal'],
        'name': 'Movimentação por país de origem'
    }))
    return {
        'data': data,
        'layout': layout
    }


def update_pesoncm_graph():
    layout = go.Layout(xaxis=dict(type='category', title='Capítulo NCM'),
                       yaxis=dict(title='Percentual em peso nas importações'),
                       margin={'l': 50, 'r': 10, 't': 10, 'b': 150})
    data = []
    data.append(go.Bar({
        'x': ncm.df_pesoncm['codcapncm'],
        'y': ncm.df_pesoncm['pesototal'],
        'name': 'Movimentação por Capítulo NCM'
    }))
    return {
        'data': data,
        'layout': layout
    }


def graph_ncmlaudos():
    layout = go.Layout(yaxis=dict(title='Laudos (qtde)'),
                       xaxis=dict(title='Importações (%peso)'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    peso_laudos = ncm.df_laudos_x_peso['pesototal']
    qtde_laudos = ncm.df_laudos_x_peso['total']
    sizes = [int(ncm.dict_valorncm[capncm].mean())
             for capncm in ncm.df_laudos_x_peso['codcapncm']]
    max_peso = peso_laudos.max()
    qtde_total = qtde_laudos.sum()
    ratio = qtde_total / 100
    colors = []
    for peso, qtde in zip(peso_laudos, qtde_laudos):
        if peso == 0:
            peso = 1
        razao_qtde = min(((qtde / ratio / peso) * 30), 200)
        colors.append('rgb(' +
                      str(255 - razao_qtde) +
                      ', ' +
                      str(razao_qtde)+ ', 10)')
    diagx = []
    diagy = []
    for r in range(int(max_peso)):
        diagx.append(r)
        diagy.append(r * ratio)
    data.append(go.Scatter({
        'x': peso_laudos,
        'y': qtde_laudos,
        'text': ncm.df_laudos_x_peso['codcapncm'],
        'name': 'Peso NCM x Qtde Laudos',
        'mode': 'markers',
        'marker': {'size': sizes, 'color': colors}
    }))
    data.append(go.Scatter({
        'x': diagx,
        'y': diagy,
        'name': 'linha de equilíbrio'
    }))
    return {
        'data': data,
        'layout': layout
    }


def graph_tabela_geral():
    cells = laudos.cells
    data_table = go.Table(
        # header=dict(values=["Descrição", "Quantidade"]),
        cells=dict(values=[cells['descricao'], cells['valor']])
    )
    return go.Figure(data=[data_table])


def generate_table_fromdf(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def generate_table_fromdict(pdict: dict, max_rows=10):
    max_rows = min(len(next(iter(pdict.values()))), max_rows)
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in pdict.keys()])] +
        # Body
        [html.Tr([
            html.Td(item[i]) for key, item in pdict.items()
        ]) for i in range(max_rows)]
    )


def generate_table_fromlist(columns, headers=None, max_rows=10):
    if headers is None:
        headers = []
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in headers])] +
        # Body
        [html.Tr([
            html.Td(columns[col][line]) for col in len(columns)
        ]) for line in range(min(len(columns[0]), max_rows))]
    )
