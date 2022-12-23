from django.db import models
# from BaseModel.models import BaseModel,Depa
# from hrms.models import Department,Designation,BaseModel
from django.db.models.signals import post_save, pre_save
from datetime import datetime
from BaseModel.models import BaseModel, Department, Designation
import json
from . import message
STATUS = (('selected', 'SELECTED'), ('not selected',
          'NOT SELECTED'), ('in review', 'IN REVIEW'))


# Create your models here.
class Applicant(BaseModel):
    applicant_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="applicant_department")
    designation = models.ForeignKey(
        Designation, on_delete=models.CASCADE, related_name="applicant_designation")
    status = models.CharField(
        max_length=20, choices=STATUS, default='in review')
    cv = models.FileField(upload_to='cv/%Y-%m-%d', blank=True, null=True)
    resuming_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    salary = models.CharField(
        'net month salary', max_length=200, null=True, blank=True)
    offer_letter = models.FileField(
        upload_to='offerletter/%Y-%m-%d', blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.designation.name}'

    @property
    def position(self):
        return f'{self.department.name} {self.designation.name}'

    @property
    def cv_exists(self):
        if self.cv:
            return self.cv.url
        return ''

    @property
    def full_name(self):
        if self.first_name and self.last_name and self.other_name:
            return f'{self.first_name} {self.last_name} {self.other_name}'
        else:
            return f'{self.first_name} {self.last_name}'

    @property
    def applicant_salary(self):
        return self.salary if self.salary else self.designation.net_month_salary

    @property
    def comment(self):
        with open('applicant/applicant_message.json', 'r') as openfile:
            comment = json.load(openfile)
            if self.status == 'selected':
                return comment.get('selected')
            if self.status == 'in review':
                return comment.get('in_review')
            else:
                return comment.get('not_selected')

    @property
    def message(self):
        # print('selected ',message.message.get('selected'))
        if self.status == 'selected':


            return message.message.get('selected')

        if self.status == 'in review':
            return message.message.get('in_review')
        else:
            return message.message.get('not_selected')
    class Meta:
        ordering = ('updated_at',)


# CREATE DEFAULT USER IF FOR EMPLOYEE
def save_profile(sender, instance, **kwargs):

    if not instance.applicant_id:
        first_name = instance.first_name
        last_name = instance.last_name
        year = date = datetime.now().year
        initials = f'{first_name[0]}{last_name}-{year}'.upper()
        employee_id = initials.replace(' ', '')
        instance.applicant_id = employee_id


pre_save.connect(save_profile, sender=Applicant)
