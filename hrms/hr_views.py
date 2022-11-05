from datetime import datetime, timedelta

from django.db.models import Count, F, Q, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django_pandas.io import read_frame
from HRMSPROJECT import sql_server
from HRMSPROJECT.custome_decorators import group_required
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import (Department, Dependant, Designation, Education, Employee,
                     Leave, LeavePolicy, PreviousEployment,
                     ProfessionalMembership)


@group_required('HR', 'Manager')
@api_view(['GET'])
def hr_reports(request, data_value=None):

    qs = Employee.objects.exclude(id=4).select_related('designation')

    # ACTIVE EMPLOYEES
    active_employees = qs.filter(status='active')
    # active_employees_married = active_employees.filter(is_merried=True)

    is_merried = active_employees.values('is_merried').aggregate(
        married=(
            Count('id', filter=Q(is_merried=True))
        ),
        not_married=(
            Count('id', filter=Q(is_merried=False))
        ),
    )

    gender = active_employees.values('gender').aggregate(
        male=(
            Count('id', filter=Q(gender='male'))
        ),
        female=(
            Count('id', filter=Q(gender='female'))
        ),
    )

    age = active_employees.values('age').aggregate(
        above=(
            Count('id', filter=Q(age__gt=3))
        ),
        below=(
            Count('id', filter=Q(age__lt=3))
        ),
    )

    age = active_employees.values('age').aggregate(
        above=(
            Count('id', filter=Q(age__gt=3))
        ),
        below=(
            Count('id', filter=Q(age__lt=3))
        ),
    )

    on_leave = active_employees.values('leave_employees__from_leave').aggregate(
        on_leave=(
            Count('id', filter=Q(leave_employees__from_leave=False))
        ),
        not_on_leave=(
            Count('id', filter=Q(leave_employees__from_leave=True))
        ),
    )

    hods = active_employees.filter(is_head=True).values(
        'first_name', 'last_name', 'department__name')

    country = qs.values('country').annotate(emp_count=Count('country'))
    this_year = datetime.now().year

    # print(this_year-1)

    leave_this_year = qs.filter(leave_employees__from_leave=False, leave_employees__start__year=this_year).values(
        'leave_employees__start__month').annotate(emp_onleave_this_month=Count('leave_employees__start'))

    leave_applications = qs.filter(leave_employees__start__isnull=False).values(
        'leave_employees__start__year').annotate(leave_applications=Count('id'))

    emp_exceed_leave = qs.filter(leave_employees__from_leave=False, leave_employees__end__lt=timezone.now()).values(
        'leave_employees__employee__first_name', 'leave_employees__employee__last_name', 'leave_employees__end')

    emp_on_leave = qs.filter(leave_employees__from_leave=False).values('leave_employees__employee__employee_id', 'leave_employees__from_leave', 'leave_employees__hr_manager', 'leave_employees__line_manager',
                                                                       'leave_employees__employee__first_name', 'leave_employees__employee__last_name', 'leave_employees__pk', 'leave_employees__end')

    emp_from_leave_recent = qs.filter(leave_employees__from_leave=True).values(
        'leave_employees__employee__first_name', 'leave_employees__employee__last_name', 'leave_employees__end').reverse()[:5]

    employment_rate = qs.values(
        'date_employed__year').annotate(employee_count=Count('date_employed'))

    turn_over_rate = qs.values(
        'status', 'date_employed__year').annotate(employee_count=Count('date_employed'))

    # print(turn_over_rate)

    # employment_rate_quarter = employment_rate.filter(date_employed__quarter=2)

    emp_beneficiary = active_employees.distinct().values('id').aggregate(
        with_beneficiary=(
            Count('id', filter=Q(beneficiarys__employee_id__isnull=False))
        ),
        without_beneficiary=(
            Count('id', filter=Q(beneficiarys__employee_id__isnull=True))
        ),
    )

    # print('active_employees',active_employees)
    data = {
        'gender': gender,
        'age': age,
        'is_merried': is_merried,
        'emp_beneficiary': emp_beneficiary,
        'leave': on_leave,
        'country': country,
        'department_heads': hods,
        'active_employees_count': active_employees.count(),
        # 'active_employees_merried': active_employees.filter(is_merried=True).count(),

        'leave_this_year': leave_this_year,
        'leave_applications': leave_applications,
        'emp_exceed_leave': emp_exceed_leave,

        'emp_on_leave': emp_on_leave,
        'emp_from_leave_recent': emp_from_leave_recent,
        'employment_rate': employment_rate,
        'turn_over_rate': turn_over_rate,
    }

    # print(data_value)

    if not data_value:
        return Response(data)

    else:

        return Response(data.get(data_value))


@api_view(['GET'])
def employment_rate(request, quarter):

    employment_rate = Employee.objects.values(
        'date_employed__year').annotate(employee_count=Count('date_employed')).exclude(id=4)

    if quarter not in ['1', '2', '3']:
        return Response(employment_rate)

    else:

        employment_rate = employment_rate.filter(
            date_employed__quarter=int(quarter))

    return Response(employment_rate)


@api_view(['POST'])
def emp_on_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)

    # leave.on_leave = False
    leave.from_leave = True
    leave.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def hr_approve_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)

    leave.hr_manager = True
    leave.save()

    return Response(status=status.HTTP_200_OK)


@group_required('HR', 'Manager')
def attendance(request):

    return render(request, 'attendance/attendance.html')


