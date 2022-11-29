# TIME ATTENDACE SETTINGS TO MICROSOFT SQL SERVER
import pyodbc
from decouple import config

server_not_connected = ''

SERVER = config('SERVER')
DATABASE = config('DATABASE')
USER = config('USER_ID')
PASSWORD = config('PASSWORD')
TIMEOUT = config('TIMEOUT')
conntected_to_server = True
try:
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};" + f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USER};"
        f"PWD={PASSWORD};",
        timeout=int(TIMEOUT))

    cursor = connection.cursor()
except:
    server_not_connected = 'Server not connected'
    conntected_to_server = False
    print('server_not_connected',SERVER)

