import dash_core_components as dcc
import dash_html_components as html

menu = \
html.Div([
    html.Ul([
        html.Li([
            dcc.Link('Resumo', href='/laudos_dash/apps/pag1')
        ]),
        html.Li([
            dcc.Link('Qtde anual/fatores', href='/laudos_dash/apps/pag2')
        ]),
        html.Li([
            dcc.Link('Tempos ano/mês fluxo', href='/laudos_dash/apps/pag3')
        ]),
        html.Li([
            dcc.Link('Análise NCM', href='/laudos_dash/apps/pag4')
        ]),
        html.Li([
            dcc.Link('Análise País', href='/laudos_dash/apps/pag5')
        ]),
        html.Li([
            dcc.Link('Atualizar dados', href='/laudos_dash/apps/pag6')
        ]),
    ], className='nav navbar-nav')
], className='navbar navbar-default navbar-static-top')

'''
menu = html.Div([
    html.Nav(className="nav nav-pills", children=[
        html.A('Resumo', className="nav-item nav-link btn", href='/laudos_dash/apps/pag1'),
        html.A('Stats Ano/mês', className="nav-item nav-link btn", href='/laudos_dash/apps/pag2'),
        html.A('Stats Ano/mês', className="nav-item nav-link btn", href='/laudos_dash/apps/pag3'),
        html.A('Análise NCM', className="nav-item nav-link btn", href='/laudos_dash/apps/pag4'),
        html.A('Análise País', className="nav-item nav-link btn", href='/laudos_dash/apps/pag5'),
    ]),
])

menu = html.Div([
    html.Div([
    html.Div('LAUDOS DASHBOARD',
             className='two columns'),
    html.Div(dcc.Link('Página inicial - resumo',
                      href='/apps/pag1'),
             className='two columns'),
    html.Div(dcc.Link('Estatísticas de quantidades por ano e mês',
                      href='/apps/pag2'),
             className='three columns'),
    html.Div(dcc.Link('Tempos do fluxo de trabalho por ano e mês',
                      href='/apps/pag3'),
             className='three columns'),
    html.Div('',
             className='two columns')],
    className='row',
    style={'font-size': '110%'}),
    html.Hr()]
)
'''

style = {'class': 'conteiner',
         'text-align': 'left',
         'border-radius': '10px',
         'margin': '50px'}
