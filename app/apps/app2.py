import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from importlib import reload
from mysql.connector.errors import OperationalError

from app.app import app
from app.datasources import laudos
from app.apps.layout import menu, style

layout = html.Div([
    menu,
    html.H3('Consultas na base Laudo - Quantidade por ano de um fator'),
    dcc.Dropdown(
        id='query',
        options=laudos.queries[1],
        value=0,
    ),
    dcc.Dropdown(
        id='years',
        options=laudos.years,
        value=['2018'],
        multi=True

    ),
    dcc.Dropdown(
        id='unidades',
        options=laudos.unidades,
        value=1,
        multi=False
    ),
    dcc.Graph(id='years-graph'),
], style=style
)


@app.callback(Output('years-graph', 'figure'),
              [Input('years', 'value'), Input('query', 'value'), Input('unidades', 'value')])
def update_my_graph(selected_dropdown_value, query_value, unidades_value):
    data = []
    sql = laudos.lista_sql['sql'][query_value]
    sql = sql.replace('%unidade%', str(unidades_value))
    try:
        df = pd.read_sql(sql, con=laudos.db)
    except OperationalError:
        reload(laudos)
        df = pd.read_sql(sql, con=laudos.db)
    layout = go.Layout(xaxis=dict(type='category', title=df.columns[1]),
                       yaxis=dict(title='Número de pedidos'),
                       margin={'l': 100, 'r': 50, 't': 50, 'b': 150})
    data = []
    for year in selected_dropdown_value:
        df_filtered = df[df['Ano_Solicitacao'] == int(year)]
        data.append(go.Bar({
            'x': df_filtered[df.columns[1]],
            'y': df_filtered.qtde,
            'name': year
        }))
    return {
        'data': data,
        'layout': layout
    }


app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
