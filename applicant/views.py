# from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from hrms.models import Department, Designation
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Applicant
from rest_framework import generics
from .serializers import ApplicantSerializer, AcceptanceSerializer
from datetime import datetime
from .import tasks
from hrms.models import Employee
# Create your views here.


def date_value(value):
    return value if value else None


@api_view(['GET', 'POST'])
def applicant(request):
    employees = Employee.objects.values_list('pk', flat=True)

    # print(Applicant.objects.filter(applicant__in=employees))

    applicant = Applicant.objects.exclude(applicant__in=employees)

    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant, many=True)
        # print(serializer.data)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data

        file = request.FILES.get('file')
        first_name = data.get('fname')
        last_name = data.get('lname')
        year = datetime.now().year

        applicant_id = f'{first_name[0]}{last_name}-{year}'.upper()

        full_name = '{} {}'.format(first_name, last_name)

        applicant_date = {
            'applicant_id': applicant_id,
            'first_name': data.get('fname'),
            'last_name': data.get('lname'),
            'other_name': data.get('oname'),
            'department_id': data.get('department'),
            'designation_id': data.get('designation'),
            'comment': data.get('comment'),
            'cv': file,
            'phone': data.get('phone'),
            'email': data.get('email'),
            'status': data.get('status'),
            'resuming_date': date_value(data.get('date')),
            'address': data.get('address'),
            'salary': data.get('salary'),
        }

        print(data.get('address'), data.get('salary'))


        applicant = applicant.create(**applicant_date)

        applicant_id = applicant.applicant_id
        name = applicant.full_name
        email = applicant.email
        designation = applicant.designation.name
        department = applicant.department.name
        resuming_date = applicant.resuming_date

        if email:
            tasks.send_applicant_email(
                name, email, designation, department, applicant_id)

        return Response(full_name, status=status.HTTP_201_CREATED)


def file_exists(old_file, new_file):
    if old_file and new_file:
        return new_file
    elif new_file and old_file:
        return new_file
    elif old_file and not new_file:
        return old_file
    elif new_file and not old_file:
        return new_file
    else:
        return


@api_view(['GET', 'POST'])
def update_applicant(request, applicant_id):
    applicant = get_object_or_404(Applicant, Q(
        applicant_id=applicant_id) | Q(phone=applicant_id))

    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)

        # print(serializer.data)
        return Response(serializer.data)

    if request.method == 'POST':

        data = request.data

        old_file = applicant.cv
        new_file = request.FILES.get('file')


        print(data.get('address'), data.get('salary'))


        # print(file_exists(old_file, new_file))

        if data.get('date'):
            applicant.first_name = data.get('fname')
            applicant.last_name = data.get('lname')
            applicant.email = data.get('email')
            applicant.phone = data.get('phone')
            applicant.other_name = data.get('oname')
            applicant.department_id = data.get('department')
            applicant.designation_id = data.get('designation')
            applicant.cv = file_exists(old_file, new_file)
            applicant.comment = data.get('comment')
            applicant.status = data.get('status')
            applicant.resuming_date = data.get('date')
            applicant.salary = data.get('salary')
            applicant.address = data.get('address')
            applicant.save()

            if applicant.status == 'selected' and applicant.email and applicant.resuming_date:
                tasks.send_applicant_email_selected(applicant.full_name, applicant.email, applicant.designation.name,
                                                    applicant.department.name, applicant.applicant_id)

        else:
            applicant.first_name = data.get('fname')
            applicant.last_name = data.get('lname')
            applicant.email = data.get('email')
            applicant.phone = data.get('phone')
            applicant.other_name = data.get('oname')
            applicant.department_id = data.get('department')
            applicant.designation_id = data.get('designation')
            applicant.cv = file_exists(old_file, new_file)
            applicant.comment = data.get('comment')
            applicant.status = data.get('status')
            applicant.salary = data.get('salary')
            applicant.address = data.get('address')
            applicant.save()

            if applicant.status == 'selected' and applicant.email:
                tasks.send_applicant_email_selected(applicant.full_name, applicant.email, applicant.designation.name,
                                                    applicant.department.name)

        return Response(applicant.full_name)

# @api_view(['GET'])


def acceptance_view(request, applicant_id):
    applicant = get_object_or_404(Applicant, Q(
        applicant_id=applicant_id) | Q(phone=applicant_id))

    # serializer = AcceptanceSerializer(applicant)

    # print(serializer.data)
    context = {
        'applicant': applicant
    }
    # return Response(serializer.data)
    return render(request, 'applicant/offerl_letter.html', context)


@api_view(['GET'])
def acceptance_api_view(request, applicant_id):
    applicant = get_object_or_404(Applicant, Q(
        applicant_id=applicant_id) | Q(phone=applicant_id))

    serializer = AcceptanceSerializer(applicant)

    return Response(serializer.data)
