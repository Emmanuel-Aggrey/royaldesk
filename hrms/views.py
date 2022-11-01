import os
import sys
from datetime import datetime

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, models
from django.db.models import Count, F, Q, Sum, Variance
from django.http import JsonResponse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render, resolve_url, reverse)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView, View)
from HRMSPROJECT.custome_decorators import group_required
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.contrib.auth.models import Group

from .import tasks
from .models import (Department, Dependant, Designation, Education, Employee,
                     Leave, LeavePolicy, PreviousEployment,
                     ProfessionalMembership, Documente, File)
from helpdesk.models import User

from .serializers import (EmployeeSerializer, GetEmployeeSerializer,
                          LeaveSerializer, DocumentSerializer)


def date_value(value):
    return value if value else None

# @group_required('HR', 'Manager')


@api_view(['GET', 'POST'])
def employees(request):

    if request.method == 'GET':

        employees = Employee.objects.exclude(id=4)
        serializer = EmployeeSerializer(employees, many=True)

        return Response({'data': serializer.data})

    elif request.method == 'POST':

        data = request.data
        profile = request.FILES.get('profile')
        first_name = data.get('fname')
        last_name = data.get('lname')
        date_employed = data.get('date_employed')
        helpdesk_user = bool(int(data.get('helpdesk_user')))

        # CREATTING EMPLOYEE ID
        date = datetime.strptime(date_employed, '%Y-%m-%d')
        year = date.strftime('%Y')
        emp_id = f'{first_name[0]}{last_name}-{year}'.upper().replace(' ', '')

        employees = {
            'profile': profile,
            "first_name": first_name,
            "last_name": last_name,
            'title': data.get('title'),
            'email': data.get('email'),
            'dob': data.get('dob'),
            'other_name': data.get('oname'),
            'is_head': data.get('hod'),
            'salary': data.get('salary'),
            'nia': data.get('nia'),
            'emergency_name': data.get('emergency_name'),
            'emergency_phone': data.get('emergency_phone'),
            'emergency_address': data.get('emergency_address'),
            'place_of_birth': data.get('place_of_birth'),
            'is_merried': data.get('is_merried'),
            'nationality': data.get('nationality'),
            'languages': data.get('languages'),
            'country': data.get('country'),
            'department_id': data.get('department'),
            'designation_id': data.get('designation'),
            'snnit_number': data.get('snnit_number'),
            'bank_name': data.get('bank_name'),
            'bank_branch': data.get('bank_branch'),
            'bank_ac': data.get('bank_ac'),
            'next_of_kin_name': data.get('next_of_kin_name'),
            'next_of_kin_phone': data.get('next_of_kin_phone'),
            'next_of_kin_address': data.get('next_of_kin_address'),
            'next_of_kin_relationship': data.get('next_of_kin_relationship'),
            "date_employed": date_employed,
            'gender': data.get('sex'),
            'address': data.get('res_address'),
            'mobile': data.get('p_phone'),
            'employee_id': emp_id,
            'applicant_id': date_value(data.get('applicant'))
        }

        # print(date_value(data.get('applicant')))

        employee = Employee.objects.create(**employees)

        # CREATE HELPDESK USER
        # user = User(password='changeme', username=employees.get('employee_id'), first_name=employees.get('first_name'), last_name=employees.get(
        #     'last_name'),is_head=employees.get('is_head'), email=employees.get('email'), department_id=employees.get('department_id'), designation_id=employees.get('designation_id'), profile=employees.get('profile'))

        user = User(password='changeme', username=employee.employee_id, first_name=employee.first_name, last_name=employee.last_name, is_head=employee.is_head,
                    email=employee.email, department_id=employee.department_id, designation_id=employee.designation_id, profile=employee.profile)

        # GET DEPARTMENT INITIALS eg FRONT OFFICE to FO
        # ''.join([x[0].upper() for x in user.department.name.split(' ')])

        
        # GET DEPARTMENT SHORTNAME    
        department = employee.department.shortname

       
        # CREATE HELPDESK USER AND ADD TO GROUP
        group = Group.objects.filter(name=department).last()
        if user and helpdesk_user and group:
            user.save()
            user.groups.add(group)
          

         # CREATE HELPDESK USER
        if user and helpdesk_user:
            user.save()

        # SEND USERNAME AND PASSEORD  TO THE NEW EMPLOYEE VIA EMAIL
        if user and user.email and helpdesk_user:
            employee_id = user.username
            employee = user.full_name
            employee_email = user.email
            employee_password = 'changeme'
            tasks.send_email_new_helpdesk_employee(
                employee, employee_id, employee_email, employee_password)

        return Response({'data': emp_id},
                        status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        # # print(data)
        # return Response(serializer.errors,
        #                 status=status.HTTP_400_BAD_REQUEST)


@group_required('HR', 'Manager')
@api_view(['GET'])
def employee(request, emp_uiid):
    '''
    GET EMPLOYEE DETAIL API

    '''

    if request.method == 'GET':
        employee = get_object_or_404(
            Employee.objects.select_related('designation'), emp_uiid=emp_uiid)
        # employee = Employee.objects.select_related('designation').get(employee_id=employee_id)
        dependants = employee.beneficiarys.values()
        educations = employee.educations.values()
        memberships = employee.memberships.values()
        employments = employee.employments.values()
        serializer = GetEmployeeSerializer(employee)

        data = {
            'employee': serializer.data,
            'dependants': dependants,
            'educations': educations,
            'memberships': memberships,
            'employments': employments,
        }

        # print(data)
        return Response(data)

        # return Response(serializer.data,dependants)


def employee_data(request, emp_uiid):
    '''
    GET EMPLOYEE DETAIL

    '''

    employee = get_object_or_404(
        Employee.objects.select_related('designation'), emp_uiid=emp_uiid)

    dependants = employee.beneficiarys.values()
    educations = employee.educations.values()
    memberships = employee.memberships.values()
    employments = employee.employments.values()
    serializer = GetEmployeeSerializer(employee)

    context = {
        'employee': serializer.data,
        'dependants': dependants,
        'educations': educations,
        'memberships': memberships,
        'employments': employments,
    }

    return render(request, 'employees/employee_data.html', context)


@api_view(['POST', 'GET'])
def add_dependants(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)

    if request.method == 'POST':
        # data = dict(request.data)
        data = request.data

        dependants = {
            'employee': employee,
            "gender": data.get('gender'),
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "other_name": data.get('other_name'),
            "dob": data.get('dob'),
            "mobile": data.get('mobile'),
            "address": data.get('address'),

        }

        try:
            Dependant.objects.create(**dependants)

        except IntegrityError as e:
            print(e)
            if 'UNIQUE constraint' in e.args[0]:

                return Response({'data': 'error'})

        return Response({'data': 'success'})


@api_view(['POST', 'GET'])
def add_education(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)

    if request.method == 'POST':
        data = request.data

        education = {
            'employee': employee,
            "school_name": data.get('school_name'),
            "course": data.get('course'),
            "certificate": data.get('certificate'),
            "date_completed": data.get('date_completed'),


        }
        try:
            Education.objects.create(**education)

        except IntegrityError as e:
            print(e)
            if 'UNIQUE constraint' in e.args[0]:

                return Response({'data': 'error'})

        return Response({'data': 'success'})


@api_view(['POST', 'GET'])
def add_membership(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)

    if request.method == 'POST':
        data = request.data

        membership = {
            'employee': employee,
            "name": data.get('name'),
            # "date_completed": data.get('date_completed'),

        }
        try:
            ProfessionalMembership.objects.create(**membership)

        except IntegrityError as e:
            print(e)
            if 'UNIQUE constraint' in e.args[0]:

                return Response({'data': 'error'})

        return Response({'data': 'success'})


@api_view(['POST', 'GET'])
def add_emploment(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)

    if request.method == 'POST':
        data = request.data

        employment = {
            'employee': employee,
            "company": data.get('company'),
            "job_title": data.get('job_title'),
            "date": data.get('date_completed'),
        }

        # print(employment)
        try:
            PreviousEployment.objects.create(**employment)

        except IntegrityError as e:
            print(e)
            if 'UNIQUE constraint' in e.args[0]:

                return Response({'data': 'error'})

        return Response({'data': 'success'})


@api_view(['POST', 'GET'])
def filename(request):
    if request.method == 'GET':
        filenames = File.objects.values('name', 'pk')

        return Response({'data': filenames}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        name = File.objects.create(name=request.POST.get('filename'))

        return Response(data=name.name, status=status.HTTP_201_CREATED)


# DOCUMENT MANAGEMENT
@api_view(['GET', 'POST'])
def add_document(request, employee_id):
    if request.method == 'GET':

        document = Documente.objects.filter(employee__employee_id=employee_id)
        serializer = DocumentSerializer(document, many=True)

        data = {
            'document': serializer.data,
        }
        return Response(data, status=200)

    if request.method == 'POST':
        employee = get_object_or_404(Employee, employee_id=employee_id)

        file = request.FILES.get('document')
        description = request.data.get('description')
        date = request.data.get('date')
        filename = request.data.get('document_id')

        document = Documente.objects.create(
            employee=employee, description=description, date=date, file=file, filename_id=filename)

        serializer = DocumentSerializer(document)

        return Response(serializer.data)


# EMPLOYEE EXIT ENDPOINT
@api_view(['POST'])
def exit_employee(request, employee_id):
    employee = Employee.objects.get(employee_id=employee_id)
    employee_status = request.data.get('employee_status')
    date_exited = request.data.get('date_exited')
    exit_check = request.data.get('exit_check', False)

    employee.status = employee_status
    employee.date_exited = date_exited
    employee.exit_check = exit_check

    employee.save()

    if employee:
        data = {
            'status': employee.status,
            'employee_id': employee_id
        }
        return Response(data=data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delate_document(request, employee_id, pk):
    document = get_object_or_404(
        Documente, employee__employee_id=employee_id, pk=pk)
    document.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


# APPLY FOR LEAVE

@api_view(['POST', 'GET'])
def apply_leave(request, employee_id):

    # employee = get_object_or_404(Employee,employee_id=employee_id)
    employee = get_object_or_404(Employee, ~Q(id=4) & Q(status='active') & Q(
        employee_id=employee_id) | Q(email=employee_id))

    # handle_over_to = list(Employee.objects.values(
    #     'pk', 'first_name', 'last_name').filter(department=employee.department, status='active').exclude(employee_id=employee_id))

    # print(handle_over_to.query)

    leave_policies = list(LeavePolicy.objects.values('pk', 'name', 'days'))

    on_leave = employee.leave_employees.filter(
        from_leave=False, employee__employee_id=employee_id).exists()

    if request.method == 'GET':
        leave_data = {
            'user_name': employee.full_name,
            'employee_id': employee.employee_id,
            'phone': employee.mobile,
            'email': employee.email,
            # 'handle_over_to': handle_over_to,
            'leave_policies': leave_policies,
            'on_leave': on_leave,
        }

        return Response({'data': leave_data})

    elif request.method == 'POST':
        data = request.data
        file = request.FILES.get('file')

        leave_data = {
            'employee': employee,
            "start": data.get('start'),
            "end": data.get('end'),
            "phone": data.get('phone'),
            "policy_id": data.get('policy'),
            "resuming_date": data.get('resuming_date'),
            "file": file,
            # "handle_over_to_id": data.get('handle_over_to'),

        }

        leave = Leave.objects.create(**leave_data)

        # print(leave)

        employee = leave.employee.full_name
        start = leave.start
        end = leave.end
        policy = leave.policy.name
        handle_over_to = '',#leave.handle_over_to.full_name
        department_email = leave.employee.department.email
        on_leave = leave.from_leave
        leave_days = leave.leavedays

        # SEND EMAIL TO HOD AND HR
        tasks.apply_for_leave_email(
            employee, start, end, leave_days, policy, handle_over_to, department_email)

        return Response({'data': str(leave_data), 'on_leave': on_leave})


def bool_values(value):
    return True if value else False


def file_exists(old_file, new_file):
    if old_file and new_file:
        return new_file
    elif new_file and old_file:
        return new_file
    elif old_file and not new_file:
        return old_file
    else:
        return


@api_view(['POST'])
def update_leave(request, leave_id):

    leave = get_object_or_404(Leave, pk=leave_id)

    old_file = leave.file
    new_file = request.FILES.get('file')

    data = request.data

    # print(data.get('on_leave'))

    # print('supervisor ', data.get('supervisor'))

    supervisor = bool_values(data.get('supervisor'))
    line_manager = bool_values(data.get('line_manager'))
    hr_manager = bool_values(data.get('hr_manager'))
    from_leave = bool_values(data.get('on_leave'))

    leave.employee = leave.employee
    leave.start = data.get('start')
    leave.end = data.get('end')
    leave.phone = data.get('phone')
    leave.policy_id = data.get('policy')
    leave.resuming_date = data.get('resuming_date')
    leave.status = data.get('status')
    leave.file = file_exists(old_file, new_file)
    # leave.handle_over_to_id = data.get('handle_over_to')
    leave.supervisor = supervisor
    leave.hr_manager = hr_manager
    leave.line_manager = line_manager
    leave.from_leave = from_leave
    leave.save()

    data = {
        'leave_id': leave_id,
        'on_leave': leave.from_leave
    }
    return Response(data)


# DISPLAY LEAVE BASED ON USER RIGHTS
@api_view(['GET'])
def leaves(request, employee_id):
    """
    DISPLAY USER LEAVE
    """
    employee = get_object_or_404(
        Employee, employee_id=employee_id, status='active')

    leave = Leave.objects.select_related(
        'employee').filter(employee__status='active')

    if employee.department.name == 'Human Resource':

        # if any(x in ['GM', 'HR'] for x in group):

        leave = leave.all()

    # elif 'HOD' in group:
    elif employee.is_head:
        leave = leave.filter(employee__department=employee.department)

    # else:
    #     leave = leave.filter(Q(employee__employee_id=employee_id) | Q(
    #         handle_over_to__employee_id=employee_id))

    serializer = LeaveSerializer(leave, many=True)

    user_group = {
        # 'name': group,
        'hr': employee.department.name == 'Human Resource',
        'hod': employee.is_head
    }
    # print(user_group)
    return Response({'data': serializer.data, 'user_type': user_group})

# GET EMPLOYEE LEAVE HISTORY


@api_view(['GET'])
def employee_leave(request, employee_id):

    leave = Leave.objects.select_related().filter(
        employee__employee_id=employee_id).order_by('start', 'policy__name')

    serializer = LeaveSerializer(leave, many=True)

    leave_per_year = leave.values(
        'policy__name', 'start__year', 'policy__days').annotate(total_spent=Sum('leavedays'),
                                                                out_standing=F(
                                                                    'policy__days') - F('total_spent'),
                                                                num_application=Count('policy__name')).\
        order_by('-start__year', 'policy__days')

    document_count = Documente.objects.filter(
        employee__employee_id=employee_id).count()

    print(document_count)

    data = {
        'employees': serializer.data,
        'leave_per_year': leave_per_year,
        'document_count': document_count,
    }

    # print(leave.values('employee__employee_documents'))

    return Response(data)


@api_view(['GET'])
def getleave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)

    policies = LeavePolicy.objects.values('pk', 'name', 'days')
    collegues = Employee.objects.filter(
        department=leave.employee.department, status='active').values('pk', 'first_name', 'last_name').exclude(employee_id=leave.employee.employee_id)

    # user = leave.employee.my_group

    # print(user)

    data = {
        'name': leave.employee.full_name,
        # 'handle_over_to': leave.handle_over_to.full_name,
        'start_date': leave.start,
        'email': leave.employee.email,
        'end_date': leave.end,
        'leave_days': leave.leavedays,
        'status': leave.status,
        'phone': leave.phone,
        'policy': leave.policy.name,
        'resuming_date': leave.resuming_date,
        'file': leave.file_exists,
        'supervisor': leave.supervisor,
        'line_manager': leave.line_manager,
        'hr_manager': leave.hr_manager,
        'on_leave': leave.from_leave,
        'policies': policies,
        'collegues': collegues,
        'employee_id': leave.employee.employee_id,
        # 'hr':leave.employee.department =='Human Resource',
        # 'hod':leave.employee.is_head

    }

    return Response(data)


@api_view(['GET'])
def designation(request):
    departments = list(Department.objects.values('pk', 'name'))
    designations = list(Designation.objects.values(
        'pk', 'name', 'department', 'net_month_salary'))

    data = {
        'departments': departments,
        "designations": designations,
    }

    return Response(data)
