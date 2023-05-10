from HRMSPROJECT.connections import oracle_db

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


@api_view(['GET'])
def reservations(request):

    oracle_db.connect()
    # sql = "SELECT COUNT(RESV_STATUS ),RESV_STATUS  FROM OPERA.NAME_RESERVATION  WHERE  RESV_STATUS IN ('RESERVED','CHECKED IN') GROUP BY RESV_STATUS"
    sql2 = "SELECT COUNT(RESV_STATUS ),COMPUTED_RESV_STATUS  \
        FROM OPERA.NAME_RESERVATION  WHERE  COMPUTED_RESV_STATUS IN ('RESERVED','CHECKED IN','DUE IN','DUE OUT') \
           AND ROOM_CATEGORY_LABEL NOT IN ('PM')  GROUP BY COMPUTED_RESV_STATUS"
    sql_today = "SELECT COUNT(COMPUTED_RESV_STATUS),COMPUTED_RESV_STATUS  \
        FROM OPERA.NAME_RESERVATION   WHERE COMPUTED_RESV_STATUS IN ('NO SHOW','CHECKED OUT') \
          AND ROOM_CATEGORY_LABEL NOT IN ('PM')  AND  TRUNC(UPDATE_DATE) = TRUNC(SYSDATE)  GROUP BY COMPUTED_RESV_STATUS"

    result1 = oracle_db.execute_query_all(sql2)
    result2 = oracle_db.execute_query_all(sql_today)

    result = result1 + result2

    # print(result)
    print('called')
    # print(result)
    oracle_db.disconnect()

    return Response(data=result, status=status.HTTP_200_OK)
