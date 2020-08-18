# from wsgi_server import AsyncWSGIServer, AsyncWSGIRequestHandler
from asynchat_server import AsyncHTTPServer

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello World']


# server = AsyncWSGIServer()
# server.set_app(application)

# server = AsyncHTTPServer(port=8123)
# server.serve_forever()