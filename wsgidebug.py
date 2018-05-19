import os
os.environ['DEBUG'] = '1'

from app.index import app

if __name__ == '__main__':
    app.run_server(debug=True)