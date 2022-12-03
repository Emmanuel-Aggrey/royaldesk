import os
import sys
from datetime import datetime
from decouple import config
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

from .serializers import (EmployeeSerializer, AllEmployeeSerializer,
                        DependantSerializer,EducationSerializer,PreviousMembershipSerializer,
                        PreviousEploymentSerializer,LeaveSerializer, DocumentSerializer)


default_password = config('DEFAULT_PASSWORD')

def date_value(value):
    return value if value else None

@api_view(['GET', 'POST'])
def allemployees(request):

    if request.method == 'GET':

        employees = Employee.employees.select_related('designation')#.exclude(for_management=True)
        serializer = AllEmployeeSerializer(employees, many=True)

        data = {
            'employees': serializer.data,

        }

        return Response(data)

    if request.method == 'POST':
        serializer = AllEmployeeSerializer(data=request.data)

        if serializer.is_valid():   

            helpdesk_user = bool(int(request.data.get('helpdesk_user')))
            applicant=date_value(request.data.get('applicant'))

            employee = serializer.save(applicant_id=applicant)
            employee_key = employee.employee_id
            user = User(password=default_password,username=employee.employee_id, first_name=employee.first_name, last_name=employee.last_name, is_head=employee.is_head,
                    email=employee.email, department_id=employee.department_id, designation_id=employee.designation_id, profile=employee.profile)
            user.set_password(default_password)
            # user.has_usable_password(user.password)
            

         # GET DEPARTMENT SHORTNAME
            department = employee.department.shortname

            # CREATE HELPDESK USER AND ADD TO GROUP
            group = Group.objects.prefetch_related().filter(name=department).last()
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
                employee_password = default_password
                tasks.send_email_new_helpdesk_employee(
                    employee, employee_id, employee_email, employee_password)


            data ={
                'data':employee_key
            }
            return Response(data=data,status=status.HTTP_201_CREATED)

        if serializer.errors:
    
            data = {
                'errors': serializer.errors
            }
            return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)





# @group_required('HR', 'MNG')
@api_view(['GET', 'POST'])
def employees(request):

    if request.method == 'GET':

        employees = Employee.employees.select_related('designation')#.exclude(for_management=True)
        serializer = EmployeeSerializer(employees, many=True)


        on_leave = employees.values('leave_employees__from_leave','leave_employees__hr_manager').aggregate(
        on_leave=(
            Count('id', filter=Q(leave_employees__from_leave=False,leave_employees__hr_manager=True))
        ),
        not_on_leave=(
            Count('id', filter=Q(leave_employees__from_leave=True,leave_employees__hr_manager=True))
        ),
        )

        # print(on_leave)

        employees_on_leave = employees.filter(leave_employees__from_leave=False,leave_employees__hr_manager=True).count()
        employees_exceed_leave = employees.filter(leave_employees__from_leave=False, leave_employees__hr_manager=True,leave_employees__resuming_date__gt=datetime.now()).count()
    
        # employees_requested_leave = employees.filter(leave_employees__from_leave=False,).count()
        

        data = {
            'employees': serializer.data,
            'employees_on_leave': employees_on_leave,
            'employees_exceed_leave': employees_exceed_leave,
        }

        return Response(data)



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
        serializer = AllEmployeeSerializer(employee)

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
    serializer = AllEmployeeSerializer(employee)

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
    serializer = DependantSerializer(data=request.data)

    if serializer.is_valid():
        dependant = serializer.save(employee=employee)
        print(serializer.data)
        dependant = dependant.full_name
        return Response(data=dependant,status=status.HTTP_201_CREATED)

    if serializer.errors:
        data = {
                'errors': serializer.errors
            }
        print(serializer.errors)
        return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST', 'GET'])
def add_education(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)
    serializer = EducationSerializer(data=request.data)

    if serializer.is_valid():
        school = serializer.save(employee=employee)
        print(serializer.data)
        school_name = school.school_name
        return Response(data=school_name,status=status.HTTP_201_CREATED)

    if serializer.errors:
        data = {
                'errors': serializer.errors
            }
        print(serializer.errors)
        return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST', 'GET'])
def add_membership(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)
    serializer = PreviousMembershipSerializer(data=request.data)

    if serializer.is_valid():
        membership = serializer.save(employee=employee)
        print(serializer.data)
        membership = membership.name
        return Response(data=membership,status=status.HTTP_201_CREATED)

    if serializer.errors:
        data = {
                'errors': serializer.errors
            }
        print(serializer.errors)
        return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST', 'GET'])
