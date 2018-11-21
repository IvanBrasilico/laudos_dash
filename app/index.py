import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import abort

from app.app import app
from app.apps import app1, app2, app3, app4, app5
from importlib import reload
from app.datasources import laudos

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # interval=3*3600*1000), # Refresh em 3h
    html.Div(id='page-content'),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname in ['/laudos_dash/', '/index']:
        return app1.layout
    if pathname == '/laudos_dash/apps/pag1':
        return app1.layout
    if pathname == '/laudos_dash/apps/pag2':
        return app2.layout
    if pathname == '/laudos_dash/apps/pag3':
        return app3.layout
    if pathname == '/laudos_dash/apps/pag4':
        return app4.layout
    if pathname == '/laudos_dash/apps/pag5':
        return app5.layout
    if pathname == '/laudos_dash/apps/pag6':
        reload(laudos)
        reload(app1)
        reload(app4)
        reload(app5)
        return app1.layout
    return abort(404)


app.css.append_css(
    {'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=True)
