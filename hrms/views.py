import os
import sys
import time
from datetime import datetime, timedelta

from decouple import config
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, models, transaction
from django.db.models import Count, F, FloatField, Q, Sum, Variance
from django.http import JsonResponse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render, resolve_url, reverse)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView, View)
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from applicant.models import ApplicantOfferLeter
from helpdesk.models import User
from hrms import partials, tasks
from HRMSPROJECT import sql_server
from HRMSPROJECT.custome_decorators import group_required

from .models import (Applicant, Department, Dependant, Designation, Documente,
                     Education, Employee, EmployeeExit, File, Leave,
                     LeavePolicy, PreviousEployment, ProfessionalMembership,
                     RequestChange)
from .serializers import (AllEmployeeSerializer, DependantSerializer,
                          DocumentSerializer, EducationSerializer,
                          EmployeeExitSerializer, EmployeeSerializer,
                          LeaveSerializer, PreviousEploymentSerializer,
                          PreviousMembershipSerializer, RequestChangeSerilizer)

default_password = config('DEFAULT_PASSWORD')
HR_EMAIL = config('HR_EMAIL')
LEAVE_REMINDER_HOURS = config('LEAVE_REMINDER_HOURS', cast=int)


def date_value(value):
    return value if value else None


@login_required
@api_view(['GET', 'POST'])
def allemployees(request):

    if request.method == 'GET':

        employees = Employee.employees.select_related(
            'designation')  # .exclude(for_management=True)
        serializer = AllEmployeeSerializer(employees, many=True)

        # print(serializer.data)
        data = {
            'employees': serializer.data,

        }

        return Response(data)

    if request.method == 'POST':

        # is_applicant = request.user.applicant.is_applicant #check if user is an applicant

        is_applicant = request.user.is_applicant
        is_helpdesk_user = bool(int(request.data.get('helpdesk_user', False)))
        is_anviz_user = bool(int(request.data.get('anviz_user', False)))

        # WHEN IS MARRIED IS SELECTED
        is_merried_relation = request.data.get('is_merried_relation', False)
        first_name = request.data.get('is_merried_f_name')
        last_name = request.data.get('is_merried_l_name')
        mobile = request.data.get('is_merried_phone')

        # anviz_department_id = request.data.get('anviz_department')

        serializer = AllEmployeeSerializer(data=request.data)

        print('is_anviz_user', is_anviz_user)
        # print('anviz_department_id',anviz_department_id)
        print('is_helpdesk_user ', is_helpdesk_user)
        print('is_applicant', is_applicant)

        if serializer.is_valid() and not is_applicant:

            """ 
                CREATE AN EMPLOYEE AND ADD TO USERS
            """

            applicant = date_value(request.data.get('applicant'))

            try:
                employee = serializer.save(applicant_id=applicant)
                anviz_department = employee.department.anviz_department

                # tasks.create_anviz_employee(employee.full_name, employee.gender.capitalize(), anviz_department_id, employee.country, employee.dob.strftime('%Y-%m-%d'),
                #                                       employee.date_employed.strftime('%Y-%m-%d'), employee.mobile, employee.position,
                #                                       employee.place_of_birth, employee.employee_id, employee.address)

                employee_key = employee.emp_uiid
                if is_merried_relation:

                    # gender if is_merried_relation == 'Wife' else 'female'
                    # 'female' if is_merried_relation == 'Wife' else 'male'
                    gender = 'female' if is_merried_relation == 'Wife' else 'male'

                    Dependant.objects.create(employee=employee, relation=is_merried_relation,
                                             mobile=mobile, first_name=first_name, last_name=last_name, gender=gender)

                if applicant is None:

                    user = User(username=employee.employee_id, first_name=employee.first_name, last_name=employee.last_name, is_head=employee.is_head,
                                email=employee.email, department_id=employee.department_id, designation_id=employee.designation_id, profile=employee.profile)
                    user.set_password(default_password)

                    # CREATE ANVIZ USER
                    if is_anviz_user and anviz_department:
                        tasks.create_anviz_employee.delay(employee.full_name, employee.gender.capitalize(), anviz_department, employee.country, employee.dob.strftime('%Y-%m-%d'),
                                                          employee.date_employed.strftime(
                            '%Y-%m-%d'), employee.mobile, employee.position,
                            employee.place_of_birth, employee.employee_id, employee.address)

                # GET DEPARTMENT SHORTNAME
                    department = employee.department.shortname

                # CREATE HELPDESK USER AND ADD TO GROUP
                    group = Group.objects.prefetch_related().filter(name=department).last()
                    if user and is_helpdesk_user and group:
                        user.is_staff = True
                        user.save()
                        user.groups.add(group)
                        employee.user = user
                        employee.save()

                    # CREATE HELPDESK USER WITH NO EMAIL ADDRESS
                    if user and is_helpdesk_user:
                        user.is_normal_user = False
                        user.save()
                        employee.user = user
                        employee.save()

                    # SEND USERNAME AND PASSEORD  TO THE NEW EMPLOYEE VIA EMAIL
                    if user and user.email and is_helpdesk_user:
                        employee_id = user.username
                        employee_name = user.full_name
                        employee_email = user.email
                        employee_password = default_password

                        # SEND EMAIL TO NEW USER  VIA CELERY

                        tasks.send_email_new_helpdesk_employee(
                            employee_name, employee_id, employee_email, employee_password)

                    if user and not is_helpdesk_user:
                        user.is_normal_user = True
                        user.save()
                        employee.user = user
                        employee.save()

                    if user and user.email and not is_helpdesk_user:
                        employee_id = user.username
                        employee_name = user.full_name
                        employee_email = user.email
                        employee_password = default_password
                        # SEND EMAIL TO NEW USER VIA CELERY

                        tasks.send_email_new_employee.delay(
                            employee_name, employee_id, employee_email, employee_password)

                if applicant is not None:

                    ''' SAVING AN APPLICANT AS AN EMPLOYEE WITH NO USER NAME VALUES 
                        CREATED AS USER WHEN SELECTED AS AN APPLICANT 
                    '''

                    # MOVED THIS TO VERIFY APPICANT FUNCTION
                    # applicant = employee.applicant

                    # applicant.is_applicant = False
                    # applicant.save()

                    employee.user = employee.applicant.user
                    employee.save()

                    if is_helpdesk_user:
                        # print('TRUE HELP is_helpdesk_user',is_helpdesk_user)
                        helpdesk_user = employee.user
                        helpdesk_user.is_normal_user = False
                        helpdesk_user.save()

                    # print('ALL HELP is_helpdesk_user',is_helpdesk_user)

                    if is_anviz_user and anviz_department:
                        tasks.create_anviz_employee.delay(employee.full_name, employee.gender.capitalize(), anviz_department, employee.country, employee.dob.strftime('%Y-%m-%d'),
                                                          employee.date_employed.strftime(
                            '%Y-%m-%d'), employee.mobile, employee.position,
                            employee.place_of_birth, employee.employee_id, employee.address)

                data = {
                    'data': employee_key,
                    'is_applicant': True if applicant else False,
                }

                return Response(data=data, status=status.HTTP_201_CREATED)

            except IntegrityError as e:

                data = {
                    'unique_contraints': 'Employee Already Exists',
                }
                return Response(data=data)

        if serializer.errors:

            data = {
                'errors': serializer.errors
            }
            print(serializer.errors)
            return Response(data)

        if serializer.is_valid() and is_applicant:

            """ 
            CREATE EMPLOYEE AS AN APPLICANT 
            """

            print('is_applicant', is_applicant)
            applicant = request.data.get('applicant')
            user = request.user.username
            try:

                employee = serializer.save(
                    applicant_id=applicant, employee_id=user)
                employee_key = employee.emp_uiid

                employee.user = request.user
                employee.save()

                if is_merried_relation:
                    gender = 'female' if is_merried_relation == 'Wife' else 'male'
                    Dependant.objects.update(employee=employee, relation=is_merried_relation,
                                             mobile=mobile, first_name=first_name, last_name=last_name, gender=gender)

                # user = request.user
                # user.is_applicant = False
                # user.save()
                # print('user app',user.is_applicant)

                data = {
                    'data': employee_key,
                    'is_applicant': is_applicant
                }
                return Response(data=data, status=status.HTTP_201_CREATED)

            except IntegrityError as e:

                data = {
                    'unique_contraints': 'Employee Already Exists',
                }
                return Response(data=data)

        if serializer.errors:

            data = {
                'errors': serializer.errors
            }
            return Response(data)

            # print(serializer.data)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET', 'POST'])
