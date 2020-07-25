import asyncore
import asynchat

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
        self.requests = []
        self.headers_parsed = False

    def collect_incoming_data(self, data):
        # print(f"Incoming data: {data}")
        self._collect_incoming_data(data)
        self.requests.append(data)

    def found_terminator(self):
        self.parse_request(self.requests[0])

    def parse_request(self, raw_request):
        
        request = raw_request.decode('utf-8')
        print(request, '\n\n\n')
        
        
        request = request.splitlines()
        # Break down the request line into components
        (request_method,  # GET
         path,            # /hello
         request_version  # HTTP/1.1
        ) = request[0].split()
        
        (_, 
         host             # IP and port of a host  
        ) = request[1].split()
        
        (_,  
         connection # Connection (e.g: keep-alive)
        ) = request[2].split()
        
        (_,  
         max_age # Cache-Control
        ) = request[3].split()
        
        print('printing...')
        print(f'++{request_method}++{path}++{request_version}++')
        print(f'++{host}++')
        print(f'++{connection}++')
        print(f'++{max_age}++')

        if not self.headers_parsed:
            self.parse_headers()
            # if wrong headers 
            #   bad request 400
            if request_method == 'POST':
                if request.find('Content-Length'):
                    pass
                
    def parse_headers(self):
        self.headers_parsed = True
        
        
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