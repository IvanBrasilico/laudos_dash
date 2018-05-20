import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


import app.apps.graphs1 as graphs
from app.app import app

layout = html.Div([
    html.Div(dcc.Link('Estatísticas de quantidades por ano',
                      href='/apps/pag2')),
    html.Div(dcc.Link('Tempo no fluxo de trabalho por ano e mês',
                      href='/apps/pag3')),
    html.H3('DashBoard sistema Laudos'),
    html.Div([
        html.H6('Bem vindo ao painel de informações do sistema Laudos'),
        html.Div('Aqui estão disponíveis para visualização alguns números'
                 ' referentes ao sistema.'),
        dcc.Graph(id='tabela_geral', figure=graphs.graph_tabela_geral()),
    ]),
    html.Div(
        id='app-1-display-value'),
    html.H6('Histórico de importação - gráfico peso por país de origem'),

    dcc.Graph(id='pesopaises-graph',
              figure=go.Figure(graphs.update_pesopaises_graph())
              ),
    html.H6('Histórico de importação - relação entre número de Laudos e peso do NCM'),
    dcc.Graph(id='pesoncm-graph',
              figure=go.Figure(graphs.update_ncmpaises_graph())
              ),
    html.H6('Histórico de importação - gráfico peso por capítulo NCM'),
    html.Div('Este gráfico mostra a relação entre histórico de movimentação'
             ' por peso na importação e quantidade de Laudos. Pontos abaixo'
             ' da linha têm uma baixa relação de laudos por peso importado.'),
    dcc.Graph(id='laudosncm-graph',
              figure=go.Figure(graphs.graph_ncmlaudos())
              ),

])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
