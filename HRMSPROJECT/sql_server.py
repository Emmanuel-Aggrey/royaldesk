# TIME ATTENDACE SETTINGS TO MICROSOFT SQL SERVER
import pyodbc
from decouple import config
from .connections import MSSQLConnection
server_not_connected = ''

SERVER = config('SERVER')
DATABASE = config('DATABASE')
USER = config('USER_ID')
PASSWORD = config('PASSWORD')
TIMEOUT = config('TIMEOUT')


SERVER2 = config('SERVER2')
DATABASE2 = config('DATABASE2')
USER2 = config('USER_ID2')
PASSWORD2 = config('PASSWORD2')
TIMEOUT2 = config('TIMEOUT2')


conntected_to_server = True
try:
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};" + f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USER};"
        f"PWD={PASSWORD};",
        timeout=int(TIMEOUT)
        )

    cursor = connection.cursor()
except:
    server_not_connected = 'Server not connected'
    conntected_to_server = False
    print('server_not_connected',SERVER)



# Create instances of the MSSQLConnection class for each SQL Server
conn1 = MSSQLConnection(SERVER, DATABASE, USER, PASSWORD)
conn2 = MSSQLConnection(SERVER2, DATABASE2, USER2, PASSWORD2)

