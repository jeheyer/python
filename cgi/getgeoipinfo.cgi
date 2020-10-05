#!/usr/bin/env python3

import os
import sys
sys.path.insert(1, '../python-lib/')
from geoip import GeoIP
from ip_utils import GetClientIP
import json
import traceback

def GetIP():

    ipv4_address = None

    if 'REQUEST_METHOD' in os.environ:
        # Called via Web
        import cgi
        import cgitb
        cgitb.enable()
        fields = cgi.FieldStorage()
        uri = os.environ.get('REQUEST_URI', '/')
        if os.environ.get('REQUEST_METHOD') == "GET":
            if uri.startswith("/geoip/"):
                ipv4_address = uri.split("/")[2]
            if "ipv4_address" in fields:
                ipv4_address = str(fields["ipv4_address"].value)
            if ipv4_address and len(ipv4_address) >= 7:
                return ipv4_address
            else:
                return GetClientIP()
        elif os.environ.get('REQUEST_METHOD') == "POST":
            return "192.168.1.1"
        else:
            sys.exit("METHOD NOT SUPPORTED")

    else:
        # Running via CLI
        try:
            ipv4_address = sys.argv[1]
        except:
            sys.exit("Must provide IP address as argument")
        return ipv4_address

def main():

    sys.stderr = sys.stdout

    try:
        ipv4_address = GetIP()
        geo_ip = GeoIP(ipv4_address)
        print("Content-Type: application/json; charset=UTF-8\n")
        print(json.dumps(vars(geo_ip), indent=3))

    except:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        exc = traceback.format_exc()
        print(exc)

if __name__ == "__main__":
    main()
    sys.exit()
