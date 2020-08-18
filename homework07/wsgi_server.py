import io
import socket
import sys

# For coloring console text
from bcolors import bcolors

# WSGI server inherits from asynchat_server.py classes
from asynchat_server import AsyncHTTPServer, AsyncHTTPRequestHandler


# class AsyncWSGIServer(httpd.AsyncServer):
class AsyncWSGIServer(AsyncHTTPServer):

    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_address)
        # Activate
        listen_socket.listen(5)
        # Get server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # Return headers set by Web framework/Web application
        self.headers_set = []
        
    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


# class AsyncWSGIRequestHandler(httpd.AsyncHTTPRequestHandler):
class AsyncWSGIRequestHandler(AsyncHTTPRequestHandler):

    def get_environ(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        pass

    def handle_request(self):
        pass

    def finish_response(self, result):
        pass
    
def make_server(server_address, application):
    server = AsyncWSGIServer(server_address)
    server.set_app(application)
    return server

def get_link(host, port):
        if host == "":
            return f'{bcolors.OKBLUE}http://localhost:{port}{bcolors.ENDC}'
        else:
            return f'{bcolors.OKBLUE}http://{host}:{port}{bcolors.ENDC}'   

SERVER_ADDRESS = (HOST, PORT) = '', 8888

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Started server at {get_link(HOST, PORT)}')
    httpd.serve_forever()