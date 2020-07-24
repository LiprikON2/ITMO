import socket 
from pprint import pprint as pp
infolist = socket.getaddrinfo('gatech.edu', 'www')
pp(infolist[0][0])
pp(socket.AF_INET)

pp(socket.getaddrinfo('localhost', 'smtp', 0, socket.SOCK_STREAM, 0))
pp('----')
pp(socket.getaddrinfo('iana.org', 'www', 0, socket.SOCK_STREAM, 0))