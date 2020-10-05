from __future__ import print_function
import os

def GetVariable(path = None, parameter = None):

    if 'REQUEST_METHOD' in os.environ:

        # Called via Web
        import cgi
        import cgitb
        cgitb.enable()
        fields = cgi.FieldStorage()
        uri = os.environ.get('REQUEST_URI', '/')
        if os.environ.get('REQUEST_METHOD') == "GET":
            if uri.startswith(path):
                ipv4_address = uri.split("/")[2]
            if parameter in fields:
                ipv4_address = str(fields["ipv4_address"].value)
            if ipv4_address and len(ipv4_address) >= 7:
                return ipv4_address
            else:
                return GetClientIP()
        elif os.environ.get('REQUEST_METHOD') == "POST":
            return "192.168.1.1"
        else:
            sys.exit("METHOD NOT SUPPORTED")

def GetClientIP():

    if not 'REQUEST_METHOD' in os.environ:
        return "127.0.0.1"

    x_real_ip = os.environ.get('HTTP_X_REAL_IP', '')
    x_fwd_for = os.environ.get('HTTP_X_FORWARDED_FOR', '')

    # Prefer X-Real-IP header
    if x_real_ip:
        return x_real_ip
    elif x_fwd_for:
        # Parse X-Forwarded-For
        if ", " in x_fwd_for:
            # Use last element of x-forward-for array
            return x_fwd_for.split(", ")[-1]
        else:
            return x_fwd_for
    else:
        # Use remote IP address, default to localhost if not defined
        return os.environ.get('REMOTE_ADDR', '127.0.0.1')

