import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import MySQLdb

db = MySQLdb.connect('10.61.12.154', 'usr_Laudos', 'usr_Laudos')
db.select_db('LAUDOS')
app = dash.Dash('Laudos DashBoard')
def update_pesopaises_graph():
    sql = 'SELECT p.nompais as PaisOrigem, truncate(sum(pesoliqmercimp) /  ' + \
        '(SELECT sum(pesoliqmercimp) FROM LAUDOS.CapNCMImpPaisOrigem) * 100, 2) ' + \
        'as pesototal FROM LAUDOS.CapNCMImpPaisOrigem c ' + \
        'INNER JOIN paises p ON p.codpais = c.codpais ' + \
        'GROUP BY PaisOrigem ' + \
        'ORDER BY pesototal DESC; '
    df = pd.read_sql(sql, db)
    layout = go.Layout(xaxis=dict(type='category', title='País de Origem'),
                       yaxis=dict(title='Percentual em peso nas importações'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    data.append(go.Bar({
        'x': df['PaisOrigem'],
        'y': df['pesototal'],
        'name': 'Movimentação por país de origem'
    }))
    return {
        'data': data,
        'layout': layout
    }

lista_sql = pd.read_sql('SELECT * FROM relatorios ORDER BY ID', db)
sql = lista_sql['sql'][1]
queries = []
for index, name in enumerate(lista_sql['nome']):
    queries.append({'label': name, 'value': index})

app.layout = html.Div([
    dcc.Dropdown(
        id='query',
        options=queries,
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
    dcc.Graph(id='pesopaises-graph',
              figure=go.Figure( update_pesopaises_graph()

              ))
], style={'width': '800'})


@app.callback(Output('years-graph', 'figure'), [Input('years', 'value'), Input('query', 'value')])
def update_my_graph(selected_dropdown_value, query_value):
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
