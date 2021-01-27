from __future__ import print_function
import os
import math
import socket

class IP_Address:

    def __init__(self, value):

        if isinstance(value, int):
            self.as_int = value
            self.as_string = self.IntToString()
        else:
            self.as_string = str(value)
            self.as_int = self.StringToInt()

    def IntToString(self):
        as_string = ""
        remainder = self.as_int
        for i in range(3,0,-1):
            octet = math.floor(remainder / 2 ** (i * 8))
            as_string = as_string + str(octet) + "."
            remainder = remainder % 2 ** (i * 8) 
        as_string = as_string + str(self.as_int % 256)
        return as_string

    def StringToInt(self):
        int_val = 0
        octets = self.as_string.split('.')
        for i in range(0,4):
            int_val += int(octets[i]) * (2 ** ((3 - i) * 8))
        return int_val
        #return(int(int(quad[0]) * 16777216 + int(quad[1]) * 65536 + int(quad[2]) * 256 + int(quad[3])))

    def __str__(self):
        return str(self.as_string)


def GetClientIP():

    # Don't have HTTP headers, so just return localhost
    if not 'REQUEST_METHOD' in os.environ:
        return "127.0.0.1"

    # By default, use GCI REMOTE_ADDR value
    client_ip = os.environ.get('REMOTE_ADDR', "127.0.0.1")

    # Check for X-Real-IP and X-Fowarded-For headers
    x_real_ip = os.environ.get('HTTP_X_REAL_IP', None)
    x_fwd_for = os.environ.get('HTTP_X_FORWARDED_FOR', None)

    # Prefer X-Real-IP header
    if x_real_ip:
        client_ip = x_real_ip
    elif x_fwd_for:
        if ", " in x_fwd_for:
            # Get a list of IPs addresses used by this web server hostname
            server_ips = socket.gethostbyname(os.environ.get('HTTP_HOST', "localhost"))
            x_fwd_for_ips =  x_fwd_for.split(", ")
            for x in range(len(x_fwd_for_ips)):
                if x_fwd_for_ips[x] in server_ips:
                    # Use last IP address before the IP of this web server
                    client_ip = x_fwd_for_ips[x-1]

    return client_ip
