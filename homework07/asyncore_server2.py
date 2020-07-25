import asyncore
import asynchat

from pprint import pprint as pp

# For HTTP parse
from http.server import BaseHTTPRequestHandler
from io import BytesIO

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
        self.buffer = []
        self.headers_are_read = False

    def collect_incoming_data(self, data):
        print(f"Incoming data: {data[:6]}...")
        self.buffer.append(data)

    def found_terminator(self):
        self.parse_request(b"".join(self.buffer))

    def parse_request(self, raw_request):
        
        request = HTTPRequest(raw_request)
           
        
        
    

        if not self.headers_are_read:
            self.headers_are_read = True
            if request.error_code == '400':
                self.send_error(400)
                self.handle_close()
                
            if request.command == 'POST':
                if 'Content-Length' in request.headers:
                    content_length = int(request.headers.get('Content-Length'))
                    self.set_terminator(content_length)
                        
                else:
                    # self.set_terminator(None)
                    self.handle_request()
            else:
                self.handle_request()
        else:
            content_length = int(request.headers.get('Content-Length'))
            body = raw_request[len(raw_request)-content_length:]
            print(body)
            
            
    def do_POST(self):
        print('why am i (do_POST) called??')
        
    def handle_request(self):
        print('handling request (??)')
        method_name = 'do_' + self.method
        if not hasattr(self, method_name):
            self.send_error(405)
            self.handle_close()
            return
        handler = getattr(self, method_name)
        handler()
        pass

    def send_error(self, code, message=None):
        pass
    
    def
        
class AsyncHTTPServer(asyncore.dispatcher):

    def __init__(self, host="", port=8080):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print(f"Incoming connection from {addr}")
        AsyncHTTPRequestHandler(sock)





server = AsyncHTTPServer()
asyncore.loop()