import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


from app.app import app
from app.apps.graphs1 import *

layout = html.Div([
    dcc.Link('Estatísticas de quantidades por ano e mês', href='/apps/pag2'),
    html.H3('DashBoard sistema Laudos'),
    html.Div(id='app-1-display-value'),
    dcc.Graph(id='pesopaises-graph',
              figure=go.Figure(update_pesopaises_graph())
              ),
    dcc.Graph(id='pesoncm-graph',
              figure=go.Figure(update_ncmpaises_graph())
              ),
    dcc.Graph(id='laudosncm-graph',
              figure=go.Figure(graph_ncmlaudos())
              ),

])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)