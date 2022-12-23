
# from demoapp.models import Widget

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail, send_mass_mail


email_from = settings.DEFAULT_FROM_EMAIL

# @shared_task
# def send_applicant_email(applicant_name, applicant_email, designation, department,applicant_id):

#     # email_from = settings.EMAIL_HOST_USER

#     # print(applicant_name,applicant_email,designation,start_date,status)

#     subject = 'Dear  {}'.format(applicant_name)
#     subject_ = subject.upper()
#     html_content = 'Your Applicantion For {} in {} Department At Rock City Hotel Kuahu Nquatia have been updated Please <a href="http://192.168.1.18/applicant/">Click Here</a> to check the progress of the application status regularly. <br> Your Unique Identifier is {} Thank you <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH</b> </footer>'.format(
#         designation, department,applicant_id)

#     msg = EmailMultiAlternatives(
#         subject_, html_content, email_from, [applicant_email, ])
#     msg.attach_alternative(html_content, "text/html")

#     msg.send()


@shared_task
def send_applicant_email(applicant_email, subject, message):

    # email_from = settings.EMAIL_HOST_USER

    # subject: 'Your interview with Rock City Hotel for {job}'

    # subject = 'Dear  {}'.format(applicant_name)
    # subject_ = subject.upper()
    html_content = message
    # html_content = 'Congratulations, Your Applicantion For {} in {} Department At Rock City Hotel Kuahu Nquatia have been selected Please <a href="http://192.168.1.18/applicant/">Click Here</a> to download your offer letter <br> your Unique Identifier is <b>{}</b> in case you lost it Thank you <br><hr> <br> <p>Best Regards,</p><p>The Human Resource Department.</p> <br> <footer><b>POWERD BY <a href="https://192.168.1.18/"> ROYALDESK </a> RCH</b> </footer>'.format(
    #     designation, department,applicant_id)

    msg = EmailMultiAlternatives(
        subject, html_content, email_from, [applicant_email, ])
    msg.attach_alternative(html_content, "text/html")

    msg.send()


# @shared_task
# def send_mail_reminder():
#     print('send_mail_reminder')
    # print(x,y)
    # return x+y