def add_emploment(request, employee_id):

    employee = Employee.objects.get(employee_id=employee_id)
    serializer = PreviousEploymentSerializer(data=request.data)

    if serializer.is_valid():
        employment = serializer.save(employee=employee)
        print(serializer.data)
        employment = str(employment)
        return Response(data=employment,status=status.HTTP_201_CREATED)

    if serializer.errors:
        data = {
                'errors': serializer.errors
            }
        print(serializer.errors)
        return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


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
@api_view(['POST','GET'])
@group_required('HR', 'MNG')

def exit_employee(request, employee_id):
    employee = Employee.objects.get(employee_id=employee_id)

    if request.method == 'GET':

        data = {
            'employee': employee_id,
            'employee_status':employee.status,
            'date_exited': employee.date_exited,
            'exit_check': employee.exit_check,
            'reason_exiting':employee.reason_exiting,
        }

        

        return Response(data)

    if request.method == 'POST':
        employee_status = request.data.get('employee_status','active')
        date_exited = request.data.get('date_exited')

        reason_exiting = request.data.get('reason_exiting')

            
        exit_check = partials.bool_values(request.data.get('exit_check', False))

        # print('employee_status',employee_status,exit_status,date_exited,exit_check)

        # employee.status = employee_status
        # employee.date_exited = date_exited
        # employee.exit_check = exit_check
        # employee.reason_exiting = reason_exiting
        
        
       
        date = datetime.strptime(date_exited,'%Y-%m-%d')
        tasks.employee_exiting.apply_async(eta=date,args=(employee_id, date_exited, employee_status, exit_check,reason_exiting))


        # employee.save()

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


# APPLY FOR LEAVE FORM ONLY

@api_view(['POST', 'GET'])
def apply_leave(request, employee_id):

    employee = get_object_or_404(Employee.activeemployees, Q(employee_id=employee_id) | Q(email=employee_id))

    leave_policies = list(LeavePolicy.objects.values('pk', 'name', 'days'))

    on_leave = employee.leave_employees.filter(
        from_leave=False, employee__employee_id=employee_id).exists()

    if request.method == 'GET':
        leave_data = {
            'user_name': employee.full_name,
            'employee_id': employee.employee_id,
            'phone': employee.mobile,
            'email': employee.email,
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

        }

        leave = Leave.objects.create(**leave_data)

        # print(leave)

        employee = leave.employee.full_name
        start = leave.start
        end = leave.end
        policy = leave.policy.name
        department_email = leave.employee.department.email
        on_leave = leave.from_leave
        leave_days = leave.leavedays

        # SEND EMAIL TO HOD AND HR
        tasks.apply_for_leave_email(
            employee, start, end, leave_days, policy, department_email)

        return Response({'data': str(leave_data), 'on_leave': on_leave})



# DISPLAY LEAVE BASED ON USER RIGHTS
@api_view(['GET'])
def leaves(request, employee_id):
    """
    DISPLAY USER LEAVE
    """
    employee = get_object_or_404(Employee.activeemployees,employee_id=employee_id)


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
    # print('status1', new_supervisor, 'status2', old_supervisor)

# check the status of leave approvals if changed or not and update accordingly
    if partials.check_approval_status_change(new_supervisor, old_supervisor, 'supervisor', employee):
        # print('new state update status')
        leave.supervisor_approval = partials.check_approval_status_change(
            new_supervisor, old_supervisor, 'supervisor', employee)
    else:
        # print('old state dont update status')
        pass

    if partials.check_approval_status_change(new_line_manager, old_line_manager, 'line_manager', employee):
        # print('new state update status')
        leave.line_manager_approval = partials.check_approval_status_change(
            new_line_manager, old_line_manager, 'line_manager', employee)
    else:
        # print('old state dont update status')
        pass

    if partials.check_approval_status_change(new_hr_manager, old_hr_manager, 'hr_manager', employee):
        # print('new state update status')
        leave.hr_manager_approval = partials.check_approval_status_change(
            new_hr_manager, old_hr_manager, 'hr_manager', employee)
    else:
        # print('old state dont update status')
        pass

    # print(leave.supervisor_approval)

    leave.save()

    data = {
        'leave_id': leave_id,
        'on_leave': leave.from_leave
    }
    return Response(data)



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
    # print(out_standing_leaves)

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
    # employee_id

    data = {
        'name': leave.employee.full_name,
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
        'employee_id': leave.employee.employee_id,
    

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
