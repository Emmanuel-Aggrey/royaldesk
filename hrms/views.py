import os
import sys
from datetime import datetime

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, models
from django.db.models import Count, F, Q, Sum, Variance, FloatField
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
from . import partials
from .import tasks
from .models import (Department, Dependant, Designation, Education, Employee,
                     Leave, LeavePolicy, PreviousEployment,
                     ProfessionalMembership, Documente, File)
from helpdesk.models import User

from .serializers import (EmployeeSerializer, GetEmployeeSerializer,
                          LeaveSerializer, DocumentSerializer)


def date_value(value):
    return value if value else None


# @group_required('HR', 'MNG')
@api_view(['GET', 'POST'])
def employees(request):

    if request.method == 'GET':

        employees = Employee.objects.exclude(for_management=True)
        serializer = EmployeeSerializer(employees, many=True)
        # employees_on_leave = Leave.objects.filter(from_leave=False).count()
        employees_exceed_leave = Leave.objects.filter(
            from_leave=False, resuming_date__gt=datetime.now()).count()

        data = {
            'employees': serializer.data,
            'employees_on_leave': employees_on_leave,
            'employees_exceed_leave': employees_exceed_leave
        }

        return Response(data)

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


@group_required('HR', 'MNG')
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

@group_required('HR', 'MNG')
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
        'employee': employee,#serializer.data,
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

@group_required('HR', 'MNG')

