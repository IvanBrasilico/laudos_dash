import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

from app.app import app
from app.datasources import laudos


layout = html.Div([
    html.Div(dcc.Link('Início', href='/apps/pag1')),
    html.Div(dcc.Link('Estatísticas de quantidades por ano', href='/apps/pag2')),
    html.H3('Consultas na base Laudo. Tempo em dias por ano e mês no fluxo de trabalho'),
    html.Div([
        html.P('Selecione o fator a visualizar.\n'),
        html.P('Em seguida, selecione um ou mais anos a desenhar no gráfico.')
    ]),
    dcc.Dropdown(
        id='query2',
        options=laudos.queries[2],
        value=0,
    ),
    dcc.Dropdown(
        id='years2',
        # TODO: Get list of years from database
        options=[
            {'label': '2016', 'value': '2016'},
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'}
        ],
        value=['2018'],
        multi=True

    ),
    dcc.Graph(id='workflow-graph'),
], style={'width': '800'})


@app.callback(Output('workflow-graph', 'figure'), [Input('years2', 'value'), Input('query2', 'value')])
def update_my_graph(selected_dropdown_value, query_value):
    data = []
    sql = laudos.lista_sql['sql'][query_value]
    df = pd.read_sql(sql, laudos.db)
    layout = go.Layout(xaxis=dict(type='category', title='Mês'),
                       yaxis=dict(title='tempo'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    for year in selected_dropdown_value:
        df_filtered = df[df['Ano'] == int(year)]
        trace1 = go.Scatter({
            'x': df_filtered[df.columns[1]],
            'y': df_filtered['Envio'],
            'name': year + 'tempo de envio'
        })
        trace2 = go.Scatter({
            'x': df_filtered[df.columns[1]],
            'y': df_filtered['Resposta'],
            'name': year + 'tempo de resposta',
        })
        data.append(trace1)
        data.append(trace2)
        figure = go.Figure(data=data, layout=layout)
    return figure


app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
