#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

def GetEnvironment(hostname):

    # Pre-Preduction
    if ".htspaces.com" in hostname or "stage.yousendit.com" in hostname:
        if "stage." in hostname:
            return "stage"
        else:
            return hostname.split(".")[1]
    # John Home Test env
    elif "j5.org" in hostname:
        return "j5"
    else:
        return "prod"

def GetWWWURL(env = "prod", new_path = "/"):

    if env == "prod":
        www_host = "www.hightail.com"
    elif env == "j5":
        www_host = "www.htl.j5.org"
    else:
        www_host = "www." + env + ".htspaces.com"

    return { 'status_code': 301, 'location': "https://" + www_host + new_path }

def GetSpacesURL(env = "prod", **options):

    if env == "prod":
        spaces_web_host = "spaces.hightail.com"
    elif env == "j5":
        spaces_web_host = "spaces.hightail.com"
    else:
        spaces_web_host = "spaces." + env + ".htspaces.com"

    # 1.0 to Spaces transition
    if 'new_path' in options:
        new_path = options['new_path']
        if options['new_path'].startswith("/corp-login"):
            if 'email' in options:
                new_path += "?email=" + options['email']
            if 'caller' in options:
                new_path += "&caller=" + options['caller']

    # Downloads
    if 'ufid' in options:
        ufid = options['ufid']
        if len(ufid) < 16:
            return { 'status_code': 400, 'body': "Invalid UFID '{}'".format(ufid) }
        new_path = "/resolve/ufid/" + ufid
    if 'batch_id' in options:
        batch_id = options['batch_id']
        if len(batch_id) < 22:
            return { 'status_code': 400, 'body': "Invalid Batch ID '{}'".format(batch_id) }
        new_path = "/resolve/download/" + batch_id

    # Uplink
    if 'uplink_name' in options:
        new_path = "/resolve/u/" + options['uplink_name']

    # Send
    if 'send_id' in options and 'email_id' in options:
        send_id = options['send_id']
        email_id = options['email_id']
        if len(send_id) < 9: 
            return { 'status_code': 400, 'body': "Invalid Send ID '{}'".format(send_id) }
        if len(email_id) != 32: 
            return { 'status_code': 400, 'body': "Invalid Email ID '{}'".format(email_id) }
        new_path = "/resolve/" + send_id + "/" + email_id

    # Shared Folder
    if 'share_id' in options:
        share_id = options['share_id']
        if len(share_id) != 43:
            return { 'status_code': 400, 'body': "Invalid Shared Folder ID '{}'".format(share_id) }
        new_path = "/share-accept/" + share_id
        if 'sharee' in options:
            sharee = options['sharee']
            if not "@" in sharee:
                return { 'status_code': 400, 'body': "Invalid Sharee e-mail address '{}'".format(sharee) }
            new_path += "?email=" + sharee

    return { 'status_code': 301, 'location': "https://" + spaces_web_host + new_path }

def GetThirdPartyURL(url):

    return { 'status_code': 301, 'location': url }

def ProxyHTTPConnection(method = "GET", hostname = "localhost", path = "/", port = 80, timeout = 3):

    import http.client
    import urllib.parse
    import ssl

    if port == 443 or port == 8443:
        try:
            conn = http.client.HTTPSConnection(hostname, port = port, timeout = timeout, context = ssl._create_unverified_context())
        except Exception as e:
            return { 'status_code': 502, 'content_type': "text/plain", 'body': str(e) }
    else:
        conn = http.client.HTTPConnection(hostname, port = port, timeout = timeout)
    try:
        if method == "POST":
            params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
            headers = {'Content-Type': "application/x-www-form-urlencoded", 'Accept': "text/plain,text/html,application/xhtml+xml,application/xml"} 
            conn.request(method, path, params, headers)
        else:
            conn.request("GET", path)
        resp = conn.getresponse()
        status_code = resp.status
        if "Content-Type" in resp.headers:
            content_type = resp.headers["Content-Type"]
        else:
            content_type = None
        if 301 < status_code < 302:
            body = None
        else:
            body = resp.read()
    except Exception as e:
        return { 'status_code': 502, 'content_type': "text/plain", 'body': str(e) }
    conn.close()

    return { 'status_code': status_code, 'content_type': content_type, 'body': body }

