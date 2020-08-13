import asyncore
import asynchat

from pprint import pprint as pp

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


# Prevents user from going off sandbox
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

    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b"\r\n\r\n")
        self.received_data = []
        self.headers_are_read = False
        
        self.responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
            'Bad request syntax or unsupported method'),
        403: ('Forbidden',
            'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
            'Specified method is invalid for this resource.'),
    }

    def collect_incoming_data(self, data):
        # print(f"Incoming data: {data[:6]}...")
        self.received_data.append(data)

    def found_terminator(self):
        self.parse_request(b"".join(self.received_data))

    def parse_request(self, raw_request):
        
           
        print('\n\n++ checking headers')
        if not self.headers_are_read:
            print(' ++ headers are not read')
            self.headers_are_read = True
            self.request = HTTPRequest(raw_request)
            
            # Mainly error 400
            if self.request.error_code:
                self.send_error(self.request.error_code, self.request.error_message)
                self.handle_close()
                
            if self.request.command == 'POST':
                print('  ++ command == POST')
                # Read additional bytes of the request, that amounts to length of the content (body)
                if 'Content-Length' in self.request.headers:
                    content_length = int(self.request.headers.get('Content-Length'))
                    self.set_terminator(content_length)
                        
                else:
                    self.set_terminator(None) # browsers sometimes over-send
                    self.handle_request(self.request.command)
            else:
                print('  ++ command is not POST')
                
                self.set_terminator(None) # browsers sometimes over-send
                self.handle_request(self.request.command)
        else:
            print(' ++ headers are read')
            # Extract the body of the request
            content_length = int(self.request.headers.get('Content-Length'))
            self.request.body = raw_request[len(raw_request)-content_length:].decode("utf-8")
            
            self.set_terminator(None) # browsers sometimes over-send
            self.handle_request(self.request.command)
    
    def get_size(self, file):
        """ Returns size of the opened file in bytes """
        prev_pos = file.tell()
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(prev_pos)
        return size
    
    def handle_url(self):
        
        raw_url = './public' + url_normalize(self.request.path)
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
            print(' ++ sent error 404 (not found) ')
            
            self.send_error(404)
            self.handle_close()
            return
        
        # Correct attempt to open directory as file
        except PermissionError:
            print(' ++ permission error. attempting something... ')
            index_file_found = False
            for index_file in ['index.html', 'index.htm', 'page.html', 'page.htm']:
                index_path = url + index_file
                if os.path.exists(index_path):
                    url = index_path
                    
                    f = open(url, 'rb')
                    index_file_found = True
                    print('  ++ success')
                    break
                
            if not index_file_found:
                print('  ++ fail')
                self.send_error(403)
                self.handle_close()
                return
        
        file_metadata = {
            'file': f,
            'size': self.get_size(f),
            'guessed_type': mimetypes.guess_type(url)[0],
            'last_modified': os.stat(url)
        }
        
        return file_metadata
    
    
    def do_GET(self):
        print(' ++ do_GET is called')
                
        # For some reason in my windows registry mime type
        # of .js is defined as text/plain (???)
        #
        #   >>> print(mimetypes.guess_type('hello.js'))
        #   ('text/plain', None)
        
        
        url, queries = self.handle_url()
        
        file_metadata = self.handle_open(url)
        
        # Abort if file wasn't opened successfully
        if file_metadata == None:
            return
            
        producer = FileProducer(file_metadata['file'])
        
        self.send_response(200, 'OK')
        self.send_header('Date', self.date_time_string())
        self.send_header('Server', 'Asyncore_server')
        self.send_header('Last-Modified', file_metadata['last_modified'])
        self.send_header('Content-Length', file_metadata['size'])
        self.send_header('Content-Type', file_metadata['guessed_type'])
        self.send_header('Connection', 'close')
        self.end_headers()
        
        self.push_with_producer(producer)
        self.handle_close()
        
    
    
    def date_time_string(self):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return format_date_time(stamp)
        
    def do_HEAD(self):
        print(' ++ do_HEAD is called')
        
        url, _ = self.handle_url()
        
        file_metadata = self.handle_open(url)
        
        # Abort if file wasn't opened successfully
        if file_metadata == None:
            return

        
        self.send_response(200, 'OK')
        self.send_header('Date', self.date_time_string())
        self.send_header('Server', 'Asyncore_server')
        self.send_header('Last-Modified', file_metadata['last_modified'])
        self.send_header('Content-Length', file_metadata['size'])
        self.send_header('Content-Type', file_metadata['guessed_type'])
        self.send_header('Connection', 'close')
        self.end_headers()
        
        self.handle_close()
        
    def do_POST(self):
        print(' ++ do_POST is called')
        
        url, _ = self.handle_url()
        queries = parse_qs(self.request.body)
        
        file_metadata = self.handle_open(url)
        
        # Abort if file wasn't opened successfully
        if file_metadata == None:
            return
        
            
        producer = FileProducer(file_metadata['file'])
        
        self.send_response(200, 'OK')
        self.send_header('Date', self.date_time_string())
        self.send_header('Server', 'Asyncore_server')
        self.send_header('Last-Modified', file_metadata['last_modified'])
        self.send_header('Content-Length', file_metadata['size'])
        self.send_header('Content-Type', file_metadata['guessed_type'])
        self.send_header('Connection', 'close')
        self.end_headers()
        
        self.push_with_producer(producer)
        self.handle_close()
        
        
    # Calls do_POST, do_GET... depending on request
    def handle_request(self, method):
        print('\n\n++ handling request (??)')
        method_name = 'do_' + method
        if not hasattr(self, method_name):
            print(' ++ sent error 405 (not allowed method)')
            self.send_error(405)
            self.handle_close()
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

        body = f'<html><body><h1>{code}</h1> <h3>{message}</h3></body></html>'.encode("utf-8")
        
        self.send_response(code, message)
        self.send_header('Date', self.date_time_string())
        self.send_header('Server', 'Asyncore_server')
        self.send_header('Content-Length', len(body))
        self.send_header("Connection", "close")
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.push(body)
        self.handle_close()
    
    
    def send_header(self, keyword, value):
        print('  ++ send_header is called')
        self.push(f'{keyword}: {value}\r\n'.encode("utf-8"))
        self.handle_close()
    
    def end_headers(self):
        print('  ++ end_headers is called')
        self.push(f'\r\n'.encode("utf-8"))
    
    def send_response(self, code, message=None):
        print('  ++ send_response is called')
        self.push(f'HTTP/1.1 {code} {message}\r\n'.encode("utf-8"))
        
    def handle_close(self):
        self.close_when_done()
    
class AsyncHTTPServer(asyncore.dispatcher):

    def __init__(self, host="", port=8181):
        super().__init__()
        self.create_socket()
        
        # Make so you don't have to wait for shutdown of socket from previous use
        self.set_reuse_addr()
        # Set host IP and port 
        self.bind((host, port))
        # Listen for N clients at a time
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print(f"Incoming connection from {addr}")
        AsyncHTTPRequestHandler(sock)

    # def handle_close(self)
    #     self.close()


server = AsyncHTTPServer()
try:
    asyncore.loop(timeout=0.5)
except KeyboardInterrupt:
    print("Crtl+C pressed. Shutting down.")