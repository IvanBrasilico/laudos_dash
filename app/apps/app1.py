import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import app.apps.graphs1 as graphs
from app.datasources import laudos
from app.apps.layout import menu, style

layout = html.Div(
    [menu,
     html.Div([
         html.Div([
             html.Div([
                 html.Img(id='image', src='/laudos_dash/static/image_mini.jpg')
             ], className='three columns'),
             html.Div([
                 dcc.Graph(id='tipopedido-graph',
                           figure=go.Figure(
                               graphs.update_tipopedido_graph())
                           )
             ], className='three columns'),
             html.Div([
                 html.H6('Números gerais do sistema Laudos'),
                 html.Div(graphs.generate_table_fromdict(laudos.cells)),
             ])
         ], className='six columns'),
         html.Div([
             dcc.Graph(id='statusedido-graph',
                       figure=go.Figure(
                           graphs.update_statuspedido_graph())
                       )
         ], className='six columns'),
     ])
     ],
    style=style
)
