#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import cgi
sys.path.insert(1, '../python-lib/')

print("Content-Type: text/html; charset=UTF-8\n")

query_fields = cgi.FieldStorage()
print(type(query_fields))
if len(query_fields) > 1:
    for key in query_fields:
        print(key + "=" + str(query_fields[key].value))
