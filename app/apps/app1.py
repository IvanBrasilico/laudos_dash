import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import app.apps.graphs1 as graphs
from app.app import app
from app.datasources import laudos
from app.apps.layout import menu, style

layout = html.Div(
    [menu,
     html.H3('DashBoard sistema Laudos'),
     html.H6(
         'Bem vindo ao painel de informações do sistema Laudos'),
     html.Div('Nesta tela são disponibilizados para visualização alguns'
              ' números e gráficos referentes ao sistema. Nos links acima' +
              ' é possível navegar em algumas estatísticas adicionais.'),
     html.H5('Números gerais do sistema Laudos'),
     html.Div(graphs.generate_table_fromdict(laudos.cells)),
     html.H5('Número de Pedidos de Laudo por Andamento'),
     html.Div(graphs.generate_table_fromdf(
         laudos.df_estados)),
     html.Div(
         id='app-1-display-value'),
     html.H6(
         'Histórico de importações - Peso por país de origem'),
     dcc.Graph(id='pesopaises-graph',
               figure=go.Figure(
                   graphs.update_pesopaises_graph())
               ),
     html.H6('Histórico de importações - Peso por capítulo NCM'),
     dcc.Graph(id='pesoncm-graph',
               figure=go.Figure(
                   graphs.update_ncmpaises_graph())
               ),
     html.H6('Histórico de importação -' +
             'Relação entre número de Laudos e peso do NCM'),
     html.Div('Este gráfico mostra a relação entre histórico de movimentação'
              ' por peso na importação e quantidade de Laudos. Pontos abaixo'
              ' da linha têm uma baixa relação de laudos por peso importado.'),
     dcc.Graph(id='laudosncm-graph',
               figure=go.Figure(graphs.graph_ncmlaudos())
               ),
     ],
    style={'class': 'conteiner',
           'text-align': 'center',
           'border-radius': '10px',
           'margin': '50px'}
)


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
