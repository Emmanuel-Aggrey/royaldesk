from datetime import datetime,date,timedelta
import numpy as np
import random
from django.contrib.auth.hashers import  check_password
import json

def days_difference(d1, d2):
    """Difference between two datetimes: end-start date"""
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)



# d1 = '2022-09-09'
# d2 = '2022-09-20'



def days_difference_weekdays(start, end):

    if not isinstance(start, str):
        start = start.strftime('%Y-%m-%d')
        end = end.strftime('%Y-%m-%d')

        # print('string date',start,end)
      
        start = datetime.strptime(start,'%Y-%m-%d').date()
        end = datetime.strptime(end,'%Y-%m-%d').date()

        days = np.busday_count( start, end )
        # print('days',days)

        return days

    else:
        days = np.busday_count( start, end )
        # print('dates',start,end)
        # print('days',days)

        return days




def generated_ticket_number():
    return random.randint(10**5, 10**6 - 1)

# APPROVLAS LOGGING
def approvlas(supervisor,line_manager,hr_manager,username):
    print('employee')
    if supervisor:
        return {'supervisor': username}
    if line_manager:
        return {'line_manager': username}
    if hr_manager:
        return {'hr_manager': username}




def bool_values(value):
    return True if value else False


def file_exists(old_file, new_file):
    if old_file and new_file:
        return new_file
    elif new_file and old_file:
        return new_file
    elif old_file and not new_file:
        return old_file
    else:
        return


# def approvals(supervor,hod,hr):
#     # supervor,hod,hr,username = sup,hos,hr,username
#     data  ={'supervisor': supervor,'line_manager': hod,'hr_manager': hr} 

#     return data
   
# set data for leave approval process
def approvals(title,employee):
    date = datetime.now().strftime('%d %B %Y, %I:%M:%S %p')
    data  ={title: employee,'date': date} 
    
        # print(data)
    return data
        
# check status of leave approval
def check_approval_status_change(status1, status2,title,employee):
    if status1 != status2:
        return approvals(title,employee)
   



def hashed_employee(session,value):
    store = check_password(value,session)
    if True:
        return session
    else:  return  None




def day_tuple(day_offset):
    today = datetime.now().date()
    date = today + timedelta(day_offset)
    return (date.day, date.month)

three_weeks = timedelta(weeks=1)

twenty_one_days = [
    day_tuple(day)
    for day
    in range(three_weeks.days)
]


# birthdays = []
# for day, month in twenty_one_days:
#     birthdays += Person.objects.filter(
#         birthday__day=day,
#         birthday__month=month
#     )
# print(birthdays)


def anviz_department():
    with open('HRMSPROJECT/anviz_departments.json', 'r') as openfile:

            return json.load(openfile)
