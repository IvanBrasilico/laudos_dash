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
     html.Div([
         html.Div([html.H6(
             'Histórico de importações - Peso por país de origem'),
             dcc.Graph(id='pesopaises-graph',
                       figure=go.Figure(
                           graphs.update_pesopaises_graph())
                       )],
             className='six columns'),
         html.Div([
             html.Div([html.H6('Histórico de importações - Discordância por país de origem'),
                       dcc.Graph(id='discordanciapais-graph',
                                 figure=go.Figure(
                                     graphs.update_discordanciapais_graph())
                                 )],
                      className='six columns')
         ]),
     ]),
     html.H6('Histórico de importação -' +
             ' Relação entre número de Laudos e peso do país'),
     html.Div('Este gráfico mostra a relação entre histórico de movimentação'
              ' por peso na importação e quantidade de Laudos. Pontos abaixo'
              ' da linha têm uma baixa relação de laudos por histórico de'
              ' movimentação medido em total de peso importado. O tamanho da'
              ' esfera representa o valor médio da importações. Clique em um'
              ' ponto para ter mais informações sobre este país'),
     html.Div([
         html.Div(dcc.Graph(id='paiseslaudos-graph',
                            figure=go.Figure(graphs.graph_paislaudos())
                            ),
                  className='eight columns'),
         html.Div(dcc.Graph(id='paisncm-graph'),
                  className='four columns'),
     ])
     ],
    style=style
)


@app.callback(
    Output('paisncm-graph', 'figure'),
    [Input('paiseslaudos-graph', 'hoverData')])
def update_paisncm_graph(hoverData):
    opais = None
    for point in hoverData['points']:
        if point.get('text'):
            opais = point.get('text')
    layout = go.Layout(
        title='Peso do capítulo NCM na importação do país',
        xaxis=dict(
            type='category', title='Capítulo NCM ' + str(opais)
        ),
        yaxis=dict(
            title='Peso total'
        ),
        margin={'l': 50, 'r': 40, 't': 70, 'b': 70})
    data = []
    if opais:
        codpais = ncm.df_pais_x_peso.loc[ncm.df_pais_x_peso['PaisOrigem']
                                         == opais]['codpais'].values[0]
        df_filtered = ncm.df_pesoncmpais[ncm.df_pesoncmpais['codpais'] == codpais]
        df_filtered['pesototal'] = df_filtered['pesototal'] / \
                                   df_filtered['pesototal'].sum()
        # print('##########', codpais)
        # print('##########', df_filtered)
        data.append(go.Bar({
            'y': df_filtered['pesototal'],
            'x': df_filtered['codcapncm'],
            'name': opais,
            # 'histnorm': 'probability'
        }))
    return {
        'data': data,
        'layout': layout
    }
