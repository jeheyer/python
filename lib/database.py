import mysql.connector
import os
import json

class MySQLDatabase():

    def __init__(self, hostname = "localhost", username = "root", password = "", database = "mysql"):

        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database

    def OpenConnection(self):

        try:
            self.cnx = mysql.connector.connect(host = self.hostname, user = self.username, password = self.password, database = self.database)
            self.GetVersion()
        except Exception as e:
            raise Exception(e)

    def CloseConnection(self):
        self.cnx.close()

    def GetVersion(self):

        self.SQLQuery("SELECT VERSION()")
        self.version = self.rows[0]

    def GetTable(self, table_name, options = None):

        if table_name == None:
            sys.exit("Need a table name!")
        query = "SELECT * from " + table_name
        if options:
            query += " " + options
        self.SQLQuery(query)
        return self.rows

    def PrintAsJSON(self):

        #if os.environ.get('REQUEST_METHOD'):
        #    print("Status: 200\nContent-Type: text/json; charset=UTF-8\n")

        #for row in self.rows:
        print(json.dumps(self.rows, indent=4, sort_keys=True, default=str))

    def SQLQuery(self, command):

        self.rows = []
        self.SQLExecute(command)
        return self.rows

    def SQLInsertObject(self, table_name, object_to_insert):

        if table_name == None or object_to_insert == None:
            sys.exit("Need a table name and object!")

        command = "INSERT INTO " + table_name + " ("
        attributes = object_to_insert.__dict__.keys()
        num_attributes = len(attributes)

        # Populate the column names to insert
        i = 1
        for attribute in attributes:
            command += attribute
            if i < num_attributes:
                command += ", "
                i += 1
            else:
                break
        command += ") VALUES ("

        # Populate the values for SQL command
        i = 1
        for attribute in attributes:
            value = getattr(object_to_insert, attribute)
            if type(value) == str:
                value = "'" + value.replace("'","''") + "'"
            command += str(value)
            if i < num_attributes:
                command += ", "
                i += 1
            else:
                 break
        command += ");"

        self.SQLExecute(command)

    def SQLExecute(self, command):

        if command == None:
           sys.exit("Need a command to execute")
        self.cursor = self.cnx.cursor(dictionary=True)
        self.cursor.execute(command)
        if "SELECT" in command:
            for rows in self.cursor:
                self.rows.append(rows)
        if "INSERT" in command:
            self.cnx.commit()
        self.cursor.close()
