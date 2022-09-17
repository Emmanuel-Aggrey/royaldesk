
# from demoapp.models import Widget

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail, send_mass_mail


@shared_task
def send_applicant_email(applicant_name, applicant_email, designation, department,applicant_id):

    email_from = settings.EMAIL_HOST_USER

    # print(applicant_name,applicant_email,designation,start_date,status)

    subject = 'Dear  {}'.format(applicant_name)
    subject_ = subject.upper()
    html_content = 'Your Applicantion For {} in {} Department At Rock City Hotel Kuahu Nquatia have been updated Please <a href="https://a524-154-160-6-247.eu.ngrok.io/applicant/">Click Here</a> to check the progress of the application status regularly. <br> Your Unique Identifier is {} Thank you <br><hr> <br> <footer><b>POWERD BY <a href="https://a524-154-160-6-247.eu.ngrok.io:8000/"> ROYALDESK </a> RCH</b> </footer>'.format(
        designation, department,applicant_id)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, [applicant_email, ])
    msg.attach_alternative(html_content, "text/html")

    msg.send()


@shared_task
def send_applicant_email_selected(applicant_name, applicant_email, designation, department,applicant_id):

    email_from = settings.EMAIL_HOST_USER

    subject = 'Dear  {}'.format(applicant_name)
    subject_ = subject.upper()
    html_content = 'Your Applicantion For {} in {} Department At Rock City Hotel Kuahu Nquatia have been selected Please <a href="https://a524-154-160-6-247.eu.ngrok.io/applicant/">Click Here</a> to download your offer letter <br> your Unique Identifier is <b>{}</b> in case you lost it Thank you <br><hr> <br> <footer><b>POWERD BY <a href="https://a524-154-160-6-247.eu.ngrok.io:8000/"> ROYALDESK </a> RCH</b> </footer>'.format(
        designation, department,applicant_id)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, [applicant_email, ])
    msg.attach_alternative(html_content, "text/html")

    msg.send()


# @shared_task
# def send_mail_reminder():
#     print('send_mail_reminder')
    # print(x,y)
    # return x+y
