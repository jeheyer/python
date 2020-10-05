from __future__ import print_function
import os
import math

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

    #
    if not 'REQUEST_METHOD' in os.environ:
        return "127.0.0.1"

    x_real_ip = os.environ.get('HTTP_X_REAL_IP', '')
    x_fwd_for = os.environ.get('HTTP_X_FORWARDED_FOR', '')
    # Prefer X-Real-IP header
    if x_real_ip:
        client_ip = x_real_ip
    elif x_fwd_for:
        if ", " in x_fwd_for:
            # Use last element of x-forward-for array
            client_ip = x_fwd_for.split(", ")[-1]
        else:
            client_ip = x_fwd_for
    else:
        # Use remote IP address, default to localhost if not defined
        client_ip = os.environ.get('REMOTE_ADDR', '127.0.0.1')
    return client_ip
