
# from demoapp.models import Widget

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail, send_mass_mail
from hrms.models import Leave
from datetime import datetime, timedelta
import pandas as pd


@shared_task
def apply_for_leave_email(employee, start, end, diff, policy, handle_over_to, department_email):

    email_from = settings.EMAIL_HOST_USER

    subject = 'New Leave For {}'.format(employee)
    subject_ = subject.upper()
    html_content = '{} Have Applied  For {} from {} to {} making {} day(s) handled over to {}, Please <a href="http://192.168.43.212:8000/apply-leave/">Click Here</a> to approve Thank you <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.43.212:8000/"> ROYALDESK </a> RCH</b> </footer>'.format(
        employee, policy, start, end, diff, handle_over_to)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, ['aggrey.en@live.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def employee_on_leave():
    tomorrow = datetime.now().date() + timedelta(days=1)
    leave = Leave.objects.filter(end=tomorrow).select_related('employee')
    data = leave.values('employee__first_name', 'employee__last_name', 'employee__department__name',
                 'employee__designation__name', 'policy__name', 'start', 'end', 'leavedays', 'employee__emergency_phone')
    df = pd.DataFrame(data)

    df.to_csv('employee_on_leave.csv')


