import asyncore
import asynchat
import multiprocessing

import logging
import argparse
import sys

# For HTTP request parse
from http.server import BaseHTTPRequestHandler
from io import BytesIO

# For HTTP response date time format (RFC 1123)
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

# For file management
import os

# For parsing GET queries
import urllib.parse as urlparse
from urllib.parse import parse_qs

# For determining mime media types to send in responses
import mimetypes

# For coloring console text
from bcolors import bcolors


# Prevents user from leaving sandbox
def url_normalize(path):
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1+3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    return path


# Splits file for transfer
class FileProducer(object):

    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


# For parsing http headers
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


class AsyncHTTPRequestHandler(asynchat.async_chat):
    """ Обработчик клиентских запросов """

    def __init__(self, sock, host=None, port=None, document_root='./public'):
        super().__init__(sock)

        self.server_title = 'Asyncore_server'
        self.host = host
        self.port = port
        self.document_root = document_root

        self.log = logging.getLogger(__name__)

        self.set_terminator(b"\r\n\r\n")
        self.received_data = []
        self.headers_are_read = False

    def collect_incoming_data(self, data):
        self.received_data.append(data)

    def found_terminator(self):
        self.parse_request(b"".join(self.received_data))

    def parse_request(self, raw_request):
        self.log.info('Parsing request')

        if not self.headers_are_read:
            self.headers_are_read = True
            self.request = HTTPRequest(raw_request)

            # Mainly error 400
            if self.request.error_code:
                self.log.info(f'Sent error {self.request.error_code}')
                self.send_error(self.request.error_code,
                                self.request.error_message)

            if self.request.command == 'POST':
                # Read additional bytes of the request, that amounts to length of the content (body)
                if 'Content-Length' in self.request.headers:
                    content_length = int(
                        self.request.headers.get('Content-Length'))
                    self.set_terminator(content_length)

                else:
                    self.set_terminator(None)  # browsers sometimes over-send
                    self.handle_request()
            else:
                self.set_terminator(None)  # browsers sometimes over-send
                self.handle_request()
        else:
            self.log.info('POST body detected. Extracting...')
            # Extract the body of the request
            content_length = int(self.request.headers.get('Content-Length'))
            self.request.body = raw_request[len(
                raw_request)-content_length:].decode("utf-8")

            self.set_terminator(None)  # browsers sometimes over-send
            self.handle_request()

    def get_size(self, file):
        """ Returns size of the opened file in bytes """
        prev_pos = file.tell()
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(prev_pos)
        return size

    def handle_url(self):

        # Provided in args. Default is './public'
        raw_url = self.document_root + url_normalize(self.request.path)

        # Parse GET queries
        parsed = urlparse.urlparse(raw_url)

        # Decode spaces
        url = parsed.path.replace('%20', ' ')

        queries = parse_qs(parsed.query)

        return (url, queries)

    def handle_open(self, url):

        try:
            # 'rb' (byte stream) for consistent prediction of content length
            f = open(url, 'rb')

        except FileNotFoundError:
            self.log.info('Sent error 404')

            self.send_error(404)
            return

        # Correct attempt to open directory as file
        except PermissionError:
            self.log.info('Attempting to find directory index file...')
            index_file_found = False
            for index_file in ['index.html', 'index.htm', 'page.html', 'page.htm']:
                index_path = url + index_file
                if os.path.exists(index_path):
                    url = index_path

                    f = open(url, 'rb')
                    index_file_found = True
                    self.log.info('...success')
                    break

            if not index_file_found:
                self.log.info('...fail. Sent error 403')
                self.send_error(403)
                return

        # For some reason in my windows registry mime type
        # of .js extension is defined as text/plain
        #
        #   >>> import mimetypes
        #   >>> mimetypes.guess_type('hello.js')
        #   ('text/plain', None)

        file_metadata = {
            'file': f,
            'size': self.get_size(f),
            'guessed_type': mimetypes.guess_type(url)[0],
            'last_modified': os.stat(url)
        }

        return file_metadata

    def do_GET(self):
        self.log.info('Processing GET request')

        url, queries = self.handle_url()

        file_metadata = self.handle_open(url)

        # Abort if file wasn't opened successfully
        if file_metadata == None:
            return

        producer = FileProducer(file_metadata['file'])

        self.send_response(200, 'OK')
        self.send_head(file_metadata['last_modified'],
                       file_metadata['size'], file_metadata['guessed_type'])

        self.push_with_producer(producer)
        self.handle_close()

    def date_time_string(self):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return format_date_time(stamp)

    def do_HEAD(self):
        self.log.info('Processing HEAD request')

        url, _ = self.handle_url()

        file_metadata = self.handle_open(url)

        # Abort if file wasn't opened successfully
        if file_metadata == None:
            return

        self.send_response(200, 'OK')
        self.send_head(file_metadata['last_modified'],
                       file_metadata['size'], file_metadata['guessed_type'])

        self.handle_close()

    def do_POST(self):
        self.log.info('Processing POST request')

        url, _ = self.handle_url()
        # Check for empty POST request
        if hasattr(self.request, 'body'):
            queries = parse_qs(self.request.body)

        file_metadata = self.handle_open(url)

        # Abort if file wasn't opened successfully
        if file_metadata == None:
            return

        producer = FileProducer(file_metadata['file'])

        self.send_response(200, 'OK')
        self.send_head(file_metadata['last_modified'],
                       file_metadata['size'], file_metadata['guessed_type'])

        self.push_with_producer(producer)
        self.handle_close()

    # Calls do_POST, do_GET... depending on request
    def handle_request(self):
        self.log.info('Handling request')
        method_name = 'do_' + self.request.command
        if not hasattr(self, method_name):
            self.log.info('Sent error 405')
            self.send_error(405)
            return
        handler = getattr(self, method_name)
        handler()

    def send_error(self, code, message=None):
        try:
            short_msg, long_msg = self.responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg

        body = f'<html><body><br><br><br><br><center><h1>{code}</h1> <h3>{message}</h3></center></body></html>'.encode(
            "utf-8")

        self.send_response(code, message)
        self.send_header('Date', self.date_time_string())
        self.send_header('Server', self.server_title)
        self.send_header('Content-Length', len(body))
        self.send_header("Content-Type", "text/html")
        self.send_header('Connection', 'close')

        self.end_headers()
        self.push(body)
        self.handle_close()

    def send_response(self, code, message=None):
        self.push(f'HTTP/1.1 {code} {message}\r\n'.encode("utf-8"))

    def send_header(self, keyword, value):
        self.push(f'{keyword}: {value}\r\n'.encode("utf-8"))

    def send_head(self, last_modified, content_length, content_type):
        self.send_header('Date', self.date_time_string())
        self.send_header('Server', self.server_title)
        self.send_header('Last-Modified', last_modified)
        self.send_header('Content-Length', content_length)
        self.send_header('Content-Type', content_type)
        self.send_header('Connection', 'close')
        self.end_headers()

    def end_headers(self):
        self.push(f'\r\n'.encode("utf-8"))

    # Waits for file producer before closing connection
    # Without this only part of the image will be sent
    def handle_close(self):
        self.close_when_done()

    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
    }


