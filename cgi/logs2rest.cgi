#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(1, '../python-lib/')
#from assignment4_classes import LogReporter
#from assignment4_classes import LogFile
#from assignment4_classes import LogEntry
from database import MySQLDatabase

def main():

    #log_reporter = LogReporter()
    # Read some log files
    ##log_reporter.AddLogFile("/var/log/user.log")
    #log_reporter.AddLogFile("/var/log/named.log")
    #log_reporter.AddLogFile("/var/log/dpkg.log")

    # Open Database Connection
    mysql_database = MySQLDatabase("192.168.249.218", "loggingfun", "87zt9SdJYKBQWD95", "logs")
    mysql_database.OpenConnection()

    # Insert all log entries in to the SQL database
    for logfile in log_reporter.logfiles:
        for logentry in logfile.logentries:
            print(logentry.__str__())
            mysql_database.SQLInsertObject("log_messages", logentry)

    # Close Database Connection
    mysql_database.CloseConnection()

if __name__ == '__main__':
    main()
