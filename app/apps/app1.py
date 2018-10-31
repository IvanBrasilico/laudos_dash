import dash_core_components as dcc
import dash_html_components as html
from importlib import reload
from dash.dependencies import Input, Output

import app.apps.graphs1 as graphs
from app.app import app
from app.datasources import laudos, ncm
from app.apps.layout import menu, style

layout = html.Div(
    [html.Div(id='home'),
     menu,
     html.H1('DashBoard sistema Laudos', style={'text-align': 'center'}),
     html.H3(
         'Bem vindo ao painel de informações do sistema Laudos'),
     html.Div('Nesta aplicação são disponibilizados para visualização alguns'
              ' números e gráficos referentes ao sistema. Nos links acima' +
              ' é possível navegar pelas telas de estatísticas disponíveis.'),
     html.Div([
         html.Div([
             html.H6('Números gerais do sistema Laudos'),
             html.Div(graphs.generate_table_fromdict(laudos.cells)),
             html.Div(graphs.generate_table_fromdf(
                 laudos.data.df('qtdeportipo'))),
         ], className='six columns'),
         html.Div([
             html.H6('Número de Pedidos de Laudo por Andamento'),
             html.Div(graphs.generate_table_fromdf(laudos.data.df('estados'))),
         ], className='six columns'),
     ]),
     dcc.Interval(
         id='interval-component',
         interval=3 * 3600 * 1000,  # in milliseconds
         n_intervals=0
     )
     ],
    style=style
)

@app.callback(
    Output('home', 'children'),
    [Input('interval-component', 'n_intervals')])
def refresh_laudos():
    reload(laudos)
