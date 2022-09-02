
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
    html_content = '{} Have Applied  For {} from {} to {} making {} day(s) handled over to {}, Please <a href="http://192.168.43.212:8000/apply-leave/">Click Here</a> to approve Thank you <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.43.212:8000/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        employee, policy, start, end, diff, handle_over_to)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, ['aggrey.en@live.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_email_new_helpdesk_employee(employee,email,password):

    email_from = settings.EMAIL_HOST_USER

    subject = 'Dear {}'.format(employee)
    subject_ = subject.upper()
    html_content = 'Welcome to Rock City Help Desk, Your Uername is <b>{}</b> ,And password is <b>{}</b>, Please <a href="http://192.168.43.212:8000/">Click Here</a> to login to use Help Desk. <p>you will be redirected to change the default password to your own password </p>  Thank you.  <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.43.212:8000/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        employee, password)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, [email])
    msg.attach_alternative(html_content, "text/html")

    print(html_content)
    # msg.send()


@shared_task
def employee_on_leave():
    tomorrow = datetime.now().date() + timedelta(days=1)
    leave = Leave.objects.select_related('employee').filter(end=tomorrow,from_leave=False)
    data = leave.values('employee__first_name', 'employee__last_name', 'employee__department__name','employee__designation__name','employee__department__email')

    department_email = [data[i]['employee__department__email'] for i in range(len(data))]

    department_email = list(set(department_email))

    print(department_email)




    # create an html table with data
    df = pd.DataFrame(data)
    df.drop(['employee__department__email'], axis = 1, inplace = True) 

    df.columns = ['First Name', 'Last Name', 'Department', 'Designation']
    html_table = df.to_html(index=False)
    html_table = html_table.replace('border="1"', 'border="1"')
    html_table = html_table.replace('style="border: 1px solid;"', 'style="align-items: center;"')





    # df.to_html(classes='table table-striped text-center', justify='center')

    # print(html_table)




      




    email_from = settings.EMAIL_HOST_USER
    tomorrow = tomorrow.strftime("%B %d, %Y")


    subject = 'Employees On Leave'
    subject_ = subject.upper()
    html_content = 'List of employees whom are to return from Leave tomorrow  On The {}  <br> <br> {} <br> <b>Thank you</b>  <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.43.212:8000/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        tomorrow,html_table)

    # print(html_content)
    

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, ['aggrey.en@live.com'])
    msg.attach_alternative(html_content, "text/html")
    # msg.send()



    
    # df = pd.DataFrame(data)

    # df.to_csv('employee_on_leave.csv')


