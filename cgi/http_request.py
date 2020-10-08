#!/usr/bin/env python3
    
def main():
    import http.client
    import ssl
    import sys

    conn = http.client.HTTPSConnection("www.hightail.com", port = 443, timeout = 3, context = ssl._create_unverified_context())
    #conn.request("GET", "/en_US/theme_default/images/hightop_250px.png")
    #conn.request("GET", "/")
    conn.request("GET", "/login.php")
    resp = conn.getresponse()

    if 301 <= resp.status <= 302:
        print("Status: {}\nLocation: {}".format(resp.status, resp.headers['Location']))
    else:
        print("Status: {}\nContent-Type: {}\n".format(resp.status, resp.headers['Content-Type']))
    body = resp.read()

    if type(body) == str:
        print("{}\n".format(body))
    else:
        # Output binary
        sys.stdout.flush()
        sys.stdout.buffer.write(body)

def main2():
    import requests
    url = "https://api.j5.org"
    try:
        status_code = 400
        resp = requests.get(url, params, timeout = 5)
        if resp.status_code:
            status_code = resp.status_code
        if resp.headers['Content-Type']:
            content_type =  resp.headers['Content-Type']
        if 301 < status_code < 302:
            body = None
        else:
            body = resp._content
        print(content_type)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
