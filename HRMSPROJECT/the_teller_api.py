import requests
import json
import pprint
from decouple import config
from django.shortcuts import redirect
import random
import time
import string



# print(random.randint(10**12, 10**13 - 1))



# def create_transaction_id():
#     """GENERATE UNIQUE TRANSACTION ID"""
#     timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds

#     print('timestamp ',timestamp)
#     random_number = random.randint(1, 999999)  # Generate a random 6-digit number
#     transaction_id = f"{timestamp}{random_number:06}"  # Combine timestamp and random number
#     return transaction_id


# def create_transaction_id():
#     """GENERATE UNIQUE 12 DIGITS TRANSACTION ID"""
#     return random.randint(100000000000, 999999999999)
#     # str(random.randint(10**12, 10**13 - 1))




def create_transaction_id():
    """GENERATE UNIQUE 12 DIGITS TRANSACTION ID"""
    digits = string.digits
    return ''.join(random.choices(digits, k=12))

transaction_id = create_transaction_id()


def floatToMinor(amount):
    '''CREATE THETELLER AMOUNT'''
    if not amount:
        return "0".zfill(12)
    
    roundit = round(amount, 2)
    multiplyby100 = str(int(roundit * 100))
    minor = multiplyby100.zfill(12)
    
    return minor


headers = {
    'Authorization': config('THETELLER_Authorization'),
    'Content-Type': 'application/json',
    # 'Cookie': 'XSRF-TOKEN=eyJpdiI6ImgrVjcrc0h3Sll0aGVDYklTcGpSNHc9PSIsInZhbHVlIjoiWElLUWNZU0FIRkdubUMxYitjR21iTVwvYXJ5eW1IYm5Ec0Z2MzVjTHV0MUNFbU5sNkNMWEVmWEZOZ05nTGdSMFMiLCJtYWMiOiIyZWFiOGFlYjk1MzNiZTBkN2Q2MmFlYjNhM2U3ZDYzOWIzZDgwZDBlY2U5MDczYTJmZDZjZjY3NGQ3OTg2MmIyIn0%3D; theteller_checkout_session=eyJpdiI6Ikl0blp6c1AzXC84XC92TWdLS2psYXpQQT09IiwidmFsdWUiOiJvbk5ieGJJWmJLM0ZxeVl4dHFpVVAwSVZzYUQzXC9YZmFyZXd6Sm1EYW9XOEdqWXZuWnZGWjdERTlYNDE1enUrcCIsIm1hYyI6IjI2YWQ5OGY4OGFmZDE5Njk5ZDU3ZWVlMTk0MWVmNjMzZGUxYjMzZmJmMzkzYjhhZDhkZWQ4MGY4ZDE4M2VhN2EifQ%3D%3D'
    }

def make_payment(email,amount,transaction_id=create_transaction_id()):
    '''MAKE PAYMANT WITH THETELLER'''

    url = config('THETELLER_ENDPOINT')

    payload = json.dumps({
        "merchant_id": config('THETELLER_MERCHANT_ID'),
        "transaction_id": transaction_id,
        "desc": "Payment Using Checkout Page",
        "amount": floatToMinor(amount),
        "redirect_url": config('THETELLER_MY_REDIRENT_URL'),
        "email": email,
    })
  
    
    # response = requests.request("POST", url, headers=headers, data=payload)

# Make sure the connection is available before sending the request
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # raise an exception for 4xx or 5xx status codes

        result = response.json()
        # data = result.update({'transaction_id':transaction_id})

        result.update({'transaction_id': transaction_id})           
        # data = result


        return result
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

        return 'no connection try again'
    # handle the error as appropriate


    

    # data = {
    #     'checkout_url':result.get('checkout_url'),
    #     'status':result.get('status'),
    #     'reason':result.get('reason'),
    #     'token':result.get('token'),
    # }



    


# from HRMSPROJECT.the_teller_api import make_payment

def verify_transaction(transaction_id):


    try:
        # response = requests.request("POST", url, headers=headers, data=payload)
        response = requests.get(f'https://test.theteller.net/v1.1/users/transactions/{transaction_id}/status',headers=headers,verify=False)

        response.raise_for_status()  # raise an exception for 4xx or 5xx status codes

        result = response.json()

        return result
    except requests.exceptions.RequestException as e:
        # print(f"Error: {e}")

        return 'no connection try again'


    

    # from HRMSPROJECT.the_teller_api import make_payment





