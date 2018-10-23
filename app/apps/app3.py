import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app.app import app
from app.datasources import laudos
from app.apps.layout import menu, style

unidade = '1'

layout = html.Div([
    menu,
    html.H3('Consultas na base Laudo. ' +
            'Tempo em dias por ano e mês no fluxo de trabalho'),
    html.Div([
        html.P('Selecione o fator a visualizar.\n'),
        html.P('Em seguida, selecione um ou mais anos a desenhar no gráfico.')
    ]),
    dcc.Dropdown(
        id='query2',
        options=laudos.queries[2],
        value=laudos.queries[2][0]['value'],
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
], style=style
)


@app.callback(Output('workflow-graph', 'figure'),
              [Input('years2', 'value'), Input('query2', 'value')])
def update_my_graph(selected_dropdown_value, query_value):
    data = []
    sql = laudos.lista_sql['sql'][query_value]
    sql = sql.replace('%unidade%', unidade)
    df = pd.read_sql(sql, con=laudos.db, params=[1])
    layout = go.Layout(xaxis=dict(type='category', title='Mês'),
                       yaxis=dict(title='tempo'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80}
                       )
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
