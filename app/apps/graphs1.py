import math
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app.datasources import laudos, ncm

def update_tipopedido_graph():
    layout = go.Layout(xaxis=dict(type='category', title='Tipo de Pedido de Exame'),
                       yaxis=dict(title='Total'),
                       margin={'l': 10, 'r': 10, 't': 10, 'b': 10})
    data = []
    data.append(go.Pie({
        'labels': laudos.data.df('qtdeportipo')['Tipo'],
        'values': laudos.data.df('qtdeportipo')['total'],
        'name': 'Total por tipo de pedido'
    }))
    return {
        'data': data,
        'layout': layout
    }


def update_statuspedido_graph():
    annotations = []
    for estado, qtde in zip(
            laudos.data.df('estados')['Estado'],
            laudos.data.df('estados')['Quantidade']):
        annotations.append(dict(xref='y', y=estado, x=qtde + 110,
                                text=str(qtde), showarrow=False))
    layout = go.Layout(yaxis=dict(type='category'),
                       margin={'l': 250, 'r': 50, 't': 20, 'b': 30})
    layout['annotations'] = annotations
    data = []
    data.append(go.Bar({
        'y': laudos.data.df('estados')['Estado'],
        'x': laudos.data.df('estados')['Quantidade'],
        'name': 'Pedidos de Laudo por Andamento',
        'orientation': 'h'
    }))
    return {
        'data': data,
        'layout': layout
    }


def update_pesopaises_graph():
    layout = go.Layout(xaxis=dict(type='category', title='País de Origem'),
                       yaxis=dict(title='Percentual em peso nas importações'),
                       margin={'l': 50, 'r': 10, 't': 10, 'b': 150})
    data = []
    data.append(go.Bar({
        'x': ncm.datancm.df('df_pesopais')['PaisOrigem'],
        'y': ncm.datancm.df('df_pesopais')['pesototal'],
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

def update_discordanciancm_graph():
    layout = go.Layout(xaxis=dict(type='category', title='Discordância NCM'),
                       yaxis=dict(title='Percentual de discordância por NCM'),
                       margin={'l': 50, 'r': 10, 't': 10, 'b': 150})
    data = []
    data.append(go.Bar({
        'x': laudos.df_discordanciancm['Capitulo_NCM'],
        'y': laudos.df_discordanciancm['percentual'],
        'name': 'Discordância por Capítulo NCM'
    }))
    return {
        'data': data,
        'layout': layout
    }


def update_discordanciapais_graph():
    layout = go.Layout(xaxis=dict(type='category', title='Discordância País'),
                       yaxis=dict(title='Percentual de discordância por País'),
                       margin={'l': 50, 'r': 10, 't': 10, 'b': 150})
    data = []
    data.append(go.Bar({
        'x': laudos.df_discordanciapais['PaisdeOrigem'],
        'y': laudos.df_discordanciapais['percentual'],
        'name': 'Discordância por país de origem'
    }))
    return {
        'data': data,
        'layout': layout
    }


def colors_por_ratio(peso_ncm, qtde_laudos, ratio):
    """Define um gradiente de cor.

    Define um gradiente de cor, de acordo com a proporção
    relativa peso/laudos normalizada.
    Verde = qtde_laudos > peso_ncm
    Vermelho = qtde_laudos < peso_ncm

    """
    colors = []
    for peso, qtde in zip(peso_ncm, qtde_laudos):
        if peso == 0:
            peso = 1
        razao_qtde = min(((qtde / ratio / peso) * 30), 200)
        colors.append('rgb(' +
                      str(255 - razao_qtde) +
                      ', ' +
                      str(razao_qtde) + ', 10)')
    return colors


def markers_size_por_valor(codcapncm):
    """Retorna uma matriz de números.

    O número será maior de acordo com o valor médio do NCM

    """
    marker_sizes = []
    for capncm in codcapncm:
        marker_ncm = ncm.dict_valorncm[capncm].mean() * 5
        if marker_ncm < 4:
            marker_ncm = 4
        elif marker_ncm > 30:
            marker_ncm = 30
        marker_sizes.append(marker_ncm)
    return marker_sizes


def graph_ncmlaudos():
    layout = go.Layout(yaxis=dict(title='Laudos (qtde)'),
                       xaxis=dict(title='Importações (%peso)'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    peso_ncm = ncm.df_laudos_x_peso['pesototal'] * 100
    qtde_laudos = ncm.df_laudos_x_peso['total']
    sizes = markers_size_por_valor(ncm.df_laudos_x_peso['codcapncm'])
    max_peso = peso_ncm.max()
    qtde_total = qtde_laudos.sum()
    ratio = qtde_total / 100
    colors = colors_por_ratio(peso_ncm, qtde_laudos, ratio)
    diagx = []
    diagy = []
    for r in range(int(max_peso)):
        diagx.append(r)
        diagy.append(r * ratio)
    data.append(go.Scatter({
        'x': ['%.2f' % peso for peso in peso_ncm],
        'y': qtde_laudos,
        'text': ncm.df_laudos_x_peso['codcapncm'],
        'name': 'Imp. x Laudos',
        'mode': 'markers',
        'marker': {'size': sizes, 'color': colors}
    }))
    data.append(go.Scatter({
        'x': diagx,
        'y': diagy,
        'name': 'Equilíbrio'
    }))
    return {
        'data': data,
        'layout': layout
    }


def graph_paislaudos():
    layout = go.Layout(yaxis=dict(title='Laudos (qtde)'),
                       xaxis=dict(title='Importações (%peso)'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    peso_ncm = ncm.df_pais_x_peso['pesototal'] * 100
    qtde_laudos = ncm.df_pais_x_peso['total']
    # sizes = markers_size_por_valor(ncm.df_pais_x_peso['PaisOrigem'])
    sizes = 10
    max_peso = peso_ncm.max()
    qtde_total = qtde_laudos.sum()
    ratio = qtde_total / 100
    colors = colors_por_ratio(peso_ncm, qtde_laudos, ratio)
    diagx = []
    diagy = []
    for r in range(min(int(max_peso), 100)):
        diagx.append(r)
        diagy.append(r * ratio)
    data.append(go.Scatter({
        'x': ['%.2f' % peso for peso in peso_ncm],
        'y': qtde_laudos,
        'text': ncm.df_pais_x_peso['PaisOrigem'],
        'name': 'Imp. x Laudos',
        'mode': 'markers',
        'marker': {'size': sizes, 'color': colors}
    }))
    data.append(go.Scatter({
        'x': diagx,
        'y': diagy,
        'name': 'Equilíbrio'
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