def ParseLegacyURL(hostname = "localhost", path = "/", query_fields = {}):

    import re

    env = GetEnvironment(hostname)
    #s3_bucket_hostname = "hightail-" + env + "-legacy.s3.amazonaws.com"
    s3_bucket_hostname = "hightail-j5-legacy.s3.amazonaws.com"

    # PHI to Spaces transitional URIs
    www_to_spaces_uris = {
        "/login": "/login",
        "/login.php": "/login",
        "/send": "/send",
        "/folders": "/storage/hightail",
        "/sent": "/dashboard/tracker",
        "/overview": "/dashboard/tracker"
    }
    if path in www_to_spaces_uris:
         return GetSpacesURL(env, **{'new_path': www_to_spaces_uris[path]} )

    # v3 / PHI Downloads
    if path.startswith("/download/") and path != "/":
        return GetSpacesURL(env, **{'batch_id': path.split("/")[2]} )
    if path == "/e" and "phi_action" in query_fields:
        if "batch_id" in query_fields:
            return GetSpacesURL(env, **{'batch_id': query_fields['batch_id']} )
        if "sendId" in query_fields and "emailId" in query_fields:
            return GetSpacesURL(env, **{'send_id': query_fields['sendId'], 'email_id': query_fields['emailId']} )
    if path == "/dl" and "phi_action" in query_fields:
        rurl = query_fields['rurl']
        if "batch_id" in rurl:
            return GetSpacesURL(env, **{'batch_id': rurl[-22:]} )
        if "send_id" in rurl and "email" in rurl:
            return GetSpacesURL(env, **{'send_id': rurl[-49:-39], 'email_id': rurl[-32:]} )

    # v2PHP Downloads
    if hostname.startswith("download.") and path != "/":
       return GetSpacesURL(env, **{'ufid': path.replace("/","")} )

    # Uplink / Dropbox handling
    if path.startswith("/u/"):
        return GetSpacesURL(env, **{'uplink_name': path[3:]} )
    if hostname.startswith("dropbox.") and path != "/":
        return GetSpacesURL(env, **{'uplink_name': path.replace("/","")} )
    if path.startswith("/dropbox") and "dropbox" in query_fields:
        return GetSpacesURL(env, **{'uplink_name': query_fields['dropbox']} )

    # Send handling
    if hostname.startswith("rcpt.") and path != "/":
        if path[10] == "/" or path[11] == "/":
            return GetSpacesURL(env, **{'send_id': path.split("/")[1], 'email_id': path.split("/")[2][:32]} )

    # Shared Folder
    if path.startswith("/sharedFolder") and "phi_action" in query_fields:
        if "id" in query_fields:
            if "sharee" in query_fields:
                return GetSpacesURL(env, **{'share_id': query_fields['id'], 'sharee': query_fields['sharee']} )
            else:
                return GetSpacesURL(env, **{'share_id': query_fields['id']} )

    # transfer.php
    if path.startswith("/transfer.php") and "action" in query_fields:
        if query_fields['action'] == "dropbox":
                return GetSpacesURL(env, **{'uplink_name': query_fields['dropbox']} )
        if query_fields['action'] == "download":
                return GetSpacesURL(env, **{'ufid': query_fields['ufid']} )
        if query_fields['action'] == "batch_download":
            if "batch_id" in query_fields:
                return GetSpacesURL(env, **{'batch_id': query_fields['batch_id']} )
            if "send_id" in query_fields:
                return GetSpacesURL(env, **{'send_id': query_fields['send_id'], 'email_id': query_fields['email']} )

    # 1.0 SAML Login Handling
    if path.startswith("/loginSSO"):

        if env == "prod":
            api_host = "api.spaces.hightail.com"
        elif env == "j5":
            #api_host = "api.j5.org"
            api_host = "api.spaces.hightail.com"
        else:
            api_host = "api." + env + ".htspaces.com"
        return ProxyHTTPConnection("GET", api_host, "/api/v1/saml/loginSSO", 443)

        if "email" in query_fields and "caller" in query_fields:
            return ProxyHTTPConnection("GET", api_host, "/api/v1/saml/loginSSO?email={}&caller=".format(query_fields['email'], query_fields['caller']), 443)
        elif "email" in query_fields:
            return ProxyHTTPConnection("GET", api_host, "/api/v1/saml/loginSSO?email={}".format(query_fields['email']), 443)
        else:
            return GetSpacesURL(env, **{'new_path': "/corp-login"} )

    # 1.0 SAML Callback Handling
    if path.startswith("/samlLogin"):
        if env == "prod":
            spaces_api_host = "api.spaces.hightail.com"
        elif env == "j5":
            spaces_api_host = "api.j5.org"
        else:
            spaces_api_host = "api." + env + ".htspaces.com"
        return ProxyHTTPConnection("POST", spaces_api_host, "/api/v1/saml/consumer", 443)

    # Old website image paths
    if path.startswith("/en_US/"):
        return ProxyHTTPConnection("GET", s3_bucket_hostname, path)
    if path.startswith("/web/"):
        return ProxyHTTPConnection("GET", s3_bucket_hostname, path)

    # v3 Branding Images
    if path.startswith("/uploads/logos/"):
        file = path.split("/")[3]
        return ProxyHTTPConnection("GET", "bitspring-email-assets.s3.amazonaws.com", "/branding/" + file, 443)

    # Old v2 branding images
    if hostname.startswith("images."):
        if "_main" in path or "_email" in path:
            #return ProxyHTTPConnection("GET", "ysi-bimages.s3.amazonaws.com", path)
            return ProxyHTTPConnection("GET", s3_bucket_hostname, "/ysi-bimages" + path)
        else:
            return { 'status_code': 400, 'body': "Invalid Image" }

    # Older suport sites to Redirect to Zendesk
    if re.match(r"learn|kb|support|static", hostname) or re.match(r"/lenovo_getting_started|/applications|/apps", path):
        new_path = "/hc/en-us"
        # Express download
        if path.startswith("/applications") or "Express" in path:
            new_path += "/articles/203132540-Installing-Hightail-Express-"
        # Desktop sync download
        if re.match(r"/lenovo_getting_started|/apps|/plugins", path):
            new_path += "/articles/221397607-Hightail-Desktop-app"
        return GetThirdPartyURL("https://hightail.zendesk.com" + new_path)

    # Ookla speedtest
    if hostname.startswith("speedtest."):
        return GetThirdPartyURL("https://www.speedtest.net")

    # Old YSI Marketing blogs and press releases
    if hostname.startswith("blog.") or path.startswith("/cms/"):
        return GetThirdPartyURL("https://blog.hightail.com")

    # v1, discontined since 2011
    if path.startswith("/v1/"):
        return GetWWWURL(env, "/features")

    # Old SmartLing sites
    if re.match(r"fr|nl|it|de|es", hostname):
        return GetWWWURL(env, path)

    # Redirect to www if more specific match not found below
    if hostname == "hightail.com" or "yousendit.com" in hostname or "ysi" in hostname:
        return GetWWWURL(env, path)

    # No matches; just return something
    return { 'status_code': 418, 'body': "Hightail / YSI Legacy Redirector Function" }

