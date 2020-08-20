import multiprocessing

import logging
import argparse
import sys
import io

# WSGI server inherits from asynchat_server.py classes
from asynchat_server import AsyncHTTPServer, AsyncHTTPRequestHandler

# For coloring console text
from bcolors import bcolors


class AsyncWSGIRequestHandler(AsyncHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        env['wsgi.input']        = io.BytesIO(self.request.body)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = True
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request.command   # GET
        env['PATH_INFO']         = self.request.path      # /hello
        env['SERVER_NAME']       = self.host              # localhost
        env['SERVER_PORT']       = str(self.port)         # 8888
        
        env['QUERY_STRING']      = self.query_string
        env['SCRIPT_NAME']       = ''
        return env

    def start_response(self, status, response_headers, exc_info=None):
        self.log.info(f'Starting response')
        server_headers = [
            ('Date', self.date_time_string()),
            ('Server', self.server_title),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def handle_request(self):
        self.log.info(f'Handling request')

        self.url, self.query_string = self.handle_url()
        
        # Construct environment dictionary using request data
        env = self.get_environ()

        # Hardcoded name of class instance (?)
        self.application = httpd.get_app()

        # Call application callable and get back a result that will become HTTP response body
        response_body = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(response_body)

    def finish_response(self, response_body):
        self.log.info(f'Finishing response')

        merged_body = b''.join(x for x in response_body)
        
        code = int(self.headers_set[0][:3])
        message = self.headers_set[0][4:]

        self.send_response(code, message=message)
        for header in self.headers_set[1]:
            keyword, value = header
            self.send_header(keyword, value)
        self.end_headers()
        self.push(merged_body)

        self.handle_close()


class AsyncWSGIServer(AsyncHTTPServer):

    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


def make_server(application, host, port, document_root):
    server = AsyncWSGIServer(
        host=host, port=port, request_handler=AsyncWSGIRequestHandler, document_root=document_root)
    server.set_app(application)

    return server


def parse_args():

    parser = argparse.ArgumentParser("Simple asynchronous WSGI web-server")
    parser.add_argument(
        'wsgi_obj', help='WSGI application object - module:callable')
    parser.add_argument("--host", dest="host", default="",
                        help='Default is localhost')
    parser.add_argument("--port", dest="port", type=int,
                        default=8181, help='Default is 8181')
    parser.add_argument("--log", dest="loglevel",
                        default="info", help='e.g. CRITICAL, INFO')
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int,
                        default=1, help='Number of workers (processes)')
    parser.add_argument("-r", dest="document_root", default="./public")

    return parser.parse_args()


def run(args):

    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")

    module, application = args.wsgi_obj.split(':')

    module = __import__(module)
    application = getattr(module, application)

    global httpd
    httpd = make_server(application, host=args.host, port=args.port,
                        document_root=args.document_root)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.handle_close()


if __name__ == "__main__":

    args = parse_args()

    for _ in range(args.nworkers):

        try:
            p = multiprocessing.Process(target=run, args=(args,))
            p.start()
            p.join()
        except KeyboardInterrupt:
            print(f'{bcolors.WARNING}Crtl+C pressed. Shutting down.{bcolors.ENDC}')
            sys.exit(0)
