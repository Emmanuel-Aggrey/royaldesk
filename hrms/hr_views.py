from datetime import datetime, timedelta

from django.db.models import Count, F, Q, Sum,FloatField
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django_pandas.io import read_frame
from HRMSPROJECT import sql_server
from HRMSPROJECT.custome_decorators import group_required
from rest_framework import generics, status
from rest_framework.decorators import api_view
from PIL import Image
import os
from rest_framework.response import Response
from datetime import datetime
from decouple import config
import shutil 
from . import partials
from .models import (Department, Dependant, Designation, Education, Employee,
                     Leave, LeavePolicy, PreviousEployment,
                     ProfessionalMembership)
    


@group_required('HR', 'MNG')
def hr_dashborad(request):

    return render(request,'hr/hr_dashborad.html')

@group_required('HR', 'MNG')
@api_view(['GET'])
def hr_reports(request, data_value=None):

    qs = Employee.objects.select_related('designation').exclude(for_management=True)
 

    # ACTIVE EMPLOYEES
    active_employees = qs.filter(status='active',department__for_management=False)

    # print(dir(active_employees))
    # active_employees_married = active_employees.filter(is_merried=True)

    is_merried = active_employees.values('is_merried').aggregate(
        married=(
            Count('id', filter=Q(is_merried='married'))
        ),
        not_married=(
            Count('id', filter=~Q(is_merried='married'))
        ),
    )

    # print('is_merried',is_merried)
    gender = active_employees.values('gender').aggregate(
        male=(
            Count('id', filter=Q(gender='male'))
        ),
        female=(
            Count('id', filter=Q(gender='female'))
        ),
    )



    age = active_employees.only('dob__year').annotate(age= datetime.now().year -F('dob__year'))\
        .aggregate(
        above=(
             Count('dob__year', filter=Q(age__gte=30))
        ),
        below=(
              Count('dob__year', filter=Q(age__lt=30))
        ),
    )
 

    on_leave = active_employees.values('leave_employees__from_leave','leave_employees__hr_manager').aggregate(
        on_leave=(
            Count('id', filter=Q(leave_employees__from_leave=False,leave_employees__hr_manager=True))
        ),
        applied_leave=(
            Count('id', filter=Q(leave_employees__from_leave=False,leave_employees__hr_manager=False))
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

    emp_exceed_leave = qs.filter(leave_employees__from_leave=False,leave_employees__hr_manager=True, leave_employees__resuming_date__gt=timezone.now()).values(
        'leave_employees__employee__first_name', 'leave_employees__employee__last_name', 'leave_employees__end')

    emp_on_leave = qs.filter(leave_employees__from_leave=False).values('leave_employees__employee__employee_id', 'leave_employees__from_leave', 'leave_employees__hr_manager', 'leave_employees__line_manager',
                                                                       'leave_employees__employee__first_name', 'leave_employees__employee__last_name', 'leave_employees__pk', 'leave_employees__resuming_date','leave_employees__status')

    emp_from_leave_recent = qs.filter(leave_employees__from_leave=True,leave_employees__hr_manager=True).values(
        'leave_employees__employee__first_name', 'leave_employees__employee__last_name', 'leave_employees__end').reverse()[:5]

    employment_rate = qs.values(
        'date_employed__year').annotate(employee_count=Count('date_employed'))

    turn_over_rate = qs.values(
        'status', 'date_employed__year').annotate(employee_count=Count('date_employed'))

    department_count = active_employees.values('department__name').annotate(employee_count=Count('department__name'))

    # print(dpeartment_count)

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
        'department_count':department_count,
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

@group_required('HR', 'MNG')
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

@group_required('HR', 'MNG')
@api_view(['POST'])
def hr_approve_leave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)

    new_hr_manager = True
    old_hr_manager = leave.hr_manager
    employee = str(request.user).upper()
    if partials.check_approval_status_change(new_hr_manager,old_hr_manager,'hr_manager', employee):
        print('new state update status')
        leave.hr_manager_approval = partials.check_approval_status_change(new_hr_manager,old_hr_manager,'hr_manager', employee)
    else:
        print('old state dont update status')

    
    leave.hr_manager = True
    leave.save()

    return Response(status=status.HTTP_200_OK)


@group_required('HR', 'MNG', 'FO')
def attendance(request):

    return render(request, 'attendance/attendance.html')


@group_required('HR', 'MNG', 'FO')
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

    # GET YESTERDAYS DATE IF NO DATE FROM, AND TO IS PROVIDED
    # sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) ='{}' AND DeptName IS NOT NULL GROUP BY [DeptName] ORDER BY [DeptName]".format(yesterday)

    sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In FROM [dbo].[V_Record] WHERE [StatusText] in ('In') AND CAST(CheckTime AS DATE) ='{}' AND DeptName IS NOT NULL GROUP BY [DeptName] ORDER BY [DeptName]".format(yesterday)
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
        # sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATETIME) BETWEEN '{}' AND '{}' AND DeptName IS NOT NULL GROUP BY [DeptName] ORDER BY [DeptName]".format(

        sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In FROM [dbo].[V_Record] WHERE [StatusText] in ('In') AND CAST(CheckTime AS DATETIME) BETWEEN '{}' AND '{}' AND DeptName IS NOT NULL GROUP BY [DeptName] ORDER BY [DeptName]".format(
            date_from, date_to)

    elif date_to:
        request.session['date_from'] = date_from
        request.session['date_to'] = date_to
        request.session['DATETIME'] = "DATE"
        # print(date_from, date_to)
        # sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS DATE) BETWEEN '{}' AND '{}' AND DeptName IS NOT NULL  GROUP BY [DeptName] ORDER BY [DeptName]".format(
    
        sql = "SELECT  [DeptName] AS Department, 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In FROM [dbo].[V_Record] WHERE [StatusText] in ('In') AND CAST(CheckTime AS DATE) BETWEEN '{}' AND '{}' AND DeptName IS NOT NULL  GROUP BY [DeptName] ORDER BY [DeptName]".format(
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

    # sql = "SELECT  [Name] , 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In, 'Out' as [Status_out],Count(case StatusText when 'Out' then 1 end) as Count_Out FROM [dbo].[V_Record] WHERE [StatusText] in ('In', 'Out') AND CAST(CheckTime AS {}) BETWEEN '{}' AND '{}' AND [DeptName]='{}' GROUP BY [Name] ORDER BY [Name]".format(
    #     DATETIME, date_from, date_to, department)

    sql = "SELECT  [Name] , 'In' as [StatusText In], Count(case StatusText when 'In' then 1 end) as Count_In FROM [dbo].[V_Record] WHERE [StatusText] in ('In') AND CAST(CheckTime AS {}) BETWEEN '{}' AND '{}' AND [DeptName]='{}' GROUP BY [Name] ORDER BY [Name]".format(
        DATETIME, date_from, date_to, department)

    cursor = sql_server.cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    # print(sql)
    # print(date_from, date_to)
    # print(result)
    return Response(result)


@group_required('HR', 'MNG', 'FO')
@api_view(['GET'])
def clockins(request):

    today = datetime.now()

    today_ = today.strftime('%Y-%m-%d')
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    week = today - timedelta(days=7)
    week = week.strftime('%Y-%m-%d')

    if sql_server.server_not_connected:
        # print('server not connected')
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

@group_required('IT')
@api_view(['GET', 'POST'])
def update_anviz_user(request):


    if request.method == 'GET':

        employee= request.GET.get('employee')
        # sql = "SELECT  [DeptName] AS Department, 'Name' as [Employee] FROM [dbo].[V_Record] WHERE [Userid] ='{}'".format(username)
        sql= "SELECT  [Duty] AS Department, [Name] as Employee FROM [dbo].[Userinfo] WHERE [Userid] = '{}'".format(employee)

        sql_data = ()
        
        try:
            cursor = sql_server.cursor.execute(sql)
            rows = cursor.fetchone()
            sql_data = rows
            name,department =  rows 
            request.session['anviz_id'] = employee
            anviz_employee = f'{department} {name}'.upper()
            request.session['anviz_employee'] = anviz_employee
            
        except :
            name=''
            department=''
            # print('not found',sql_data)
        
        # print('found ',sql_data)
        
        # print(department,name)
        # sql_server.connection.close()
        # sql_server.pyodbc.pooling=False
       

        
        # print(g)
        data = {
            'employee':name,
            'department':department
        }
        return Response(data)

 

    if request.method == 'POST':
        anviz_id = request.session.get('anviz_id')
        anviz_employee = request.session.get('anviz_employee')
        profile = request.FILES.get('profile')

        print(profile)

        image_root = config('IMAGE_ROOT')  
     
        img=  Image.open(profile).convert('RGB')
        size = 128, 128
        #img.thumbnail(size)
        image =img.save(f"{image_root}//{profile}")
        # img.save(f"{image_root}//{profile}")
        old_path = f'{image_root}//{profile}'
        new_location = config('NEW_LOCATION')
        
        new_path = f'{new_location}//{anviz_employee}.jpg'

            
        sql = "UPDATE [anviz].[dbo].[Userinfo] SET Picture =(SELECT  BulkColumn FROM OPENROWSET(BULK  N'C:/Users/Public/Profiles/{}',SINGLE_BLOB) AS Picture) WHERE Userid ='{}'".format(profile,anviz_id)

        cursor = sql_server.cursor.execute(sql)

        cursor.commit()

        #sql_server.connection.close()
        #sql_server.pyodbc.pooling=False

        
        shutil.move(old_path, new_path)
        # img.show(new_path)

        #print(cursor)

        return Response(anviz_employee)
