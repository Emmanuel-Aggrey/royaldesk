# ------------------------------------------------------------------------------
# Copyright (c) 2016, 2021, Oracle and/or its affiliates. All rights reserved.
#
# Portions Copyright 2007-2015, Anthony Tuininga. All rights reserved.
#
# Portions Copyright 2001-2007, Computronix (Canada) Ltd., Edmonton, Alberta,
# Canada. All rights reserved.
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# database_change_notification.py
#   This script demonstrates using database change notification in Python, a
# feature that is available in Oracle 10g Release 2. Once this script is
# running, use another session to insert, update or delete rows from the table
# TestTempTable and you will see the notification of that change.
#
# This script requires cx_Oracle 5.3 and higher.
# ------------------------------------------------------------------------------

import time

import cx_Oracle as oracledb
import datetime
# from views import oracle_db

# import sample_env

# 7:47
registered = True


def callback(message):
    global registered
    print("Message type:", message.type)
    if not message.registered:
        print("Deregistration has taken place...")
        print(datetime.datetime.now())
        registered = False
        return
    print("Message database name:", message.dbname)
    print("Message tranasction id:", message.txid)
    print("Message tables:")

    for table in message.tables:
        print("--> Table Name:", table.name)
        print("--> Table Operation:", table.operation)
        if table.rows is not None:
            print("--> Table Rows:")
            for row in table.rows:
                print("--> --> Row RowId:", row.rowid)
                print("--> --> Row Operation:", row.operation)
                print("-" * 60)
        print("=" * 60)

    # QUERY START

    sql = "SELECT * from OPERA.R_SP_SYNTAX_ROM ORDER BY BUSINESS_DATE_CREATED  DESC FETCH FIRST 1 ROWS ONLY"
    sql1 = "SELECT * FROM OPERA.R_SP_SYNTAX_ROM WHERE ROWNUM = 1 ORDER BY UPDATE_DATE DESC"

    sql2 = "SELECT RESV_NAME_ID,SALUTATION,ENVELOPE_GREETING,LETTER_GREETING,\
            CONFIRMATION_NO,UPDATE_DATE,TOTAL_REVENUE,ROOM_CATEGORY_LABEL,\
            RESV_STATUS,COMPUTED_RESV_STATUS \
            FROM OPERA.NAME_RESERVATION   ORDER BY UPDATE_DATE  DESC"
    cursor = connection.cursor()
    cursor.execute(sql2)
    row = cursor.fetchone()

    print(row)



# connection = oracledb.connect(sample_env.get_main_connect_string(),
#                               events=True)
connection = oracledb.connect(user="opera", password="opera",
                              dsn="192.168.1.13/opera", events=True)


sub = connection.subscribe(callback=callback, timeout=1800,
                           qos=oracledb.SUBSCR_QOS_ROWIDS)
print("Subscription:", sub)
print("--> Connection:", sub.connection)
print("--> ID:", sub.id)
print("--> Callback:", sub.callback)
print("--> Namespace:", sub.namespace)
print("--> Protocol:", sub.protocol)
print("--> Timeout:", sub.timeout)
print("--> Operations:", sub.operations)
print("--> Rowids?:", bool(sub.qos & oracledb.SUBSCR_QOS_ROWIDS))


# sql = "SELECT * FROM OPERA.RESERVATION_NAME"
sql2 = "SELECT * FROM OPERA.NAME"
sub.registerquery(sql2)

while registered:
    # input('"Waiting for notifications...."')
    # sub.refresh()
    print("Waiting for notifications....")
    time.sleep(5)