def updateEmployee(request, employee_id):
    try:
        employee = get_object_or_404(Employee, emp_uiid=employee_id)

        if request.method == 'GET':
            serializer = AllEmployeeSerializer(instance=employee)

            can_edit_employee = True if request.user.is_superuser or request.user.groups.filter(
                name='HR').exists() else False
            request_changes_state = employee.request_changes.values(
                'status').last()

            serializer = dict(serializer.data)
            serializer.update({'can_edit_employee': can_edit_employee})

            return Response(serializer, status=200)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        employee = get_object_or_404(Employee, emp_uiid=employee_id)
        # employee.request_change=False
        # employee.save()
        is_applicant = request.user.is_applicant
        is_helpdesk_user = bool(int(request.data.get('helpdesk_user', False)))

        is_anviz_user = bool(int(request.data.get('anviz_user', False)))

        # APPICANT UPDATING PERSONAL RECORDS
        serializer = AllEmployeeSerializer(employee, request.data)

        # check if employee made a request to change data, if yes change status to done after submit
        request_change = RequestChange.objects.filter(employee=employee).last()
        if request_change:
            request_change.status = 'done'
            request_change.save()

        # if request_change
        if serializer.is_valid() and is_applicant:

            employee = serializer.save()

            # employee.user = employee.applicant.user
            # employee.save()

        # EMPLOYEE UPDATING APPICANT  RECORDS
        if serializer.is_valid() and not is_applicant:
            employee = serializer.save()
            anviz_department = employee.department.anviz_department

            if is_helpdesk_user:
                helpdesk_user = employee.user
                helpdesk_user.is_normal_user = False
                helpdesk_user.save()

                # SENT THIS PART TO VERIFY FUNTION
            # if employee.user.is_applicant:
                # applicant = employee.applicant
                # applicant.is_applicant = False
                # applicant.save()

                # print('is_applicant ',employee.user.is_applicant)

                if is_anviz_user and anviz_department:
                    tasks.create_anviz_employee.delay(employee.full_name, employee.gender.capitalize(), anviz_department, employee.country, employee.dob.strftime('%Y-%m-%d'),
                                                      employee.date_employed.strftime(
                        '%Y-%m-%d'), employee.mobile, employee.position,
                        employee.place_of_birth, employee.employee_id, employee.address)

                    # print('created is_anviz_user',is_anviz_user)

        return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@group_required('HR')
