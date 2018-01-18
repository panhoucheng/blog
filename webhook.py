#!/usr/bin/env python
# coding=utf-8
from wsgiref.simple_server import make_server
import os


def application(environ, start_response):
    if environ['PATH_INFO'] == '/webhook/key/xxblog':
        start_response('200 OK', [('Content-Type', 'text/html')])
        os.system('/mnt/blog/build.sh')
        print('update success.')
        return [b'success, web hook!']
    else:
        start_response('403 Error', [('Content-Type', 'text/html')])
        return [b'error, key wrong!']


httpd = make_server('127.0.0.1', 18000, application)
print('Serving HTTP on port 8000...')
httpd.serve_forever()