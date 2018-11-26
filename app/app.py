import dash

app = dash.Dash('Laudos DashBoard', url_base_pathname='/laudos_dash/')
server = app.server
app.config.suppress_callback_exceptions = True

# To Serve static css if neeed (bootstrap??)
app.css.append_css({"external_url": [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
]})

@app.server.route('/static/<path:path>')
def static_file(path):
    return app.server.send_from_directory('static', path)
