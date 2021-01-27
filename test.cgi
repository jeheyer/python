#!/usr/bin/env python

from __future__ import print_function
import sys

e = "an error occurred"
print("Status: 500\nContent-Type: text/plain\n\n{}".format(e))
