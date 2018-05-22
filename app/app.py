import dash

app = dash.Dash('Laudos DashBoard')
server = app.server
app.config.suppress_callback_exceptions = True

# To Serve static css if neeed (bootstrap??)


@app.server.route('/static/<path:path>')
def static_file(path):
    return app.server.send_from_directory('static', path)
