import io
import socket
import sys

# WSGI server inherits from asynchat_server.py classes
from asynchat_server import AsyncHTTPServer, AsyncHTTPRequestHandler


class AsyncWSGIRequestHandler(AsyncHTTPRequestHandler):

    def __init__(self, sock, host, port):
        super().__init__(sock, host=host, port=port)
        self.headers_set = []

    def get_environ(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = sys.stdin.buffer  #io.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request.command   # GET
        env['PATH_INFO']         = self.request.path      # /hello
        env['SERVER_NAME']       = self.host              # localhost
        env['SERVER_PORT']       = str(self.port)         # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', self.date_time_string()),
            ('Server', self.server_title),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def handle_request(self):
        # Construct environment dictionary using request data
        env = self.get_environ()

        # Hardcoded name of class instance (?)
        self.application = httpd.get_app()

        # Call application callable and get back a result that will become HTTP response body
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(result)

    def finish_response(self, result):

        [body] = result
        code, message = self.headers_set[0].split(' ')

        self.send_response(code, message=message)
        for header in self.headers_set[1]:
            keyword, value = header
            self.send_header(keyword, value)
        self.end_headers()
        self.push(body)

        self.close()


class AsyncWSGIServer(AsyncHTTPServer):

    def __init__(self, host='', port=8181, request_handler=AsyncWSGIRequestHandler):
        super().__init__(host=host, port=port, request_handler=request_handler)
        # # Return headers set by Web framework/Web application
        # self.headers_set = []

    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


def make_server(application, host='', port=8181):
    server = AsyncWSGIServer(host=host, port=port)
    server.set_app(application)

    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(
            'Provide a WSGI application object as module:callable (application file : name of its function)')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)  # wsgi_application.application

    # httpd - HTTP Daemon
    httpd = make_server(application, host='', port=8181)
    httpd.serve_forever()


# TODO
# - implement multiprocessing (call run)
# - Catch CTRL + C
# - Fix hardcoded name
# - Fix DOCUMENT_ROOT
