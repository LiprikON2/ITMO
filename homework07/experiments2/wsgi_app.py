from flask import Flask
from flask import Response
flask_app = Flask('wsgi_app')


@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain'
    )

app = flask_app.wsgi_app