def main(http_request):

    import sys
    import traceback

    # Make tracebacks as brief as possible
    sys.stderr = sys.stdout
    sys.tracebacklimit = 0

    try:
        http_response = ParseLegacyURL(http_request['host'], http_request['path'], http_request['query_string'])
        if not 'content_type' in http_response:
            http_response['content_type'] = "text/plain"
        return http_response

    except Exception:
        return {
            'status_code': 500,
            'content_type': "text/plain",
            'body': traceback.format_exc()
        }

# CGI Script execution
if __name__ == "__main__":

    import os
    import cgi
    import sys

    http_request = {
        'host': os.environ.get('HTTP_HOST', 'localhost'),
        'path': os.environ.get('REQUEST_URI', '/').split('?')[0],
        'query_string': {}
    }

    # Convert query parameters from objects to Dictionary
    query_fields_objects = cgi.FieldStorage()
    for key in query_fields_objects:
        http_request['query_string'][key] = str(query_fields_objects[key].value)

    http_response = main(http_request)

    if 301 <= http_response['status_code'] <= 302:
        print("Status: {} Moved Permanently\nLocation: {}\n".format(http_response['status_code'], http_response['location']))
    else:
        print("Status: {}\nContent-Type: {}\n".format(http_response['status_code'], http_response['content_type']))
        if type(http_response['body']) == str:
            print("\n" + http_response['body'] + "\n")
        else:
            sys.stdout.flush()
            sys.stdout.buffer.write(http_response['body'])

    sys.exit()

# AWS Lambda Entry Point
def lambda_handler(event, context):

    import base64

    http_request = {
        'host': event['headers']['host'],
        'path': event['path'],
        'query_string': event['queryStringParameters']
    }

    http_response = main(http_request)

    lambda_output = {}
    lambda_output['statusCode'] = http_response['status_code']

    if 301 <= lambda_ouput['status_code'] <= 302:
        lambda_output['headers'] = { 'Location': http_response['location']}
    else:
        lambda_output['headers'] =  { 'Content-Type': http_response['content_type'] }
        if type(http_response['body']) == str:
            lambda_output['body'] = http_response['body']
        else:
            lambda_output['body'] = base64.b64encode(http_response['body']).decode("utf-8")
            lambda_output['isBase64Encoded'] = True

    return lambda_output
