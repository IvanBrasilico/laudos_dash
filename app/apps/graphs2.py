import plotly.graph_objs as go

from app.datasources import laudos as laudos


def update_pesopaises_graph():
    layout = go.Layout(xaxis=dict(type='category', title='País de Origem'),
                       yaxis=dict(title='Percentual em peso nas importações'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    data.append(go.Bar({
        'x': laudos.df_pesopais['PaisOrigem'],
        'y': laudos.df_pesopais['pesototal'],
        'name': 'Movimentação por país de origem'
    }))
    return {
        'data': data,
        'layout': layout
    }


def update_ncmpaises_graph():
    layout = go.Layout(xaxis=dict(type='category', title='Capítulo NCM'),
                       yaxis=dict(title='Percentual em peso nas importações'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    data.append(go.Bar({
        'x': laudos.df_pesoncm['codcapncm'],
        'y': laudos.df_pesoncm['pesototal'],
        'name': 'Movimentação por Capítulo NCM'
    }))
    return {
        'data': data,
        'layout': layout
    }


def graph_ncmlaudos():
    layout = go.Layout(xaxis=dict(title='Laudos (qtde)'),
                       yaxis=dict(title='Importações (%peso)'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    data.append(go.Scatter({
        'y': laudos.df_laudos_x_peso['pesototal'],
        'x': laudos.df_laudos_x_peso['total'],
        'text': laudos.df_laudos_x_peso['codcapncm'],
        'name': 'Movimentação NCM x Qtde de Laudos',
        'mode': 'markers'
    }))
    return {
        'data': data,
        'layout': layout
    }
