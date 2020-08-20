def application(env, start_response):
    start_response('200 OK', [('Content-Length', '11'), ('Content-Type', 'text/plain'),  ('Connection', 'close')])
    return [b'Hello World']