def verify_data(request, employee_id):
    '''STATUS FROM APPLICANT TO EMPLOYEE VERIFICATION'''

    if request.method == 'POST':
        employee = get_object_or_404(Employee, emp_uiid=employee_id)
        if employee.applicant:
            applicant = employee.applicant
            applicant.is_applicant = False
            applicant.save()

            return JsonResponse({'data': 'record verified'})
        return JsonResponse({})
    return JsonResponse({'data': 'Method not Allowed'})

# @group_required('HR', 'MNG')


@api_view(['GET', 'POST'])
def employees(request):
    if request.method == 'GET':

        employees = Employee.employees.select_related(
            'designation')  # .exclude(for_management=True)
        serializer = EmployeeSerializer(employees, many=True)

        on_leave = employees.values('leave_employees__from_leave', 'leave_employees__hr_manager').aggregate(
            on_leave=(
                Count('id', filter=Q(leave_employees__from_leave=False,
                      leave_employees__hr_manager=True))
            ),
            not_on_leave=(
                Count('id', filter=Q(leave_employees__from_leave=True,
                      leave_employees__hr_manager=True))
            ),
        )

        # print(on_leave)

        employees_on_leave = employees.filter(
            leave_employees__from_leave=False, leave_employees__hr_manager=True).count()
        employees_exceed_leave = employees.filter(
            leave_employees__from_leave=False, leave_employees__hr_manager=True, leave_employees__resuming_date__gt=datetime.now()).count()

        # employees_requested_leave = employees.filter(leave_employees__from_leave=False,).count()
        data = {
            'employees': serializer.data,
            'employees_on_leave': employees_on_leave,
            'employees_exceed_leave': employees_exceed_leave,
        }

        return Response(data)


