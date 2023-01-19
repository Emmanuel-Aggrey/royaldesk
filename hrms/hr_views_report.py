
import os
import shutil
import subprocess
from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from decouple import config
from django.db.models import Count, F, FloatField, Q, Subquery, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django_pandas.io import read_frame
from PIL import Image
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from HRMSPROJECT import sql_server
from HRMSPROJECT.custome_decorators import group_required

from . import partials
from .serializers import LeaveSerializer
from .models import (Department, Dependant, Designation, Education, Employee,
                     Leave, LeavePolicy, PreviousEployment,
                     ProfessionalMembership)


class CountryStaff(APIView):

    def get(self, request, *args, **kwargs):

        return Response()


@api_view(['GET'])
def country_stats(request):

    status = request.GET.get('status')
    country = request.GET.get('country')

    print(status, country)

    employee = Employee.employees.filter(country=country, status=status).values(
        'first_name', 'last_name', 'other_name', 'status')

    return Response(employee, status=200)


@api_view(['GET'])
def department_stats(request):

    status = request.GET.get('status')
    department = request.GET.get('department')

    employees = Employee.employees.select_related('department')

    if department == 'all':

        # departments = employees.filter(status=status).values('department__name').annotate(departmant_count=Count('department'))

        employees = employees.filter(status=status).values(
            'department__name', 'first_name', 'last_name', 'other_name', 'status').order_by('department__name')

    else:
        # departments = employees.values('department__name').filter(department=department,status=status).annotate(departmant_count=Count('department'))
        employees = employees.values('department__name', 'first_name', 'last_name', 'other_name', 'status').filter(
            status=status, department=department).order_by('department__name')

    data = {
        # 'departments': departments,
        'employees': employees,

    }

    return Response(data=data, status=200)


# @group_required('HR')
@api_view(['GET'])
def employment_rate(request):

    quarter = request.GET.get('quarter')
    start_date = request.GET.get('date_start')
    end_date = request.GET.get('date_end')
    status = request.GET.get('status')

    employment_rate = Employee.employees.select_related('department').values(
        'department__name', 'first_name', 'last_name', 'other_name', 'status')

    # print('quarter ',quarter,start_date,end_date,status)

  

    if quarter:

        employment_rate = employment_rate.filter(
            date_employed__quarter=int(quarter), status=status)
        
        print(employment_rate)

    if start_date:

        employment_rate = employment_rate.filter(
            date_employed__range=[start_date, end_date], status=status)

    return Response(data=employment_rate, status=200)


@api_view(['GET'])
def employement_status(request):

    department = request.GET.get('department')
    year = request.GET.get('year')
    # end_date = request.GET.get('date_end')
    status = request.GET.get('status')

    employment_rate = Employee.employees.select_related('department').values(
        'department__name', 'first_name', 'last_name', 'other_name', 'date_employed','date_departure')

    print('department here', department, year, status)

    if department == 'all':

        employment_rate = employment_rate.filter(
            date_employed__year=year, status=status)

    else:

        employment_rate = employment_rate.filter(
            date_employed__year=year, status=status, department=department)

    return Response(data=employment_rate, status=200)


@api_view(['GET'])
def employees_age(request):

    year = date.today().year

    age_from = int(request.GET.get('age_from'))
    age_to = int(request.GET.get('age_to'))
    status = request.GET.get('status')

    print(age_to,age_from,status)

    employees = Employee.employees.annotate(age=year-F('dob__year')).filter(age__range=[age_from,age_to],status=status)\
        .values(
        'department__name', 'first_name', 'last_name', 'other_name', 'status','age','dob')

    return Response(data=employees,status=200)



@api_view(['GET'])
def turn_over_rate(request):

    start_date = request.GET.get('date_from')
    end_date = request.GET.get('date_to')

 
    # Count the number of active and inactive employees within the date range
    # active_employees = Employee.objects.filter(
    # Q(status='active') & Q(date_employed__gte=start_date) & Q(date_employed__lte=end_date)
    # ).count()


    active_employees = Employee.objects.filter(date_departure__isnull=True,status='active').count()


    inactive_employees = Employee.objects.filter(~Q(status='active')&Q(date_departure__isnull=False, date_departure__range=(start_date, end_date))).count()


    # inactive_employees = Employee.objects.filter(
    # ~Q(status='active') & Q(employee_exit__data__date_departure__gte=start_date) & Q(employee_exit__data__date_departure__lte=end_date)
    # ).count()

    print('active_employees',active_employees,'inactive_employees',inactive_employees)

    # Calculate the turnover rate as a percentage
    turnover_rate = (
    inactive_employees / (active_employees + inactive_employees)
    )    * 100
    turnover_rate_percentage = "{:.2f} ".format(turnover_rate)

    print('turnover_rate_percentage',turnover_rate_percentage)


  

    turn_over_rate = {'date_from':start_date,'date_to':end_date,'rate':turnover_rate_percentage}
    

    return Response(data=turn_over_rate,status=200)




@api_view(['GET'])
def leave(request):
    department = request.GET.get('department')
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    on_leave = request.GET.get('on_leave').capitalize()
    supervisor = request.GET.get('supervisor').capitalize()
    line_manager = request.GET.get('line_manager').capitalize()
    hr_manager = request.GET.get('hr_manager').capitalize()


    leave = Leave.objects.select_related('employee')
    if department=='all':

        leave =leave.filter(status=status,on_leave=on_leave,supervisor=supervisor,line_manager=line_manager,hr_manager=hr_manager,start__range=[start_date,end_date])
    else:
        leave =leave.filter(status=status,on_leave=on_leave,supervisor=supervisor,line_manager=line_manager,hr_manager=hr_manager,start__range=[start_date,end_date],employee__department=department)


    serializer = LeaveSerializer(leave,many=True)

    print(serializer.data)


    return Response(data=serializer.data,status=200)