from datetime import datetime,date
import numpy as np

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



    

    # print(days)


# days_difference_weekdays()



# APPROVLAS LOGGING
def approvlas(supervisor,line_manager,hr_manager,username):
    print('employee')
    if supervisor:
        return {'supervisor': username}
    if line_manager:
        return {'line_manager': username}
    if hr_manager:
        return {'hr_manager': username}