# @group_required('HR')
def employee_data(request, emp_uiid):
    '''
    GET EMPLOYEE DETAIL

    '''

    employee = get_object_or_404(
        Employee.objects.select_related('designation'), Q(emp_uiid=emp_uiid) | Q(employee_id=emp_uiid))

    dependants = employee.beneficiarys.values()
    educations = employee.educations.values()
    memberships = employee.memberships.all()
    employments = employee.employments.values()
    serializer = AllEmployeeSerializer(employee)

    context = {
        'employee': employee,  # serializer.data,
        'dependants': dependants,
        'educations': educations,
        'memberships': memberships,
        'employments': employments,
    }

    return render(request, 'employees/employee_data.html', context)


@api_view(['POST', 'GET'])
def add_dependants(request, employee_id):

    if request.method == 'GET':
        try:
            dependant = Dependant.objects.filter(
                employee__emp_uiid=employee_id)
            serializer = DependantSerializer(dependant, many=True)

            return Response(serializer.data)
        except:
            return Response(status=404)
        # print('employee',employee_id)

    if request.method == 'POST':
        employee = Employee.objects.get(emp_uiid=employee_id)
        print(employee)
        serializer = DependantSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save(employee=employee)
            # print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            data = {
                'errors': serializer.errors
            }
            print(serializer.errors)
            return Response(data)

    Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def deletedependent(request, employee_id, pk):
    if request.method == 'DELETE':
        dependant = get_object_or_404(
            Dependant, pk=pk, employee__emp_uiid=employee_id)
        key = dependant.id
        dependant.delete()
        return JsonResponse({'data': 'record deleted'})


@api_view(['POST', 'GET'])
def add_education(request, employee_id):
    if request.method == 'GET':
        try:
            education = Education.objects.filter(
                employee__emp_uiid=employee_id)
            serializer = EducationSerializer(education, many=True)
        # print(serializer.data)
            return Response(serializer.data)

        except:
            return Response(status=404)

    if request.method == 'POST':
        employee = Employee.objects.get(emp_uiid=employee_id)

        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee)
            # print(serializer.data)
            # school_name = school.school_name
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            data = {
                'errors': serializer.errors
            }
            print(serializer.errors)
            return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def deleteEducation(request, employee_id, pk):
    if request.method == 'DELETE':
        education = get_object_or_404(
            Education, pk=pk, employee__emp_uiid=employee_id)
        # key = education.id
        education.delete()
        return JsonResponse({'data': 'record deleted'})


@api_view(['POST', 'GET'])
def add_membership(request, employee_id):

    if request.method == 'GET':

        try:
            membership = ProfessionalMembership.objects.filter(
                employee__emp_uiid=employee_id)
            serializer = PreviousMembershipSerializer(membership, many=True)

            return Response(serializer.data)
        except:
            return Response(status=404)

    if request.method == 'POST':
        employee = Employee.objects.get(emp_uiid=employee_id)

        serializer = PreviousMembershipSerializer(data=request.data)

        if serializer.is_valid():
            membership = serializer.save(employee=employee)
            # print(serializer.data)
            # membership = membership.name
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            data = {
                'errors': serializer.errors
            }
            # print(serializer.errors)
            return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def deleteMembership(request, employee_id, pk):
    if request.method == 'DELETE':
        membership = get_object_or_404(
            ProfessionalMembership, pk=pk, employee__emp_uiid=employee_id)
        # key = education.id
        membership.delete()
        return JsonResponse({'data': 'record deleted'})


