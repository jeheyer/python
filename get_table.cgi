#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

def main():

    import configparser
    sys.stderr = sys.stdout
    sys.path.insert(1, 'lib/')
    from database import MySQLDatabase
    #from http_utils import GetVariable

    try:
        if os.environ.get('REQUEST_METHOD') == "GET":
            import cgi
            form = cgi.FieldStorage()
            if "database" in form and "table" in form:
                db_name = str(form["database"].value)
                db_table = str(form["table"].value)
                if "join_table" in form:
                    db_join_table = str(form["join_table"].value)
            else:
                raise Exception("Must provide database name and table name as arguments")
        else:
            if len(sys.argv) > 2:
                db_name = sys.argv[1]
                db_table = sys.argv[2]
                db_join_table = False
                if len(sys.argv) > 3:
                    db_join_table = sys.argv[3]
            else:
                raise Exception("Must provide database name and table name as arguments")

    except Exception as e: 
        raise Exception(e)

    try:

        # Read config file
        config = configparser.ConfigParser()
        config.read('/mnt/homes/j5/automation/cfg/mysql.cfg')
        mysql_database = MySQLDatabase(
            config[db_name]['hostname'],
            config[db_name]['username'],
            config[db_name]['password'],
            db_name
        )

        mysql_database.OpenConnection()
        if db_table == "polls":
            rows = mysql_database.SQLQuery("SELECT * FROM polls,{} WHERE polls.poll_name = '{}' AND id = polls.choice_id".format(db_join_table, db_join_table))
        else:
            rows = mysql_database.GetTable(db_table,"ORDER BY id")
        mysql_database.CloseConnection()

        return rows

    except Exception as e:
        raise Exception(e)

if __name__ == '__main__':

    sys.stderr = sys.stdout

    try:
        data = main()
        print("Status: 200\nContent-Type: text/json; charset=UTF-8\n")
        print(json.dumps(data, indent=3))        

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n\n{}".format(e))
