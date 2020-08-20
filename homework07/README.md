## Async web server built with asyncore and asynchat

### Running examples
```
python asynchat_server.py
```
```
curl -v localhost:8181
```
```
curl -v localhost:8181/dir1/space%20in%20name.txt
```

## WSGI server

### Running examples

#### 1.
```
python wsgi_server.py wsgi_app:application
```


#### 2.
> `pip install falcon`
```
python wsgi_server.py falcon_app:app
```
```
curl -v localhost:8181/quote
```

#### 3.
> `pip install pyramid`

```
python wsgi_server.py pyramid_app:app
```
```
curl -v localhost:8181/hello
```


## Optional arguments:
`-h, --help`

`--host HOST` (default is localhost)

`--port PORT` (default is 8181)

`--log LOGLEVEL` - e.g. CRITICAL, INFO (default is INFO)

`--logfile LOGFILE` (default is None)

`-w NWORKERS` - Number of workers i.e. processes (default is 1)

`-r DOCUMENT_ROOT` (default './public')

## Tests

### Curl

```
curl -v localhost:8181
```

```
curl -v -X HEAD localhost:8181 
```

```
curl -v -X POST -d "param1=value1&param2=value2" localhost:8181 
```



### Functionality testing
1. Launch server on localhost:8181
2. Run `python test_async_server.py`


### Stress testing
1. Install locust
2. Launch server:
```
python asynchat_server.py -w 50 --log critical
```
or

```
python wsgi_server.py wsgi_app:application -w 50 --log CRITICAL
```

3. Run locust:
```
locust -f locustfile.py --host=http://localhost:8181/
```
4. Go to the locust GUI: [localhost:8089](http://localhost:8089/)
