import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
from datetime import datetime as dt
import MySQLdb

db = MySQLdb.connect('localhost', 'root', 'ivan1234')
db.select_db('LAUDOS')
app = dash.Dash('Hello World')

lista_sql = pd.read_sql('SELECT * FROM relatorios ORDER BY ID', db)
sql = lista_sql['sql'][1]
queries = []
for index, name in enumerate(lista_sql['nome']):
    queries.append({'label': name, 'value': index})

app.layout = html.Div([
    dcc.Dropdown(
        id='query',
        options= queries,
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
    dcc.Graph(id='my-graph'),
    dcc.Graph(id='pesopaises-graph')

], style={'width': '800'})

"""
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

@app.callback(Output('my-graph', 'figure'), [Input('years', 'value'), Input('query', 'value')])
def update_graph(selected_dropdown_value, query_value):
    data = []
    sql = lista_sql['sql'][query_value]
    df = pd.read_sql(sql, db)
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

if __name__ == '__main__':
    app.run_server(debug=True)
