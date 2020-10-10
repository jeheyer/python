#!/usr/bin/env python3
    
def main2():
    import http.client
    import ssl
    import sys

    conn = http.client.HTTPSConnection("www.hightail.com", port = 443, timeout = 3, context = ssl._create_unverified_context())
    conn.request("GET", "/en_US/theme_default/images/hightop_250px.png")
    #conn.request("GET", "/")
    #conn.request("GET", "/login.php")
    resp = conn.getresponse()

    if 301 <= resp.status <= 302:
        print("Status: {}\nLocation: {}\n".format(resp.status, resp.headers['Location']))
    else:
        print("Status: {}\nContent-Type: {}\n".format(resp.status, resp.headers['Content-Type']))
    body = resp.read()

    if type(body) == str:
        print("{}\n".format(body))
    else:
        # Output binary
        sys.stdout.flush()
        sys.stdout.buffer.write(body)

def main():

    import requests
    import sys

    url = "https://www.hightail.com/uploads/logos/asdlkj"
    try:
        resp = requests.get(url, params = {}, timeout = 5, allow_redirects = False)
        if 301 <= resp.status_code <= 302:
            print("Status: {}\nLocation: {}\n".format(resp.status_code, resp.headers['Location']))
        else:
            print("Status: {}\nContent-Type: {}\n".format(resp.status_code, resp.headers['Content-Type']))
        #if resp.headers['Content-Type'].startswith("text"):
        #    print("{}\n".format(resp.text))
        #else:
        sys.stdout.flush()
        sys.stdout.buffer.write(resp._content)

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain\n\n{}".format(e))

if __name__ == "__main__":
    main()
