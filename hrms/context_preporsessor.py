
from HRMSPROJECT.sql_server import conntected_to_server


def sql_server_is_connected(request):
    return {'conntected_to_server': conntected_to_server}