@api_view(['POST', 'GET'])
def filename(request):
    if request.method == 'GET':
        filenames = File.objects.values('name', 'pk')

        return Response({'data': filenames}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        name = File.objects.create(name=request.POST.get('filename'))

        return Response(data=name.name, status=status.HTTP_201_CREATED)


# DOCUMENT MANAGEMENT
@group_required('HR', 'MNG')
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
@group_required('HR', 'MNG')

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
@group_required('HR', 'MNG')

def delate_document(request, employee_id, pk):
    document = get_object_or_404(
        Documente, employee__employee_id=employee_id, pk=pk)
    document.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


# APPLY FOR LEAVE

@api_view(['POST', 'GET'])
def apply_leave(request, employee_id):

    # employee = get_object_or_404(Employee,employee_id=employee_id)
    employee = get_object_or_404(Employee, ~Q(for_management=True) & Q(status='active') & Q(
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
       # handle_over_to = '',#leave.handle_over_to.full_name
        department_email = leave.employee.department.email
        on_leave = leave.from_leave
        leave_days = leave.leavedays

        # SEND EMAIL TO HOD AND HR
        tasks.apply_for_leave_email(
            employee, start, end, leave_days, policy, department_email)

        return Response({'data': str(leave_data), 'on_leave': on_leave})


@api_view(['POST'])
def update_leave(request, leave_id):

    leave = get_object_or_404(Leave, pk=leave_id)

    old_file = leave.file
    new_file = request.FILES.get('file')

    data = request.data
    employee = data.get('leave_user')

    # supervisor
    new_supervisor = partials.bool_values(data.get('supervisor'))
    old_supervisor = leave.supervisor

    # line_manager
    new_line_manager = partials.bool_values(data.get('line_manager'))
    old_line_manager = leave.line_manager

    # hr_manager
    new_hr_manager = partials.bool_values(data.get('hr_manager'))
    old_hr_manager = leave.hr_manager

    # print(data.get('leave_user'))

    # print('supervisor ', data.get('supervisor'))

    supervisor = new_supervisor
    line_manager = new_line_manager
    hr_manager = new_hr_manager
    from_leave = partials.bool_values(data.get('on_leave'))
    leave.employee = leave.employee
    leave.start = data.get('start')
    leave.end = data.get('end')
    leave.phone = data.get('phone')
    leave.policy_id = data.get('policy')
    leave.resuming_date = data.get('resuming_date')
    leave.status = data.get('status')
    leave.file = partials.file_exists(old_file, new_file)
    leave.supervisor = supervisor
    leave.hr_manager = hr_manager
    leave.line_manager = line_manager
    leave.from_leave = from_leave
    print('status1', new_supervisor, 'status2', old_supervisor)

# check the status of leave approvals if changed or not and update accordingly
    if partials.check_approval_status_change(new_supervisor, old_supervisor, 'supervisor', employee):
        print('new state update status')
        leave.supervisor_approval = partials.check_approval_status_change(
            new_supervisor, old_supervisor, 'supervisor', employee)
    else:
        print('old state dont update status')

    if partials.check_approval_status_change(new_line_manager, old_line_manager, 'line_manager', employee):
        print('new state update status')
        leave.line_manager_approval = partials.check_approval_status_change(
            new_line_manager, old_line_manager, 'line_manager', employee)
    else:
        print('old state dont update status')

    if partials.check_approval_status_change(new_hr_manager, old_hr_manager, 'hr_manager', employee):
        print('new state update status')
        leave.hr_manager_approval = partials.check_approval_status_change(
            new_hr_manager, old_hr_manager, 'hr_manager', employee)
    else:
        print('old state dont update status')

    # print(leave.supervisor_approval)

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

    department = ['HR', 'MNG']
    if employee.department.shortname in department:

        # if any(x in ['GM', 'HR'] for x in group):

        leave = leave.all()

    # elif 'HOD' in group:
    elif employee.is_head:
        leave = leave.filter(employee__department=employee.department)

    else:
        leave = leave.filter(employee__employee_id=employee_id)

    serializer = LeaveSerializer(leave, many=True)

    user_group = {
        # 'name': group,
        'hr': employee.department.shortname in department,
        'hod': employee.is_head
    }
    # print(user_group)
    return Response({'data': serializer.data, 'user_type': user_group})

# GET EMPLOYEE LEAVE HISTORY


@api_view(['GET'])
def employee_leave(request, employee_id):

    leave = Leave.objects.select_related().filter(
        employee__employee_id=employee_id).order_by('-start__year', 'policy__name')

    serializer = LeaveSerializer(leave, many=True)
    last_date_on_leave = leave.values_list('resuming_date', flat=True).filter(
        employee__employee_id=employee_id, hr_manager=True).last()

    leave_per_year = leave.values(
        'policy__name', 'start__year', 'policy__days', 'policy__has_days').annotate(total_spent=Sum('leavedays'),
                                                                                    out_standing=F(
            'policy__days') - F('total_spent'),
        num_application=Count('policy__name')).\
        order_by('-start__year', 'policy__name')

    out_standing_leaves = leave_per_year.filter(
        policy__has_days=True).aggregate(out_standing_leaves=Sum('out_standing'))
    # out_standing_leaves = leave.values(
    #     'policy__name','end__year').filter(policy__has_days=True).annotate(total_spent=Sum('leavedays'),
    #                                                             out_standing=F(
    #                                                                 'policy__days') - F('total_spent'))

    # num_application=Count('policy__name'))
    print(out_standing_leaves)

    document_count = Documente.objects.filter(
        employee__employee_id=employee_id).count()

    # print(leave_per_year)

    data = {
        'employees': serializer.data,
        'leave_per_year': leave_per_year,
        'document_count': document_count,
        'last_date_on_leave': last_date_on_leave,
        'out_standing_leaves': out_standing_leaves.get('out_standing_leaves'),
    }

    # print(leave.values('employee__employee_documents'))

    return Response(data)


@api_view(['GET'])
def getleave(request, pk):
    leave = get_object_or_404(Leave, pk=pk)

    policies = LeavePolicy.objects.values('pk', 'name', 'days')
    # collegues = Employee.objects.filter(
    #     department=leave.employee.department, status='active').values('pk', 'first_name', 'last_name').exclude(employee_id=leave.employee.employee_id)

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
        # 'collegues': collegues,
        'employee_id': leave.employee.employee_id,
        # 'hr':leave.employee.department =='Human Resource',
        # 'hod':leave.employee.is_head

    }

    return Response(data)


def leave_application_detail(request, employee, leave_id):
    employee_leave = Leave.objects.select_related('employee').filter(employee__employee_id=employee)
    leave =  get_object_or_404(employee_leave,pk=leave_id)# employee_leave.get(pk=leave_id)
    # policy = leave.policy.name
    leave_year = leave.end.strftime('%Y')


    last_date_on_leave = employee_leave.values_list('resuming_date', flat=True).filter(
        employee__employee_id=employee, hr_manager=True).last()

    leave_per_year = employee_leave.filter(policy__name=leave.policy.name, end__year=leave_year).values(
        'policy__name', 'end__year').annotate(total_spent=Sum('leavedays'),
                                              out_standing=F(
            'policy__days') - F('total_spent')).order_by('-start__year')


    out_standing_days = leave_per_year.filter(policy__has_days=True).aggregate(out_standing_days=Sum('out_standing'))

    # available_days  = leavedays - sum of previous + current
    prev_issue = leave_per_year.filter(id__lt=leave_id).exclude(id=leave_id).order_by('-id').aggregate(prev_issue=Sum('leavedays'))

    # prev_issue = leave_per_year.exclude(id=leave_id).order_by('-id').aggregate(prev_issue=Sum('leavedays'))

    policy_days = leave.policy.days
    prev_issue  =  prev_issue.get('prev_issue') if prev_issue.get('prev_issue') else 0
    current = leave.leavedays


    available_days = policy_days-(prev_issue+current)

    # print(available_days)
  
    # next_issue = (leave_per_year
    # .filter(id__gt=leave_id)
    # .exclude(id=leave_id)
    # .order_by('id')
    # .first())

    context = {
        'leave': leave,
        'last_date_on_leave': last_date_on_leave,
        'out_standing_days': out_standing_days.get('out_standing_days'),
        'leave_per_year': leave_per_year,
        'available_days':available_days if leave.policy.has_days else 'N/A'
    }

    return render(request, 'leave/leave_application_detail.html', context)


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
