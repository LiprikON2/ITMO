import socket

def server(host, port):
    # Create TCP IPv4 internet socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Make so you don't have to wait for shutdown of socket from previous use
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # Set host IP and port 
    sock.bind((host, port))
    # Listen for N clients at a time
    sock.listen(1)
    
    while True:
        client_sock, client_address = sock.accept()
        print('Conection established to', client_address)
        
        data = client_sock.recv(4096)
        print('Recived', len(data), 'bytes of data') 
        if not data:
            break
        client_sock.sendall(data)
    client_sock.close()
        
def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
if __name__ == '__main__':
    server("", 80)
    client("", 80)