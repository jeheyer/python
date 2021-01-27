#!/usr/bin/env python

import sys

e = "an error occurred"
print("Status: 500\nContent-Type: text/plain\n\n{}".format(e))
