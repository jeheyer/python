#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import traceback
import configparser
sys.path.insert(1, 'lib/')
from database import *

def main():

    sys.stderr = sys.stdout

    try:
        # Read config file
        config = configparser.ConfigParser()
        config.read('/mnt/homes/j5/automation/cfg/mysql.cfg')
        mysql_hostname = config['mysql-test']['hostname']
        mysql_username = config['mysql-test']['username']
        mysql_password = config['mysql-test']['password']
        mysql_database = MySQLDatabase(mysql_hostname, mysql_username, mysql_password, "turdmonger")
        mysql_database.OpenConnection()

        rows = mysql_database.GetTable("tweets", "ORDER BY date_time DESC")
        mysql_database.CloseConnection()

        print("Status: 200\nContent-Type: text/json; charset=UTF-8\n")
        print("{\"tweets\": ")
        mysql_database.PrintAsJSON()
        print("}")

    except:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        exc = traceback.format_exc()
        print(exc)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("{\"comment\": \"exec time = %s seconds\"}" % (time.time() - start_time))
