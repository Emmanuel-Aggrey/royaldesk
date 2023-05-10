

import pyodbc
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import pandas
from HRMSPROJECT.sql_server import conn2
from HRMSPROJECT.connections import ms_db
from HRMSPROJECT.the_teller_api import make_payment, verify_transaction
import json
CAPS_CONNECTION = True




@api_view(['GET',])
def menu(request):
    try:
        with conn2.connect() as cnxn:
            # Create a cursor object
            cursor = cnxn.cursor()

            # Execute a query
            cursor.execute('SELECT * FROM dbo.ME_V_SUB_MENU_OBJ')

            # Fetch the results of the query
            rows = cursor.fetchall()

            category = {}
            for row in rows:
                # category[row.PK] = row.CATEGORY
                # category[row.PK] = row.CATEGORY.strip()
                category[row.PK] = row.CATEGORY
                # print(category)

            columns = [column[0] for column in cursor.description]
            menu = [dict(zip(columns, row)) for row in rows]

            formatted_menu = [

                {
                "NAME": item["NAME"],
                "CATEGORY": item["CATEGORY"],
                "PRICE": item["PRICE"],
                "PK": item["PK"],
                "NAME_PK": item["NAME"].replace(" ", "").lower()+"{}{}".format(item["PK"],item["PRICE"]),
                 }
                for item in menu
            ]

            # NAME = [d['NAME'] for d in menu]

            # NAME["NAME"].replace(" ", "").lower()

            # CATEGORY =list(map(str.lower,NAME))

            # print(NAME)


            data = {
                'category': category,
                'menu': formatted_menu
            }
            return Response(data=data, status=status.HTTP_200_OK)

    except pyodbc.Error as ex:
        CAPS_CONNECTION = False
        print("Error: ", ex)
        print("Unable to establish connection to the database.")

        data = {
            'message': "Unable to establish connection to the database.",
            'CAPS_CONNECTION': CAPS_CONNECTION,
            # 'ex':str(ex)
        }

        return Response(data=data, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET',])
def check(request,check):

    # CheckNumber = request.GET.get('check')

    try:
        with conn2.connect() as cnxn:
            # Create a cursor object
            cursor = cnxn.cursor()

            # Execute a query
            sql = "SELECT CheckID,CheckNumber,CheckOpen,CheckClose,AlternateID,SubTotal,Payment,CheckPostingTime,Due\
                    FROM CheckPostingDB.dbo.CHECKS WHERE CheckNumber={}".format(check)
            cursor.execute(sql)

            # Fetch the results of the query
            rows = cursor.fetchone()
            

            column_names = [desc[0] for desc in cursor.description]


        # Combine the column names with the row values as a dictionary
            data = None
            
            row_dict = dict(zip(column_names, rows)) if rows else  None

            # print(row_dict)


            # print(row_dict)
            if isinstance(row_dict, dict):
                print('found')
                amont = row_dict.get('Payment')
                amont1 = row_dict.get('SubTotal')
                amont  if amont else amont1

                data = make_payment('aggrey.en@gmail.com',2)



            else : data = f'{check} not found'
                      
            return Response(data=data, status=status.HTTP_200_OK)

    except pyodbc.Error as ex:
        CAPS_CONNECTION = False
        print("Error: ", ex)
        print("Unable to establish connection to the database.")

        data = {
            'message': "Unable to establish connection to the database.",
            'CAPS_CONNECTION': CAPS_CONNECTION,
            # 'ex':str(ex)
        }

        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

# "167950139042 8672591"

@api_view(['GET',])
def verify_payment(request):
    '''VERIFY PAYMENT  CHECK NUMBER OR TABLE NAME'''
    transaction_id = request.GET.get('transaction_id')
    print(transaction_id)
    data = verify_transaction(transaction_id)

    return Response(data=data, status=status.HTTP_200_OK)
    
    # return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET',])
def excel_menu(request):
    df = pandas.read_csv('menu/MENU.csv')


    category = set(df['CATEGORY'])

    values = df.to_json(orient='records', indent=False)
    values = json.loads(values)

    # names = values.get('CATEGORY')

    # print(names)

    formatted_menu = [

                {
                "NAME": item["NAME"],
                "CATEGORY": item["CATEGORY"],
                "PRICE": item["PRICE"],
                "PK": item["PK"],
                "NAME_PK": item["NAME"].replace(" ", "").lower()+"{}".format(item["PK"]),
                 }
                for item in values
            ]
    # print(formatted_menu)

    data = {
        'category': category,
        'menu': formatted_menu
    }

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET',])
def verify_check(request,check):
    df = pandas.read_csv('menu/CHECKS.csv')


    values = {}
    result = None
   # Convert CheckNumber column to string data type
    df['CheckNumber'] = df['CheckNumber'].astype(str)

    # Filter dataframe by CheckNumber
    filtered_df = df.loc[df['CheckNumber'] == check]

    if not filtered_df.empty:
        amount = filtered_df['Payment'].iloc[0]
    
        check = f'{check}000000' #CheckNumber to 12 digits  by adding 6 zeros 

        result = make_payment('aggrey.en@gmail.com',5,check)

        if isinstance(result,dict): result.update({'check_number': check,'amount':amount}) 

        return Response(data=result,status=status.HTTP_200_OK)


        
    else:
        # print('No payment found for CheckNumber ',check)
        result = f'No payment found for check number {check}'
        return Response(data=result,status=status.HTTP_200_OK)

    # return Response(data=result,status=status.HTTP_200_OK)
