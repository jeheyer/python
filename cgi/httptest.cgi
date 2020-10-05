#!/usr/bin/env python3 

import http.client

def main():
        conn = http.client.HTTPConnection("bitspring-email-assets.s3.amazonaws.com", 80, 3)
        conn.request("GET", "/uploads/logos/1363293870_ralogo.jpg")
        resp = conn.getresponse()
        status_code = resp.status
        content_type = resp.headers["Content-Type"]
        body = resp.read()
        conn.close()

if __name__ == "__main__":
    main()
    quit()

