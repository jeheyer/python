#!/usr/bin/env python

from __future__ import print_function
import os
import cgi
import sys

sys.stderr = sys.stdout

print("Content-Type: text/html; charset=UTF-8\n")

print("<h2>HTTP Server Headers</h2>")
for n in ['SERVER_PROTOCOL', 'HTTP_HOST', 'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR', 'REQUEST_METHOD']:
    v =  os.environ.get(n, '')
    print(n + " = '" + v + "'<BR>")

method = os.environ.get('REQUEST_METHOD', 'GET')

if method == 'GET':
    print("GET GETGET IT")
    cgi.test()

if method == 'POST':
    print("GET GETGET IT")
    cgi.test()
