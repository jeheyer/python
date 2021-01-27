#!/usr/bin/env python3

import sys

def main():

    import os
    import re
    import json
    sys.path.insert(1, 'lib/')
    from logfile import LogFile

    if 'REQUEST_METHOD' in os.environ:
        # Running via CGI
        import cgi
        #import cgitb
        #cgitb.enable()
        form = cgi.FieldStorage()
        hostname = os.environ.get('HTTP_HOST', 'localhost')
        uri = os.environ.get('REQUEST_URI', '/')
        if "token" in form:
            token = str(form["token"].value)
        if "tokens." in hostname:
            token = uri.split("/")[1]
        if "/token/" in uri:
            token = uri.split("/")[2]
    else:
        if len(sys.argv) > 1:
            token = sys.argv[1]
        else:
            sys.exit("Must provide token as argument")

    assert len(token) >= 4, "Invalid token"
 
    try:
        # Override if this is test token
        if token == "testing1234":
            dns_resolvers = [ "192.0.2.53", "198.51.100.53", "203.0.113.53" ]
        else:
            # Open the BIND log file for A record queries
            dns_resolvers = []
            dns_resolvers_hash = dict()
            bind_log_file = LogFile("/var/log/named/query.log", " IN A ")
            for line in bind_log_file.contents:
                if token in line[7]:
                    source_ip, source_port = line[6].split("#")
                    if not re.match("10.|192.168.", source_ip) and source_ip not in dns_resolvers_hash:
                        dns_resolvers_hash[source_ip] = True
                        dns_resolvers.append(source_ip)
        print("Content-Type: application/json; charset=UTF-8\n")

        # Print DNS resolvers
        print("{\n  \"token\": \"" + token + "\",\n  \"dns_resolvers\": [", end = "")
        for dns_resolver in dns_resolvers:
            print(" \"" + dns_resolver + "\"", end = "")
            if dns_resolver is not dns_resolvers[-1]:
                 print(",", end = "")
        print(" ]\n}")

    except:
        exc = traceback.format_exc()
        return(exc)

if __name__ == "__main__":

    sys.stderr = sys.stdout
    import traceback

    try:
        main()

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n\n{}".format(e))

    sys.exit()
