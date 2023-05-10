import pyodbc
import random
from decouple import config
from django.conf import settings

import pyodbc
import cx_Oracle as oracledb

SERVER = config('SERVER')
DATABASE = config('DATABASE')
USER = config('USER_ID')
PASSWORD = config('PASSWORD')
TIMEOUT = config('TIMEOUT')


SERVER2 = config('SERVER2')
DATABASE2 = config('DATABASE2')
USER_ID2 = config('USER_ID2')
PASSWORD2 = config('PASSWORD2')
TIMEOUT2 = config('TIMEOUT2')

class MSSQLConnection:
    def __init__(self, server, database, username, password,timeout='1'):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.timeout = timeout

    def connect(self):
        conn_str = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER=' + self.server + ';'
            f'DATABASE=' + self.database + ';'
            f'UID=' + self.username + ';'
            f'PWD=' + self.password + ';'
            f'timeout=' + self.timeout + ':'
        )
        return pyodbc.connect(conn_str)


# conn1 = MSSQLConnection(SERVER, DATABASE, USER, PASSWORD,TIMEOUT)
# conn2 = MSSQLConnection(SERVER2, DATABASE2, USER_ID2, PASSWORD2,TIMEOUT2)

# import pyodbc

class MSSQLDatabase:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None

    def connect(self):
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        self.conn = pyodbc.connect(conn_str)
        self.conn.autocommit = True

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def execute_query_all(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def execute_query_one(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()


ms_db = MSSQLDatabase(server=SERVER2, database=DATABASE2, username=USER_ID2, password=PASSWORD2)
# ms_db.connect()
# result = ms_db.execute_query_all('SELECT * FROM dbo.ME_V_SUB_MENU_OBJ')
# print(result)
# ms_db.disconnect()



# OPERA BELOW 


O_USER = 'opera'
O_PASSWORD = 'opera'
O_DSN = '192.168.1.13/opera'
O_DATABASE = 'opera'
import cx_Oracle

class OracleDB:
    def __init__(self, username, password, dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
        self.connection = None

    def connect(self):
        try:
            self.connection = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.dsn)
            print("Connected to Oracle Database successfully")
        except Exception as e:
            print("Error while connecting to Oracle Database:", e)

    def execute_query_all(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("Error while executing query:", e)
    
    def execute_query_one(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchone()
            return rows
        except Exception as e:
            print("Error while executing query:", e)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from Oracle Database")

oracle_db = OracleDB(O_USER, O_PASSWORD, O_DSN)


# oracle_db.connect()
# result = oracle_db.execute_query_all("SELECT * FROM OPERA.NAME")
# print(result)
# oracle_db.disconnect()