@api_view(['POST', 'GET'])
def add_emploment(request, employee_id):

    if request.method == 'GET':
        try:
            employment = PreviousEployment.objects.filter(
                employee__emp_uiid=employee_id)
            serializer = PreviousEploymentSerializer(employment, many=True)
            return Response(serializer.data)

        except:
            return Response(status=404)

    if request.method == 'POST':
        employee = Employee.objects.get(emp_uiid=employee_id)
        serializer = PreviousEploymentSerializer(data=request.data)

        if serializer.is_valid():
            employment = serializer.save(employee=employee)
            # print(serializer.data)
            # employment = str(employment)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            data = {
                'errors': serializer.errors
            }
            print(serializer.errors)
            return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def deleteEmployment(request, employee_id, pk):
    if request.method == 'DELETE':
        emploment = get_object_or_404(
            PreviousEployment, pk=pk, employee__emp_uiid=employee_id)
        # key = education.id
        emploment.delete()
        return JsonResponse({'data': 'record deleted'})


@group_required('HR')
@api_view(['POST', 'GET'])
def filename(request):
    if request.method == 'GET':
        filenames = File.objects.values(
            'name', 'pk').annotate(count=Count('filenames'))

        return Response({'data': filenames}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        name = File.objects.create(name=request.POST.get('filename'))

        return Response(data=name.name, status=status.HTTP_201_CREATED)


# DOCUMENT MANAGEMENT
# @group_required('HR')
@api_view(['GET', 'POST'])
def add_document(request, employee_id):
    if request.method == 'GET':
        employee = get_object_or_404(Employee, employee_id=employee_id)
        cv = employee.applicant_cv_exists
        document = Documente.objects.filter(employee=employee)
        serializer = DocumentSerializer(document, many=True)

        print(cv)

        data = {
            'document': serializer.data,
            'cv': cv,
            # 'letter':letter

        }
        return Response(data, status=200)

    if request.method == 'POST':
        employee = get_object_or_404(Employee, employee_id=employee_id)

        file = request.FILES.get('document')
        description = request.data.get('description')
        date = request.data.get('date')
        filename = request.data.get('document_id')

        # print(file,description,date,filename)

        document = Documente.objects.create(
            employee=employee, description=description, date=date, file=file, filename_id=filename)

        serializer = DocumentSerializer(document)

        return Response(serializer.data)


# EMPLOYEE EXIT ENDPOINT
@api_view(['POST', 'GET', 'DELETE'])
@group_required('HR')
def exit_employee(request, employee_id):

    if request.method == 'GET':
        try:
            # employee = get_object_or_404(Employee, employee_id=employee_id)
            # print('employee ')
            employee = get_object_or_404(
                EmployeeExit, employee__employee_id=employee_id)
            serializer = EmployeeExitSerializer(instance=employee)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            employee = get_object_or_404(Employee, employee_id=employee_id)
            data = {
                'employee_name': employee.full_name,
                'position': employee.position,
                'employement_length': employee.employement_length,
                'status': employee.status,
            }

            return Response(data=data, status=status.HTTP_200_OK)

    if request.method == 'POST':

        employee = get_object_or_404(Employee, employee_id=employee_id)
        data = request.data
        date_departure = data.get('date_departure')
        exit_status = data.get('status')

        data._mutable = True
        del data['csrfmiddlewaretoken']
        data.update({'hr_representative': request.user.get_full_name()})
        data._mutable = False

        # UPDATE IF IT EXISTS
        if EmployeeExit.objects.filter(employee=employee).exists():
            # print('YES')
            old_task_id = employee.employee_exit.data.get('task_id')
            
            employee.employee_exit.data = data
            employee.employee_exit.save(update_fields=['data'])

            # CELERY TASK
            date = datetime.strptime(date_departure, '%Y-%m-%d')

            print('old_task_id ', old_task_id)

            tasks_id = tasks.employee_exiting.apply_async(eta=date, args=(
                employee_id, date_departure, exit_status,old_task_id),countdown=5)

            # tasks_id = tasks.employee_exiting.apply_async(eta=date, args=(
            #     employee_id, date_departure, exit_status, old_task_id), countdown=10)

      

            # print('new_tasks_id', tasks_id)
# 
            employee.employee_exit.data._mutable = True
            employee.employee_exit.data.update({'task_id': tasks_id.id})
            employee.employee_exit.save(update_fields=['data'])
            employee.employee_exit.data._mutable = True

        else:
            # CREATE IF IT DOES NOT EXIST
            EmployeeExit.objects.create(employee=employee, data=data)
            date = datetime.strptime(date_departure, '%Y-%m-%d')

            # transaction.on_commit(tasks.employee_exiting.apply_async(
            #     eta=date).delay(employee_id, date_departure, exit_status))

            tasks_id = tasks.employee_exiting.apply_async(eta=date, args=(
                employee_id, date_departure, exit_status))

        return Response(data=data, status=status.HTTP_202_ACCEPTED)

    if request.method == 'DELETE':
        employee = get_object_or_404(
            EmployeeExit, employee__employee_id=employee_id)
        employee.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@group_required('HR')
def delate_document(request, employee_id, pk):
    document = get_object_or_404(
        Documente, employee__employee_id=employee_id, pk=pk)
    document.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


# REQUEST FOR PERSONAL DATA CHANGES
@api_view(['GET', 'POST'])
def request_changes(request, employee_id):

    ''' REQUEST FOR PERSONAL DATA CHANGES '''

    if request.method == 'GET':
        employee = get_list_or_404(
            RequestChange, employee__emp_uiid=employee_id)
        serializer = RequestChangeSerilizer(instance=employee, many=True)

        # print(serializer.data)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        employee = get_object_or_404(Employee, emp_uiid=employee_id)
        serializer = RequestChangeSerilizer(data=request.data)

        if serializer.is_valid():

            employee = serializer.save(employee=employee)

            request_change = employee.employee
            request_change.request_change = True
            request_change.save()

            subject = 'Data Change Request from %s' % employee.employee.full_name
            link = '<p>please <a href="http://192.168.1.18/employee">Click Here</a> to approve or revoke the request. </p>'
            message = request.data.get('text')
            message = f" {message} {link}"

            department = employee.employee.position

            # SEND CHANGE REQUEST TO HR
            # tasks.send_email_request_data_change.delay(subject, message)

            tasks.send_email_request_data_change.apply_async(args=(subject, message,HR_EMAIL),countdown=3)


            print(subject, message)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        if serializer.errors:
            print(serializer.errors)

            return Response(data=serializer.errors, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@group_required('HR')
# @csrf_exempt
@api_view(['GET', 'POST'])

def grant_request(request, request_id=None):
    ''' HR GET REQUEST AND VERIFY OR REVOKE EMPLOYEE DATA CHANGE POST''' 

    if request.method == 'GET':
        employee = get_list_or_404(RequestChange, status='pending')
        serializer = RequestChangeSerilizer(instance=employee, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST' and request_id:
        employee_request = get_object_or_404(RequestChange, id=request_id)

        status_text = request.data.get('status')
        print('status_text ', status_text)
        employee_request.status = status_text
        employee_request.save()

        # update employee request status in main table
        request_change = employee_request.employee
        request_change.request_change = False
        request_change.save()

        data = {
            'status': employee_request.status,
            'request_change': request_change.request_change

        }
        email  =  employee_request.employee.email


        # SEND INFO TO EMPLOYEE IF HR APPROVE OR REVOKE
        
       
   

        subject = 'Request For Data Change'
        email  =  employee_request.employee.email   
        change_status= employee_request.status
        heading ='Dear %s' % employee_request.employee.full_name
        emp_uiid = employee_request.employee.emp_uiid

        link = f'<p>please <a href="http://192.168.1.18/update-employee/{emp_uiid}">Click Here</a> to update your records . </p>' 
        approve_not_approved = link if change_status =='approved' else 'NB: please visit the HR depratement for clarity'

        message = f'<p>{heading}</p> Your request for your infomation change on royaldesk have been <b>{employee_request.status}</b> {approve_not_approved}'


        tasks.send_email_request_data_change.apply_async(args=(subject, message,email),countdown=3)

        # tasks.send_email_request_data_change.delay(subject, message,email)
        return Response(data=data, status=status.HTTP_200_OK)


# APPLY FOR LEAVE FORM ONLY

@api_view(['POST', 'GET'])
def apply_leave(request, employee_id):

    employee = get_object_or_404(Employee.activeemployees, Q(
        employee_id=employee_id) | Q(email=employee_id))

    leave_policies = list(LeavePolicy.objects.values('pk', 'name', 'days'))

    last_on_leave = employee.leave_employees.values(
        'start__year', 'start__month').filter(start__isnull=False).last()

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
            'last_on_leave': last_on_leave
        }

        return Response(leave_data)

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
        leave_days = str(leave.leavedays)
        leave_id = str(leave.id)

        # SEND EMAIL TO HOD AND HR
        # tasks.apply_for_leave_email(
        #     employee, start, end, leave_days, policy, department_email)

        # SEND REMIBER EMAIL IF NOT APPROVED WITHIN LEAVE_REMINDER_HOURS
        # LEAVE_REMINDER_HOURS
        hours_latter = datetime.now() + timedelta(minutes=10)

        tasks.applied_leave_reminder.apply_async(eta=hours_latter, args=(
            employee, start, end, leave_days, policy, leave_id,department_email
        ))

        # print('leave_id',leave_id)

        return Response({'data': str(leave_data), 'on_leave': on_leave})


# DISPLAY LEAVE BASED ON USER RIGHTS
@api_view(['GET'])
def leaves(request, employee_id):
    """
    DISPLAY USER LEAVE
    """
    employee = get_object_or_404(
        Employee.activeemployees, employee_id=employee_id)

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
    employee_leave = Leave.objects.select_related(
        'employee').filter(employee__employee_id=employee)
    # employee_leave.get(pk=leave_id)
    leave = get_object_or_404(employee_leave, pk=leave_id)
    # policy = leave.policy.name
    leave_year = leave.end.strftime('%Y')

    last_date_on_leave = employee_leave.values_list('resuming_date', flat=True).filter(
        employee__employee_id=employee, hr_manager=True).last()

    leave_per_year = employee_leave.filter(policy__name=leave.policy.name, end__year=leave_year).values(
        'policy__name', 'end__year').annotate(total_spent=Sum('leavedays'),
                                              out_standing=F(
            'policy__days') - F('total_spent')).order_by('-start__year')

    out_standing_days = leave_per_year.filter(
        policy__has_days=True).aggregate(out_standing_days=Sum('out_standing'))

    # available_days  = leavedays - sum of previous + current
    prev_issue = leave_per_year.filter(id__lt=leave_id).exclude(
        id=leave_id).order_by('-id').aggregate(prev_issue=Sum('leavedays'))

    # prev_issue = leave_per_year.exclude(id=leave_id).order_by('-id').aggregate(prev_issue=Sum('leavedays'))

    policy_days = leave.policy.days
    prev_issue = prev_issue.get(
        'prev_issue') if prev_issue.get('prev_issue') else 0
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
        'available_days': available_days if leave.policy.has_days else 'N/A'
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

# LOAD ANVIZ DEPARTMENT FROM FILE


@api_view(['GET'])
def anviz_department(request):
    anviz_department = partials.anviz_department()
    return Response(anviz_department, status=status.HTTP_200_OK)
