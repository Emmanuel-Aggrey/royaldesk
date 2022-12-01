import os

from celery import Celery
from celery import shared_task

from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HRMSPROJECT.settings')

app = Celery('HRMSPROJECT')

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'employee_on_leave': {
        'task': 'hrms.tasks.employee_on_leave',
        # Executes every Day at Midnight
        'schedule': crontab(minute=0, hour=0),
        # 'args': (1,2)
    },
    'backup-database': {
        'task': 'hrms.tasks.backupdb',
        # Executes every Day at Midnight
        'schedule': crontab(minute=0, hour=0),
        # 'args': (3,4)
    },
     'anviz_employees_from_leave': {
        'task': 'hrms.tasks.anviz_employee',
        # Executes every Day morning at 9:30 a.m.
        'schedule': crontab(minute=30, hour=9),
        # 'args': (3,4)
    },
    
}


# app.conf.timezone = 'UTC'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()




@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')