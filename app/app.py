import dash
from flask import send_from_directory
import os

app = dash.Dash('Laudos DashBoard', url_base_pathname='/laudos_dash/')
server = app.server
app.config.suppress_callback_exceptions = True

# To Serve static css if neeed (bootstrap??)
app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.server.route('/laudos_dash/static/<path:path>')
@app.server.route('/static/<path:path>')
def static_file(path):
    if not os.path.exists(os.path.join(STATIC_PATH, path)):
        print('***PATH NOT EXISTS path:%s - file:%s' %
              (STATIC_PATH, path))
    return send_from_directory(STATIC_PATH, path)
