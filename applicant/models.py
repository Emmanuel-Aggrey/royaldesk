from django.db import models
# from BaseModel.models import BaseModel,Depa
# from hrms.models import Department,Designation,BaseModel
from BaseModel.models import BaseModel,Department,Designation

STATUS = (('selected','SELECTED'),('not selected','NOT SELECTED'),('in review','IN REVIEW'))


# Create your models here.
class Applicant(BaseModel):
    applicant_id= models.CharField(max_length=20,unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200,null=True, blank=True)
    email = models.EmailField(max_length=200,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,related_name="applicant_department")
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE,related_name="applicant_designation")
    status =models.CharField(max_length=20,choices=STATUS,default='in review')
    cv = models.FileField(upload_to='media/cv/%Y-%m-%d',blank=True,null=True)

    comment = models.TextField(blank=True,null=True,help_text="eg congratulations or wish them luck")
    resuming_date = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    salary =  models.CharField('net month salary',max_length=200,null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.designation.name}'

    
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

    class Meta:
        ordering = ('-updated_at',)

    

    
