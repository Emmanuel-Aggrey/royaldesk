# from django.shortcuts import render
import json
from datetime import datetime

from decouple import config
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import Group
from helpdesk.models import User
from hrms.models import Department, Designation, Employee
from HRMSPROJECT.custome_decorators import group_required

from . import tasks
from .models import Applicant
from .serializers import AcceptanceSerializer, ApplicantSerializer,ApplicantOfferLetterSerializer,FileUploadSerializer,FileUploadDisplaySerializer

# Create your views here.


@group_required('HR')
def applicantView(request):

    return render(request, 'applicant/applicants.html')


@group_required('HR')
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
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():

            applicant = serializer.save()

            applicantid = "<b>{}</b>".format(applicant.applicant_id)
            candidatename = applicant.full_name
            job = applicant.position
            salary = '<b>{}</b>'.format(applicant.applicant_salary)
            applicant_email = applicant.email
            hrname = '<br>{}.<br>'.format(request.user.full_name)
            hrposition = '{} {}.<br>'.format(
                request.user.department.name, request.user.designation.name)
            hremail = '{}.<br>'.format(request.user.department.email)
            company = config('COMPANY_NAME', default='Rock City Hotel')

            link = config('SITE_ADDRESS',
                          default='http://192.168.1.18/applicant')
            link = "<a href={}/applicant>Link</a>".format(link)

            subject = f'Your interview with {company} for {job}'

            
            note = '<p>Please note: Do not reply to this email. This email is sent from an unattended mailbox. Replies will not be read</p>'

            if applicant_email:
                message = applicant.comment.format(candidatename=candidatename, company=company, link=link,
                                                   applicantid=applicantid, hrname=hrname, hrposition=hrposition, hremail=hremail)

            message = f'{message} {note}'

            tasks.send_applicant_email.delay(
                applicant_email, subject, message)
            # print(applicant_id, name, email, department,designation,resuming_date)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

default_password = config('DEFAULT_PASSWORD', default='changeme')

# FOR APPLCANTS VIEW
@api_view(['GET', 'POST'])
def update_applicant(request, applicant_id):
    applicant = get_object_or_404(Applicant, Q(
        applicant_id=applicant_id) | Q(phone=applicant_id))

    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)

        # print(serializer.data)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ApplicantSerializer(applicant, data=request.data)
        if serializer.is_valid():
            applicant = serializer.save()

            applicantid = "<b>{}</b>".format(applicant.applicant_id)
            candidatename = applicant.full_name
            job = applicant.position
            salary = '<b>{}</b>'.format(applicant.applicant_salary)
            startdate = "<b>{}</b>".format(applicant.resuming_date)
            applicant_email = applicant.email
            hrname = '<br>{}.<br>'.format(request.user.full_name)
            hrposition = '{} {}.<br>'.format(
                request.user.department.name, request.user.designation.name)
            hremail = '{}.<br>'.format(request.user.department.email)

            link = config('SITE_ADDRESS',
                          default='http://192.168.1.18/applicant')
            link = "<a href={}/applicant>Link</a>".format(link)
            company = config('COMPANY_NAME', default='Rock City Hotel')

            note = '<p>Please note: Do not reply to this email. This email is sent from an unattended mailbox. Replies will not be read</p>'

            # designation = applicant.designation.name
            # department = applicant.department.name
            subject = f'Your interview with {company} for {job}'

            print(applicant.status)

            if applicant.status == 'selected' and applicant.email:

                message = applicant.comment.format(applicantid=applicantid, candidatename=candidatename, job=job,
                                                   salary=salary, startdate=startdate, hrname=hrname,
                                                   hremail=hremail, hrposition=hrposition, link=link, company=company)

                
                message = f'{message} {note}'
                tasks.send_applicant_email.delay(
                    applicant_email, subject, message)

            user_exists = User.objects.filter(
                username=applicant.applicant_id).exists()

            if applicant.status == 'selected' and not user_exists:
                # print('user_exists creating user', user_exists)

                # print('selected application')
                user = User(username=applicant.applicant_id, first_name=applicant.first_name,
                            last_name=applicant.last_name, email=applicant.email, department=applicant.department,
                            designation=applicant.designation, is_applicant=True)

                user.set_password(default_password)
                user.save()

                group = Group.objects.prefetch_related().filter(
                    name=applicant.department.shortname).last()
                if user and group:
                    user.is_staff = True
                    user.save()
                    user.groups.add(group)

            if applicant.status == 'not selected' and applicant.email:

                link = '<a href={}>here</a>'.format(
                    'https://www.linkedin.com/company/rock-city-hotel-ltd/jobs/')

                message = applicant.comment.format(candidatename=candidatename, job=job, company=company,
                                                   hrname=hrname,
                                                   hremail=hremail, hrposition=hrposition, link=link)
                message = f'{message} {note}'
                tasks.send_applicant_email.delay(
                    applicant_email, subject, message)

            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def upload_offer_letter(request,applicant_id):
    applicant = get_object_or_404(Applicant,applicant_id=applicant_id)

    if request.method == 'GET':
        for files in applicant.offer_letter:
            
        
            return Response(files)

    if request.method == 'POST':

        offer_letter = request.FILES.getlist('offer_letter')
        offer_letters = []
        for files in offer_letter:
            applicant.offer_letter = files
            applicant.save()
            offer_letters.append(files)


        return Response({'offer_letters':f'{offer_letters}'})



class FileUploadView(generics.ListCreateAPIView):
    # from rest_framework.permissions import AllowAny
    # permission_classes = [AllowAny]
    # serializer_class = FileUploadDisplaySerializer
    def post(self, request, applicant_id,format=None): 
        queryset = get_object_or_404(Applicant,applicant_id=applicant_id)
        serializer = FileUploadSerializer(instance=queryset,data=request.data)
        if serializer.is_valid():    #validate the serialized data to make sure its valid       
            qs = serializer.save()                     
            message = {'detail':qs, 'status':True}
            return Response(message, status=status.HTTP_201_CREATED)
        else: #if the serialzed data is not valid, return erro response
            data = {"detail":serializer.errors, 'status':False}            
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        return Applicant.objects.all()

class ApplicantOfferLetterSerializers(APIView):
    

    def post(self, request, applicant_id,*args, **kwargs):
        queryset = get_object_or_404(Applicant,applicant_id=applicant_id)
        serializer = ApplicantOfferLetterSerializer(queryset,data=request.data)
        if serializer.is_valid():
            files = serializer.validated_data['offer_letter']
            for files in files:
                applicant
            # serializer.save()
            # Do something with the files
            print(files)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OFFER LETTER  DJANGO TEMPLATE
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

# OFFER LETTER   API


@api_view(['GET'])
def acceptance_api_view(request, applicant_id):
    applicant = get_object_or_404(Applicant, Q(
        applicant_id=applicant_id) | Q(phone=applicant_id))

    serializer = AcceptanceSerializer(applicant)

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def message_to_applicant(request):

    if request.method == 'GET':

        with open('applicant/applicant_message.json', 'r') as openfile:

            return Response(json.load(openfile))

    if request.method == 'POST':
        data = request.data
        comment = {
            "selected": data.get('selected', 'not selected'),
            "not_selected": data.get('not_selected', 'not selected'),
            "in_review": data.get('in_review', 'in review'),

        }
        message = {}
        with open("applicant/applicant_message.json", "w") as outfile:
            message = json.dump(comment, outfile)

            return Response(comment)

    else:
        return Response(status.HTTP_400_BAD_REQUEST)
