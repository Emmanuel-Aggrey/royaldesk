
# from demoapp.models import Widget
from datetime import datetime, timedelta

import pandas as pd
from celery import shared_task
from django.conf import settings
from django.core import management
from django.core.mail import EmailMultiAlternatives, send_mail, send_mass_mail
from HRMSPROJECT import sql_server
from datetime import datetime, timedelta
from hrms.models import Leave, Employee, Department

email_from = settings.DEFAULT_FROM_EMAIL
TEST_EMAIL = settings.TEST_EMAIL
HR_EMAIL = settings.HR_EMAIL
from celery import current_app
@shared_task
def apply_for_leave_email(employee, start, end, diff, policy, department_email):

    # email_from = settings.EMAIL_HOST_USER

    subject = 'New Leave For {}'.format(employee)
    subject_ = subject.upper()
    html_content = 'Dear Sir/Madam <br> \n {} Have Applied  For {} from {} to {} making {} day(s) , Please <a href="http://192.168.1.18/apply-leave-start/">Click Here</a> to approve Thank you <p>Best Regards,</p>The Royal Desk Team.</p> <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        employee, policy, start, end, diff)



    emails = [department_email, TEST_EMAIL]

    # emails = department_email.append(TEST_EMAIL)
    emails = list(set(emails))
    # print(emails,'TEST_EMAIL',department_email)
    

    # print(emails)

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, emails)  # emails  a list department_email
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def applied_leave_reminder(employee, start, end, diff, policy, leave_id,department_email):
    leave = Leave.objects.filter(pk=leave_id,supervisor=False,line_manager=False,hr_manager=False).exists()
    if leave:
        log_to_file('reminder')
        subject = 'Leave Reminder For {}'.format(employee)
        subject_ = subject.upper()
        html_content = '{} Have Applied  For {} from {} to {} making {} day(s) , Please <a href="http://192.168.1.18/apply-leave-start/">Click Here</a> to approve Thank you <p>Best Regards,</p>The Royal Desk Team.</p> <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        employee, policy, start, end, diff)

        # GET HR EMAIL AND APPEND TO EMPLOYEE DEPARTMENT EMAIL
        # hr_email = Department.objects.only('email').filter(shortname='HR').first()

        # department_email
        emails =  [TEST_EMAIL,department_email]
        # emails = [TEST_EMAIL]
        emails = list(set(emails))
        # print(emails)

        msg = EmailMultiAlternatives(
        subject_, html_content, email_from, emails)  # emails  a list
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    leave = Leave.objects.filter(pk=leave_id,supervisor=True,line_manager=True,hr_manager=False).exists()
    if leave:
        log_to_file('to hr')
        subject = 'New Leave For {}'.format(employee)
        subject_ = subject.upper()
        html_content = '{} Have Applied  For {} from {} to {} making {} day(s) , Please <a href="http://192.168.1.18/apply-leave-start/">Click Here</a> to approve Thank you <p>Best Regards,</p>The Royal Desk Team.</p> <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        employee, policy, start, end, diff)

        # GET HR EMAIL AND APPEND TO EMPLOYEE DEPARTMENT EMAIL
        # hr_email = Department.objects.only('email').filter(shortname='HR').first()
        emails = [HR_EMAIL, TEST_EMAIL]
        # emails = [TEST_EMAIL]
        emails = list(set(emails))
        # print(emails)

        msg = EmailMultiAlternatives(
        subject_, html_content, email_from, emails)  # emails  a list
        msg.attach_alternative(html_content, "text/html")
        msg.send()



@shared_task
def send_email_new_helpdesk_employee(employee, employee_id, email, password):

    # email_from = settings.EMAIL_HOST_USER

    subject = 'Dear {}'.format(employee)
    subject_ = subject.upper()
    html_content = 'Welcome to Rock City Royal Desk, Your Employee ID  is <b>{}</b> ,And your password is <b>{}</b>, Please <a href="http://192.168.1.18/">Click Here</a> to login to use Royal Desk. <p>you will be redirected to change the default password to your own password. </p>  <p>Best Regards, <br>The Royaldesk Team.</p>  <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        employee_id, password)
    emails = [email, TEST_EMAIL]

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, emails)  # personal email address
    msg.attach_alternative(html_content, "text/html")

    # print(html_content)
    msg.send()

# send email to new employee that has an email


@shared_task
def send_email_new_employee(employee, employee_id, email, password):

    # email_from = settings.EMAIL_HOST_USER

    subject = 'Dear {}'.format(employee)
    subject_ = subject.upper()
    html_content = 'Welcome to Rock City Hotel, Your Employee ID  is <b>{}</b> ,And your password is <b>{}</b>, Please <a href="http://192.168.1.18/">Click Here</a> to login to view your employee infomation. <p>you will be redirected to change the default password to your own password. </p>  <p>Best Regards, <br>The Royaldesk Team.</p>  <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
        employee_id, password)
    emails = [email, TEST_EMAIL]

    msg = EmailMultiAlternatives(
        subject_, html_content, email_from, emails)  # personal email address
    msg.attach_alternative(html_content, "text/html")

    # print(html_content)
    msg.send()


# EMPLOYEE REQUEST DATA CHABGE
@shared_task
def send_email_request_data_change(subject, message,email='emmanuel.nartey@rockcityhotelgh.com'):

    # email_from = settings.EMAIL_HOST_USER
    html_content = '{}  <p>Best Regards, <br>The Royaldesk Team.</p>  <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
       message)

    
    emails = [email, TEST_EMAIL,]

    msg = EmailMultiAlternatives(
        subject, html_content, email_from, emails)  
    msg.attach_alternative(html_content, "text/html")

    # print(html_content)
    msg.send()


