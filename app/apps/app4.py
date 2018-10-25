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
     html.H1('Análise de NCM - Histórico de importações', style={'text-align': 'center'}),
     html.Div(
         'O objetivo é poder comparar o histórico de importações com'
         ' os dados do sistema Laudos. ' + ncm.datancm.descricao),
     html.Div([
         html.Div([html.H6('Histórico de importações - Peso por capítulo NCM'),
                   dcc.Graph(id='pesoncm-graph',
                             figure=go.Figure(
                                 graphs.update_pesoncm_graph())
                             )],
                  className='six columns'),
         html.Div([
             html.Div([html.H6('Histórico de importações - Discordância por capítulo NCM'),
                       dcc.Graph(id='discordanciancm-graph',
                                 figure=go.Figure(
                                     graphs.update_discordanciancm_graph())
                                 )],
                      className='six columns')
         ]),
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
         dcc.Dropdown(
             id='cap_ncm',
             options=ncm.cap_ncm,
             value=[],
             multi=True
         )
     ]),
     html.Div([

         html.Div(dcc.Graph(id='ncmlaudos-graph',
                            # figure=go.Figure(graphs.graph_ncmlaudos())
                            ),
                  className='eight columns'),
         html.Div(dcc.Graph(id='valorncm-graph'),
                  className='four columns'),
     ]),
     ],
    style=style
)


@app.callback(
    Output('ncmlaudos-graph', 'figure'),
    [Input('cap_ncm', 'value')])
def update_ncmlaudos_graph(capncm_value):
    layout = go.Layout(yaxis=dict(title='Laudos (qtde)'),
                       xaxis=dict(title='Importações (%peso)'),
                       margin={'l': 80, 'r': 0, 't': 20, 'b': 80},
                       width=800)
    data = []
    print('capncm_value', capncm_value)
    df_filtered = ncm.df_laudos_x_peso
    print(df_filtered)
    if capncm_value:
        df_filtered = df_filtered[df_filtered['codcapncm'].isin(capncm_value)]
    print('filtered', df_filtered)
    peso_ncm = df_filtered['pesototal'] * 100
    qtde_laudos = df_filtered['total']
    caps_ncm = df_filtered['codcapncm']
    sizes = graphs.markers_size_por_valor(df_filtered['codcapncm'])
    max_peso = peso_ncm.max()
    qtde_total = qtde_laudos.sum()
    ratio = qtde_total / 100
    colors = graphs.colors_por_ratio(peso_ncm, qtde_laudos, ratio)
    diagx = []
    diagy = []
    for r in range(int(max_peso)):
        diagx.append(r)
        diagy.append(r * ratio)
    data.append(go.Scatter({
        'x': ['%.2f' % peso for peso in peso_ncm],
        'y': qtde_laudos,
        'text': caps_ncm,
        'name': 'Imp. x Laudos',
        'mode': 'markers',
        'marker': {'size': sizes, 'color': colors}
    }))
    data.append(go.Scatter({
        'x': diagx,
        'y': diagy,
        'name': 'Equilíbrio'
    }))
    return {
        'data': data,
        'layout': layout
    }


@app.callback(
    Output('valorncm-graph', 'figure'),
    [Input('ncmlaudos-graph', 'hoverData')])
def update_valorncm_graph(hoverData):
    oncm = None
    for point in hoverData['points']:
        if point.get('text'):
            oncm = point.get('text')
    data = []
    layout = []
    if oncm:
        dftitlex = ncm.df_ncm[ncm.df_ncm['COD CAPIT NCM'] == oncm]['CAPITULO NCM']
        if dftitlex.count() > 0:
            titlex = dftitlex.tolist()[0]
        print(titlex)
        layout = go.Layout(
            title='Valores US$/kg do capítulo NCM %d - média %.2f' %
                  (oncm, ncm.dict_valorncm[oncm].mean()),
            xaxis=dict(
                title=titlex
            ),
            yaxis=dict(
                title='Qtde adições'
            ),
            margin={'l': 50, 'r': 40, 't': 70, 'b': 70})
        data.append(go.Histogram({
            'x': ncm.dict_valorncm[oncm],
            'name': str(oncm),
            # 'histnorm': 'probability'
        }))
    return {
        'data': data,
        'layout': layout
    }