@group_required('HR', 'Manager', 'FO')
@api_view(['GET', 'POST'])
def time_attendance(request):

    data = request.data

    print(data.get('datetime'))

    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    date_from = data.get('date_from')
    date_to = data.get('date_to')
    startTime = data.get('time_from')
    endTime = data.get('time_to')

    # GET YESTERDAYS DATE IF NO DATE FROM AND TO IS PROVIDED
    sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) ='{}' AND DeptName IS NOT NULL GROUP BY [DeptName] ORDER BY [DeptName]".format(yesterday)
    # print(sql)

    if date_to and endTime:
        date_from = f'{date_from} {startTime}:00'
        date_to = f'{date_to} {endTime}:00'

        request.session['date_from'] = date_from
        request.session['date_to'] = date_to
        request.session['DATETIME'] = "DATETIME"

        print(date_from, date_to)
#
        # print(date_from, date_to, startTime, endTime)

        sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATETIME) BETWEEN '{}' AND '{}' AND DeptName IS NOT NULL GROUP BY [DeptName] ORDER BY [DeptName]".format(
            date_from, date_to)

    elif date_to:
        request.session['date_from'] = date_from
        request.session['date_to'] = date_to
        request.session['DATETIME'] = "DATE"
        # print(date_from, date_to)

        sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) BETWEEN '{}' AND '{}' AND DeptName IS NOT NULL  GROUP BY [DeptName] ORDER BY [DeptName]".format(
            date_from, date_to)

    if sql_server.server_not_connected:
        print('server not connected')
        # return Response()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # cursor =sql_server.connection.cursor()
    else:
        cursor = sql_server.cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        return Response(result)


@api_view(['GET'])
def get_department(request, department):
    date_from = request.session.get('date_from')
    date_to = request.session.get('date_to')
    DATETIME = request.session.get('DATETIME')

    sql = "SELECT  [Name] , 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS {}) BETWEEN '{}' AND '{}' AND [DeptName]='{}' GROUP BY [Name] ORDER BY [Name]".format(
        DATETIME, date_from, date_to, department)

    cursor = sql_server.cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    # print(sql)
    # print(date_from, date_to)
    # print(result)
    return Response(result)


@group_required(['HR', 'FO'])
@api_view(['GET'])
def clockins(request):

    today = datetime.now()

    today_ = today.strftime('%Y-%m-%d')
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    week = today - timedelta(days=7)
    week = week.strftime('%Y-%m-%d')

    if sql_server.server_not_connected:
        print('server not connected')
        # return Response()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # cursor =sql_server.connection.cursor()
    else:
        sql_today = "SELECT  [StatusText] ,  Count(case StatusText when 'In' then 1 end) as Count_In, Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) ='{}' AND DeptName IS NOT NULL GROUP BY [StatusText] ORDER BY [StatusText]".format(today_)
        sql_yesterday = "SELECT  [StatusText] ,  Count(case StatusText when 'In' then 1 end) as Count_In, Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) ='{}' AND DeptName IS NOT NULL GROUP BY [StatusText] ORDER BY [StatusText]".format(yesterday)
        sql_week = "SELECT  [StatusText] ,  Count(case StatusText when 'In' then 1 end) as Count_In, Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) BETWEEN '{}' AND '{}' AND DeptName IS NOT NULL GROUP BY [StatusText] ORDER BY [StatusText]".format(week, today_)
        sql_department_yesterday = "SELECT  [DeptName] AS Department,  Count(case StatusText when 'In' then 1 end) as Count_In, Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) = '{}' AND DeptName IS NOT NULL GROUP BY [DeptName] ORDER BY [DeptName]".format(
            yesterday)

        cursor = sql_server.cursor.execute(sql_today)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_today = [dict(zip(columns, row)) for row in rows]

        cursor = sql_server.cursor.execute(sql_yesterday)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_yesterday = [dict(zip(columns, row)) for row in rows]

        cursor = sql_server.cursor.execute(sql_week)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_week = [dict(zip(columns, row)) for row in rows]

        cursor = sql_server.cursor.execute(sql_department_yesterday)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result_department_yesterday = [dict(zip(columns, row)) for row in rows]

        data = {
            'sql_today': result_today,
            'sql_yesterday': result_yesterday,
            'sql_week': result_week,
            'result_department_yesterday': result_department_yesterday,

        }

        return Response(data)


@api_view(['POST'])
def update_anviz_user(request):
    #     UPDATE [anviz].[dbo].[Userinfo]
    # SET Picture =
    #     (SELECT  BulkColumn FROM OPENROWSET(BULK  N'C:\783be074781f55bbe26bdefa33f9b1fc.jpg', SINGLE_BLOB) AS x)
    # WHERE Userid =184
    # image =  request.data.get('image')

    from PIL import Image
    import os

    image_path = "../profile"

    # os.mkdir(image_path)

    if request.method == 'POST':
        anviz_user = request.data.get('anviz_user')
        profile = request.FILES.get('image')



        image_path = "/media/aggrey/1EF5-7DBA/HR/profile"
     
        img=  Image.open(profile)
        size = 128, 128
        img.thumbnail(size)
        image = img.save(f"{image_path}/{profile}")

        old_path = f'{image_path}/{profile}'
        new_path = f'{image_path}/{anviz_user}.jpg'

        os.rename(old_path, new_path)

        img.show(new_path)


        





        print(anviz_user, profile)

        # sql = "UPDATE [anviz].[dbo].[Userinfo] SET Picture =(SELECT  BulkColumn FROM OPENROWSET(BULK  N'{}', SINGLE_BLOB) AS Picture) WHERE Userid ='{}'".format(image,anviz_user)

        # cursor = sql_server.cursor.execute(sql)

        # print(cursor)

        return Response(anviz_user)