class AsyncHTTPServer(asyncore.dispatcher):

    def __init__(self, host="", port=8181, request_handler=AsyncHTTPRequestHandler, document_root='./public'):
        super().__init__()

        self.create_socket()
        # Make so you don't have to wait for shutdown of a socket from previous use
        self.set_reuse_addr()
        # Set host IP and port
        self.bind((host, port))
        # Listen for N clients at a time
        self.listen(5)

        self.request_handler = request_handler
        self.document_root = document_root

        link = self.get_link(host, port)
        print(f'Asynchat server online at {link}')

    def get_link(self, host, port):
        if host == "":
            return f'{bcolors.OKBLUE}http://localhost:{port}{bcolors.ENDC}'
        else:
            return f'{bcolors.OKBLUE}http://{host}:{port}{bcolors.ENDC}'

    def handle_accepted(self, sock, addr):
        print(f"Incoming connection from {addr}")
        self.request_handler(
            sock, host=addr[0], port=addr[1], document_root=self.document_root)

    def handle_close(self):
        self.close()

    def serve_forever(self, timeout=0.5):
        asyncore.loop(timeout=timeout)


def parse_args():

    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="")
    parser.add_argument("--port", dest="port", type=int, default=8181)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default="./public")

    return parser.parse_args()


def run(args):

    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")

    server = AsyncHTTPServer(
        host=args.host, port=args.port, document_root=args.document_root)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.handle_close()


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
