import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import app.apps.graphs1 as graphs
from app.app import app
from app.datasources import laudos, ncm
from app.apps.layout import menu, style

layout = html.Div(
    [menu,
     html.H1('DashBoard sistema Laudos', style={'text-align': 'center'}),
     html.H3(
         'Bem vindo ao painel de informações do sistema Laudos'),
     html.Div('Nesta tela são disponibilizados para visualização alguns'
              ' números e gráficos referentes ao sistema. Nos links acima' +
              ' é possível navegar em algumas estatísticas adicionais.'),
     html.Div([
         html.Div([
             html.H6('Números gerais do sistema Laudos'),
             html.Div(graphs.generate_table_fromdict(laudos.cells)),
         ], className='six columns'),
         html.Div([
             html.H6('Número de Pedidos de Laudo por Andamento'),
             html.Div(graphs.generate_table_fromdf(laudos.df_estados)),
         ], className='six columns'),
     ]),
     html.Div(
         id='app-1-display-value'),
     html.H4(
         'Abaixo seguem alguns dados sobre histórico de importações'),
     html.Div(
         'O objetivo é poder comparar o histórico de importações com'
         ' os dados do sistema Laudos. ' + ncm.descricao),
     html.Div([
         html.Div([html.H6(
             'Histórico de importações - Peso por país de origem'),
             dcc.Graph(id='pesopaises-graph',
                       figure=go.Figure(
                           graphs.update_pesopaises_graph())
                       )],
             className='six columns'),
         html.Div([html.H6('Histórico de importações - Peso por capítulo NCM'),
                   dcc.Graph(id='pesoncm-graph',
                             figure=go.Figure(
                                 graphs.update_pesoncm_graph())
                             )],
                  className='six columns')
     ]),
     html.H6('Histórico de importação -' +
             ' Relação entre número de Laudos e peso do NCM'),
     html.Div('Este gráfico mostra a relação entre histórico de movimentação'
              ' por peso na importação e quantidade de Laudos. Pontos abaixo'
              ' da linha têm uma baixa relação de laudos por histórico de'
              ' movimentação medido em total de peso importado. O tamanho da'
              ' esfera representa o valor médio da importações. Clique em um'
              ' ponto para ter mais informações sobre este NCM'),
     html.Div([
         html.Div(dcc.Graph(id='ncmlaudos-graph',
                            figure=go.Figure(graphs.graph_ncmlaudos())
                            ),
                  className='seven columns'),
         html.Div(dcc.Graph(id='valorncm-graph'),
                  className='five columns'),
     ])
     ],
    style=style
)


@app.callback(
    Output('valorncm-graph', 'figure'),
    [Input('ncmlaudos-graph', 'hoverData')])
def update_valorncm_graph(hoverData):
    oncm = None
    for point in hoverData['points']:
        if point.get('text'):
            oncm = point.get('text')
    layout = go.Layout(
        title='Valores US$/kg do capítulo NCM',
        xaxis=dict(
            title='US$/kg capítulo ' + str(oncm)
        ),
        yaxis=dict(
            title='Qtde adições'
        ),
        margin={'l': 50, 'r': 40, 't': 70, 'b': 70})
    data = []
    if oncm:
        data.append(go.Histogram({
            'x': ncm.dict_valorncm[oncm],
            'name': str(oncm),
            # 'histnorm': 'probability'
        }))
    return {
        'data': data,
        'layout': layout
    }
