import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

from app.app import app
from app.datasources import laudos


layout = html.Div([
    dcc.Link('Início', href='/apps/pag1'),
    html.H3('App 2'),
    dcc.Dropdown(
        id='query',
        options=laudos.queries,
        value=0,
    ),
    dcc.Dropdown(
        id='years',
        options=[
            {'label': '2016', 'value': '2016'},
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'}
        ],
        value=['2018'],
        multi=True

    ),
    dcc.Graph(id='years-graph'),
], style={'width': '800'})


@app.callback(Output('years-graph', 'figure'), [Input('years', 'value'), Input('query', 'value')])
def update_my_graph(selected_dropdown_value, query_value):
    data = []
    sql = laudos.lista_sql['sql'][query_value]
    df = pd.read_sql(sql, laudos.db)
    layout = go.Layout(xaxis=dict(type='category', title=df.columns[1]),
                       yaxis=dict(title='Número de pedidos'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
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