@shared_task
def employee_on_leave():
    date = datetime.now().date()
    today = date
    # yesterday = date + timedelta(days=1)
    # tomorrow = date + timedelta(days=1)

    leave = Leave.objects.select_related('employee').filter(
        resuming_date=today, from_leave=False)
    if leave:
        data = leave.values('employee__first_name', 'employee__last_name', 'employee__department__name',
                            'employee__designation__name', 'employee__department__email')

        department_email = [data[i]['employee__department__email']
                            for i in range(len(data))]

        # GET HR EMAIL FROM DEPARTEMT AND APPEND TO USER DEPARTEMT EMAIL
        hr_email = Department.objects.only(
            'email').filter(shortname='HR').first()

        department_email.append(hr_email.email)
        department_email.append(TEST_EMAIL)
        # print(department_email)

        department_email = list(set(department_email))

        # create an html table with data
        df = pd.DataFrame(data)
        # print(df)

        df.drop(['employee__department__email'], axis=1, inplace=True)

        df.columns = ['First Name', 'Last Name', 'Department', 'Designation']
        html_table = df.to_html(index=False)
        html_table = html_table.replace('border="1"', 'border="1"')
        html_table = html_table.replace(
            'style="border: 1px solid;"', 'style="align-items: center;"')

        # df.to_html(classes='table table-striped text-center', justify='center')

        # print(html_table)

        # email_from = settings.EMAIL_HOST_USER
        today = today.strftime("%B %d, %Y")

        subject = 'Employees On Leave'
        subject_ = subject.upper()
        html_content = 'List of employees whom are to return from Leave On The {}  <br> <br> {} <br> <b>Thank you</b>  <br><hr> <br> <footer><b>POWERD BY <a href="http://192.168.1.18/"> ROYALDESK </a> RCH IT</b> </footer>'.format(
            today, html_table)

        # print(html_content)
        # print(department_email)

        msg = EmailMultiAlternatives(
            subject_, html_content, email_from, department_email)  # department_email email is a list
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # df = pd.DataFrame(data)

        # df.to_csv('employee_on_leave.csv')


@shared_task
def anviz_employee(name="leave_users"):
    employees_on_leave = Leave.objects.select_related('employee').only('employee__anviz_id').filter(
        from_leave=False, status='approved', employee__anviz_id__isnull=False)
    if employees_on_leave:
        for employee_ids in employees_on_leave:
            anviz_ids = employee_ids.employee.anviz_id
            # employee = employee_ids.employee.employee_id
            resuming_date = employee_ids.resuming_date

            sql = "SELECT DISTINCT [IDCard]  FROM  [anviz].[dbo].[V_Record] WHERE [IDCard]  ='{}' AND CAST(CheckTime AS DATE) >= '{}'  ".format(
                anviz_ids, resuming_date)
            # print(sql,'\n')

            try:
                cursor = sql_server.cursor.execute(sql)
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                anviz_users = [dict(zip(columns, row)) for row in rows]

                values = [val for dic in anviz_users for val in dic.values()]

                numbers = ', '.join(map(str, values))

                from_leave = employees_on_leave.filter(
                    employee__anviz_id=numbers).update(from_leave=True)

            except:
                Leave.DoesNotExist()

# SAVE EMPLOYEE EXITING EXIT STATUS DATA TO DB IF THE SPECIFIED DATE VALUE IS DUE ELSE HOLD THE DATA 
@shared_task
def employee_exiting(employee_id, date_departure, status,old_task_id=None):

    employee = Employee.objects.get(employee_id=employee_id)
    #.update(
    #    date_departure=date_departure, status=status)
    
    employee.date_departure = date_departure
    employee.status = status

    status  = True if status =='active' else False
    employee.user.is_active = status
    employee.save()


    # REVOKE ANY OLD TASK
    if old_task_id is not None:
        current_app.control.revoke(old_task_id)
        # terminate=True

# IDCard, any_unique_value to link anviz user to employee
@shared_task
def create_anviz_employee(*args):

    print('conntected_to_server ', sql_server.conntected_to_server)
    if sql_server.conntected_to_server:

        # GET THE MAX OF Userid FROM ANVIZ DATABASE
        sql_count = "SELECT MAX(cast(Userid as int)) FROM [anviz].[dbo].[Userinfo]"
        cursor = sql_server.cursor.execute(sql_count)
        result = cursor.fetchone()
        result = result[0]+1
        # print(result)

        TABLES = '(Name,Sex,Deptid,Nation,Birthday,EmployDate,Telephone,Duty,NativePlace,IDCard,Address,Userid,UserCode)'

        # add result to data tuple as Userid and UserCode
        VALUES = (*args, result, result)

        sql = "INSERT INTO [anviz].[dbo].[Userinfo] {} VALUES {}".format(
            TABLES, VALUES)

        # print(sql)

        with open('./logs.log', 'a') as f:
            f.write(f'sql = {sql}\n\n result = {result}')

        cursor = sql_server.cursor.execute(sql)
        cursor.commit()


@shared_task
def log_to_file(name):
    today = datetime.now().strftime('%d %B %Y, %I:%M:%S %p')
    with open('./logs.log', 'a') as f:
        f.write(f'{today} {name} \n')


@shared_task
def backupdb():
    management.call_command('dbbackup')
    management.call_command('mediabackup')
