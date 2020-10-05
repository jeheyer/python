#!/usr/bin/env python3

from __future__ import print_function
import os
import subprocess
#from geoip import geolite2

output = str(subprocess.check_output('traceroute -n -q 1 -4 -T 66.170.1.1', shell=True))
lines = output.split("\\n")

for i in range(1,len(lines)-1):
    line = lines[i]
    #print(line)
    hop = str(line[:2].replace(" ",""))
    data = str(line[4:].replace("  "," ")).split(" ")
    #print(data)
    ipv4_address = data[0]
    latency = data[1]
    #match = geolite2.lookup(ipv4_address)
    #lat = match.location[0]
    #lng = match.location[1]
    #country = match.country.upper();
    print(hop + " : " + ipv4_address + " = " + latency)
    #line = line.replace("  ", " ")
    #print(line)
    #parts = line.split(" ")
    #print(parts[0])
    #parts = line.split(" ")
    #print(parts[0])
#stream = os.popen('echo Returned output')
#output = stream.read()
#output