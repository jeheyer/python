#!/usr/bin/env python3

import sys

def GetIP():

    import os
    from ip_utils import GetClientIP
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
        if len(sys.argv) > 1:
            return sys.argv[1]
        else:
            sys.exit("Must provide IP address as argument")

def main():

    import json

    sys.path.insert(1, 'lib/')
    from geoip import GeoIP
    from ip_utils import GetClientIP
    ipv4_address = GetIP()
    geo_ip = GeoIP(ipv4_address)
    print("Content-Type: application/json; charset=UTF-8\n")
    print(json.dumps(vars(geo_ip), indent=3))

if __name__ == "__main__":

    sys.stderr = sys.stdout

    try:
        main()

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain\n\n{}".format(e))

    sys.exit()
