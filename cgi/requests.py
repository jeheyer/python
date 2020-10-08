#!/usr/bin/env python3

import requests
import json

URL = "https://j5.org/66.170.1.10"
r = requests.get(url = URL, params = {}) 
data = r.json() 
