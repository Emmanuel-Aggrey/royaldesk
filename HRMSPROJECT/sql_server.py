# TIME ATTENDACE SETTINGS TO MICROSOFT SQL SERVER
import pyodbc
from decouple import config

server_not_connected = ''

SERVER = config('SERVER')
DATABASE = config('DATABASE')
USER = config('USER_ID')
PASSWORD = config('PASSWORD')

try:
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};" + f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USER};"
        f"PWD={PASSWORD};")
    cursor = connection.cursor()
except:
    server_not_connected = 'Server not connected'
    print('server_not_connected',SERVER)


# cursor = connection.cursor()
