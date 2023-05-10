
from HRMSPROJECT.sql_server import conntected_to_server
from menu.api import CAPS_CONNECTION

# CAPS_CONNECTION
from decouple import config

def sql_server_is_connected(request):
    return {'conntected_to_server': conntected_to_server}


def no_beneficiaries(request):
    return {'no_beneficiaries': config('NO_OF_BENEFICIARY',default=2)}


def company_name(request):
    return {'company_name': config('COMPANY_NAME',default='Rock City Hotel')}