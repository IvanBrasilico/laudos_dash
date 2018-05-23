import dash_core_components as dcc
import dash_html_components as html


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


style = {'class': 'conteiner',
         'text-align': 'left',
         'border-radius': '10px',
         'margin': '50px'}
