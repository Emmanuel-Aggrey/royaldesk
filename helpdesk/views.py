from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from hrms.models import Department, Designation
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import User,Helpdesk, Issue,Ticket_Comment
from .serializers import HelpdeskSerializer
from . import tasks
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Create your views here.





@api_view(['GET'])

def departments_issue(request):
    issue = list(Issue.objects.values('pk','issue_name','department'))
    department = list(Department.objects.values('pk','name').exclude(for_management=True))
    data = {
        'departments':department,
        'issues':issue
    }


    return Response(data)

@login_required
@api_view(['GET'])
def helpdesk(request,pk):

    tickets = Helpdesk.objects.select_related('user')
    date_filter = request.data
    date_from = request.GET.get('date_from')

    date_to = request.GET.get('date_to')
    
    if request.user.is_staff:
        tickets = tickets.all()
    
    
    elif request.user.is_head:
        tickets = tickets.filter(Q(department=request.user.department)|Q(user__pk=pk))
        print('head',request.user.department,request.user.is_head)
   

    else:
        tickets = tickets.filter(Q(user__pk=pk)| Q(handle_over_to_id=pk))
        print('head',request.user.department,request.user.is_head)

     
   
    serializer = HelpdeskSerializer(tickets, many=True)
    return Response({'data': serializer.data})




@login_required
@api_view(['GET'])
def filter_helpdesk(request,pk):
    # print('user',request.user,'departemnt',request.user.department,'is_head',request.user.is_head,'is admin',request.user.is_staff)

    tickets = Helpdesk.objects.select_related('user').exclude(user__for_management=True)
    date_filter = request.data
    date_from = request.GET.get('date_from')

    date_to = request.GET.get('date_to')
    
    if request.user.is_staff:
        tickets = tickets.filter(date__range=[date_from, date_to])       
        # print(tickets)

    elif request.user.is_head:
        tickets = tickets.filter(Q(department=request.user.department)|Q(user__pk=pk),date__range=[date_from, date_to])
        # print(tickets.query)


    else:
        tickets = tickets.filter(Q(user__pk=pk)| Q(handle_over_to_id=pk),date__range=[date_from, date_to])
        # print(request.data)

   
    serializer = HelpdeskSerializer(tickets, many=True)
    return Response({'data': serializer.data})

@login_required
@api_view(['POST'])
def send_report(request):

    data = request.data

    image = request.FILES.get('image')

    report = {
        'user_id': request.user.pk,
        'image':image,
        'department_id':data.get('department'),
        'issue_id':data.get('issue'),
        'priority':data.get('priority'),
        'subject':data.get('subject'),

    }


    request_user= Helpdesk.objects.create(**report)


    email_from = settings.EMAIL_HOST_USER

    # USER SENDING REQUEST
    user_name = request_user.user.full_name
    user_email = request_user.user.email
    user_department = request_user.department.name
    description = report.get('subject', None)
    priority = report.get('priority', None).upper()
    ticket_number = request_user.ticket_number
    department_email = request_user.department.email



   
    tasks.helpdesk_ticket_create(user_name,ticket_number,user_email,\
        user_department,description,priority,[department_email])    


    return Response(status=status.HTTP_201_CREATED)



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

# CHECK TICKET STATUS
def bool_value(user,status):
    if status =='on':
        return 'resolved' 
    elif status ==None and user:
        return 'assiend' #if  user !='4' else 'pending' 
    else:
        return 'pending'
        




# def bool_value(value):
#     return True if value else False
@login_required
@api_view(['GET','POST'])
def get_issue_data(request,pk):
    # desk = Helpdesk.objects.get(pk=pk)
    help_desk =  get_object_or_404(Helpdesk,pk=pk)



    if request.method == 'GET':
        
        employees = list(User.activeusers.filter(department=help_desk.department).values('pk','first_name','last_name','department__name'))
        
        data = {
        'image':help_desk.image_exists,
        'department':help_desk.department.name,
        'department_pk':help_desk.department.pk,
        'issue':help_desk.issue.issue_name,
        'issue_pk':help_desk.issue.pk,
        'subject':help_desk.subject,
        'priority':help_desk.priority,
        'status':help_desk.status,
        'handle_over_to':help_desk.handle_over_to.full_name,  
        'handle_over_to_pk':help_desk.handle_over_to.pk,  
        'ticket_number':help_desk.ticket_number,
        'employees':employees,
        'comments':help_desk.comments.count(),
        'hod_user':request.user.is_head,
        'handle_overto_user' : True if help_desk.handle_over_to ==request.user else False,

        }
        return Response(data)

    if request.method == 'POST':
        data = request.data
        old_file = help_desk.image
        new_file = request.FILES.get('image')
        status_= bool_value(data.get('assiend_to'),data.get('status'))
        help_desk.department_id= data.get('department')
        help_desk.issue_id = data.get('issue')
        help_desk.status=status_
        help_desk.priority = data.get('priority')
        help_desk.subject = data.get('subject')
        help_desk.comment = data.get('comment')
        help_desk.image = file_exists(old_file,new_file)
        help_desk.handle_over_to_id  = data.get('assiend_to')


        help_desk.save()

        
        if help_desk.status == 'resolved':
            department_email = help_desk.department.email

            # print(department_email)
         
            tasks.helpdesk_ticket_resolved(help_desk.user.full_name,help_desk.ticket_number,help_desk.subject,help_desk.user.email,help_desk.department,[department_email])


        data = {
            'status':help_desk.status,
        }
        return Response(data,status=status.HTTP_201_CREATED)

@login_required
@api_view(['GET','POST'])
def comment(request,pk):
    
    if request.method == 'GET':
        comments = Ticket_Comment.objects.select_related('ticket').filter(ticket_id=pk).values('comment','user')
        # print(comments.query)
        return Response(comments)
    
    
    if request.method == 'POST':

        data = request.data

        comment ={
            'ticket_id':data.get('ticket_id'),
            'comment':data.get('comment'),
            'user':request.user.id,
        }


        # print('comment ',comment)

        Ticket_Comment.objects.create(**comment)

        return Response(status=201)


    
