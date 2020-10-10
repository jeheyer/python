#!/usr/bin/env python3

import os
import sys
import io
import json

def main():
    if 'REQUEST_METHOD' in os.environ:
        # Called via Web
        import cgi
        form = cgi.FieldStorage()
        print("Content-Type: text/json; charset=UTF-8\n")
        if os.environ.get('REQUEST_METHOD') == "POST":
            output = {}
            for key in form:
                output[key] = str(form[key].value)
            print(json.dumps(output))
        else:
            print("not a post")
    else:
        sys.exit("Call me via the web")            

if __name__ == "__main__":
    main()
    quit()
