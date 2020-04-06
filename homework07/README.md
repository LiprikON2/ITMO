### TCP Singlethread
`python tcp_singlethread.py` - to launch server
`./nc.exe localhost 9090` - to connect to the server

### WEB Singlethread + locust
`python web_singlethread.py` - to launch server
`locust --host=http://127.0.0.1:9090/` - to launch locust
> `localhost:8089` - locust's web ui

### TCP Multithread
`python tcp_multithread.py` - to launch server
`./nc.exe localhost 9090` - run this and connect from multiple consoles
##### Result:
![](https://i.imgur.com/BfAtJpO.png)

### WEB Multithread + locust
`python web_multithread.py` - to launch server
`locust --host=http://127.0.0.1:9090/` - to launch locust

### TCP Thread pool
`python tcp_threadpool.py` - to launch server
`./nc.exe localhost 9090` - to connect to the server

### TCP Multiprocessing
`python tcp_mutliprocessing.py` - to launch server
`./nc.exe localhost 9090` - to connect to the server

### TCP Non-blocking. Multiplexing (with select)
`python tcp_multiplexing.py` - to lauch server
`./nc.exe localhost 9090` - to connect to the server



### Misc

`netstat` - to see the current state of sockets on your host