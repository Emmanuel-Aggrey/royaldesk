
# from demoapp.models import Widget

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from .models import Helpdesk
from django.core.mail import EmailMultiAlternatives



#NB REPLACING ALL DEPARTMENT EMAILS WITH PERSONALL ONE FOR NOW 

email_from = settings.DEFAULT_FROM_EMAIL


@shared_task
def helpdesk_ticket_create(user_name, ticket_number, user_email, department, description, priority, department_email=[]):

    # email_from = settings.EMAIL_HOST_USER
    # email_from = settings.DEFAULT_FROM_EMAIL

    subject = 'Dear {}'.format(user_name)
    subject_ = subject.upper()
    html_content = 'Your Request With Ticket Number {} Have Been Created, <a href="http://192.168.1.18/helpdesk/">Click Here</a> to view the status <br> <p>Best Regards,</p>The Royal Desk Team.</p> <hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        ticket_number)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, [user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # print('subject',subject_)

    subject1 = 'New Ticket From {} in {} Department'.format(
        user_name, department)
    subject_1 = subject1
    html_content_1 = '{} PRIORITY: {} <a href="http://192.168.1.18/helpdesk/">Click Here</a> to view the status <br><p>Best Regards,</p>The Royal Desk Team.</p><hr>  <br> <footer> <b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        description, priority)
    # html_content = 'Your Request With Ticket Number {} Have Been Created, <a href="http://192.168.1.119:8000/helpdesk/">Click Here</a> to view the status'.format(ticket_number)

    msg = EmailMultiAlternatives(
        subject_1, html_content_1, email_from, department_email)  #department_email is a list
    msg.attach_alternative(html_content_1, "text/html")
    msg.send()

    # print('department_email', department_email)


@shared_task
def helpdesk_ticket_resolved(user_name,ticket_number,description,user_email,department,department_email=[]):
    # email_from = settings.EMAIL_HOST_USER

    subject = 'Dear {}'.format(user_name)
    subject_ = subject.upper()
    html_content = 'Your Request With Ticket Number {} Have Been Resolved Thank You <br><p>Best Regards,</p>The Royal Desk Team.</p><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        ticket_number)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, [user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




    subject1 = 'Ticket Number {} Has Been Resolved'.format(ticket_number)
    subject_1 = subject1
    html_content_1 = '{} From {} In {}  <br><p>Best Regards,</p>The Royal Desk Team.</p><hr> <br> <footer> <b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH</b> </footer>'.format(
        description,user_name,department)
    # html_content = 'Your Request With Ticket Number {} Have Been Created, <a href="http://192.168.1.119:8000/helpdesk/">Click Here</a> to view the status'.format(ticket_number)

    msg = EmailMultiAlternatives(
        subject_1, html_content_1, email_from, department_email) #department_email is a list
    msg.attach_alternative(html_content_1, "text/html")
    msg.send()
