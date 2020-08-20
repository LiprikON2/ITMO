## Async web server built with asyncore and asynchat

### Running
```
python asynchat_server.py
```
### Optional arguments:
`-h, --help`
`--host HOST` (default '')
`--port PORT` (default 8181)
`--log LOGLEVEL` (default INFO)
`--logfile LOGFILE` (default None)
`-w NWORKERS` (default 1)
`-r DOCUMENT_ROOT` (default './public)
## WSGI server

### Running
```
python wsgi_server.py wsgi_app:application
```

## Tests

### Testing functionality
1. Launch server on localhost:8181
2. Run `python test_async_server.py`


### Stress testing
1. Install locust
2. Launch server
3. Run `python locust.py`
4. Go to locust GUI: [localhost:8089](http://localhost:8089/)
