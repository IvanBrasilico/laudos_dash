import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
from pandas_datareader import data as web
from datetime import datetime as dt
import MySQLdb

db = MySQLdb.connect('localhost', 'root', 'ivan1234')
db.select_db('LAUDOS')
app = dash.Dash('Hello World')

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': '2016', 'value': '2016'},
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'}
        ],
        value=['2018'],
        multi=True

    ),
    dcc.Graph(id='my-graph')
], style={'width': '500'})

app.layout = html.Div([
        html.Div(
            dcc.Tabs(
                tabs=[
                    {'label': 'Um', 'value': 1},
                    {'label': 'Dois', 'value': 2},
                    {'label': 'Três', 'value': 3},
                ],
                value=3,
                id='tabs',
                vertical=True,
                style={
                    'height': '100vh',
                    'borderRight': 'thin lightgrey solid',
                    'textAlign': 'left'
                }
            ),
            style={'width': '20%', 'float': 'left'}
        ),
        html.Div(
            html.Div(id='tab-output'),
            style={'width': '80%', 'float': 'right'}
        )
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
    })

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
    data = []
    lista_sql = pd.read_sql('SELECT * FROM relatorios ORDER BY ID', db)
    sql = lista_sql['sql'][value]
    print(sql)
    df = pd.read_sql(sql, db)
    layout = go.Layout(xaxis=dict(type='category', title=df.columns[1]),
                       yaxis=dict(title='Número de pedidos'),
                       margin={'l': 40, 'r': 0, 't': 20, 'b': 30},
                       width=800)
    for year in [2018]:
        df_filtered = df[df['Ano_Solicitacao'] == int(year)]
        data.append(go.Bar({
            'x': df_filtered[df_filtered.columns[1]],
            'y': df_filtered.qtde,
            'name': year
        }))
    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': layout
                }
            
        )
    ])


"""

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    layout = go.Layout(xaxis=dict(type='category', title='Capítulo NCM'),
                       yaxis=dict(title='Número de pedidos'),
                       margin={'l': 40, 'r': 0, 't': 20, 'b': 30},
                       width=800)
    data = []
    for year in selected_dropdown_value:
        df = pd.read_sql(
            'SELECT YEAR(dataPedido) as Ano_Solicitacao, SUBSTRING(i.ncm, 1, 2)' +
            ' AS Capitulo_NCM, COUNT(s.ID) AS Qtde FROM sats s ' +
            'INNER JOIN itenssat i ON s.ID = i.satid ' +
            ' WHERE s.unidade = 1 AND s.username <> \'25052288840\'' +
            ' GROUP BY YEAR(dataPedido), SUBSTRING(i.ncm, 1, 2) ' +
            ' ORDER BY Ano_Solicitacao, Qtde DESC',
            db
        )
        df_filtered = df[df['Ano_Solicitacao'] == int(year)]
        data.append(go.Bar({
            'x': df_filtered.Capitulo_NCM,
            'y': df_filtered.Qtde,
            'name': year
        }))
    return {
        'data': data,
        'layout': layout
    }
"""
app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)
