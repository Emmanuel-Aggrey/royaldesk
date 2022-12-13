import random
import re
import uuid
from datetime import datetime
from email import policy
from ssl import CertificateError

from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from . import partials
from BaseModel.models import BaseModel,Department,Designation
from applicant.models import Applicant


# from applicant.models import Applicant
# from django.contrib.auth.models import Group
GENDER = (('male', 'MALE'), ('female', 'FEMALE'))
TITLE = (('mr', 'MR'), ('mrs', 'MRS'), ('doc', 'DOCTOR'), ('prof',
         'PROFESSOR'), ('miss', 'MISS'), ('sir', 'SIR'), ('hon', 'HONARABLE'))
EMPLOYEE_STATUS = (('active', 'ACTIVE'), ('sacked',
                   'SACKED'), ('resign', 'RESIGN'))

STATUS = (('approved', 'APPROVED'), ('unapproved',
          'UNAPPROVED'), ('pending', 'PENDING'))

MARRITAL_STATUS = (('married','MARRIED'),('not_married','NOT MARRIED'),('divorced','Divorced'),('widow','WIDOW'),('widower','WIDOWER'),)




# Create your models here.



class Contribution(BaseModel):
    snnit_amount = models.DecimalField(default=5.5,
                                       decimal_places=2, max_digits=5, help_text='value in percentage eg 5.5%')
    snnit_amount_company = models.DecimalField(
        'snnit amount rch', default=13, decimal_places=2, max_digits=5, help_text='value in percentage eg 13%')
    provedent_amont = models.DecimalField(
        default=5, decimal_places=2, max_digits=5, help_text='value in percentage eg 5%')
    provedent_amont_company = models.DecimalField(
        'provedent amont rch', default=5, decimal_places=2, max_digits=5, help_text='value in percentage eg 5%')


    # UPDATE CONTRIBUTIONS IN DESIGNATION
    @receiver(post_save, sender='hrms.Contribution')
    def _post_save_receiver_on(sender, instance, created, **kwargs):

        snnit_amount = instance.snnit_amount
        snnit_amount_company = instance.snnit_amount_company
        provedent_amont = instance.provedent_amont
        provedent_amont_company = instance.provedent_amont_company

        Designation.objects.update(snnit_amount=snnit_amount, snnit_amount_company=snnit_amount_company,
                                   provedent_amont=provedent_amont, provedent_amont_company=provedent_amont_company)

     
# NOT USING TNIS REPLACED BY is_head in EMPLOYEE MODEL




class ActiveEmployeesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(department__for_management=False,status='active')

class EmployeesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(department__for_management=False)


class Employee(BaseModel, models.Model):
    status = models.CharField(
        max_length=10, choices=EMPLOYEE_STATUS, default='active', blank=True)
    exit_check = models.BooleanField(default=False,help_text='checks to see if the employee exit checks are successful')
    date_exited = models.DateField(null=True,blank=True,help_text='shows the date when the employee exited from the company')
    reason_exiting = models.TextField(null=True,blank=True,help_text='reason of exiting')
    employee_id = models.CharField(
        max_length=200,null=True, blank=True, unique=True, help_text='system generated (leave blank)')
    profile = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=20, choices=TITLE, null=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    other_name = models.CharField(
        'Other Name(s)', max_length=50, null=False, blank=True)
    is_head = models.BooleanField('HOD', default=False)
    nia = models.CharField(blank=True, null=True, max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=125, null=False, blank=True)
    dob = models.DateField(help_text="Date Of Birth")
    # age = models.PositiveIntegerField(blank=True, null=True)
    date_employed = models.DateField(help_text="Date Of Employment", null=True)
    address = models.CharField(max_length=100, help_text="Residential Address")
    languages = models.CharField(max_length=200, null=True)
    place_of_birth = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10)
    snnit_number = models.CharField(max_length=15, null=True, blank=True)
    is_merried = models.CharField('marital_status', max_length=20, null=True, blank=True,choices=MARRITAL_STATUS)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True,related_name='employees_department')
    designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True)
    bank_name = models.CharField(max_length=50, blank=True, null=True)
    bank_branch = models.CharField(max_length=50, blank=True, null=True)
    bank_ac = models.CharField(
        'Bank Accont No.', max_length=50, blank=True, null=True)
    salary = models.CharField(max_length=16, blank=True, null=True)
    emergency_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_phone = models.CharField(
        max_length=15, null=True, blank=True, help_text="emergency contact number")
    emergency_address = models.CharField(max_length=200, null=True, blank=True)
    next_of_kin_name = models.CharField(max_length=200, null=True, blank=True)
    next_of_kin_phone = models.CharField(max_length=15, blank=True, null=True)
    next_of_kin_address = models.CharField(
        max_length=200, blank=True, null=True)
    next_of_kin_relationship = models.CharField(
        max_length=20, null=True, blank=True)
    emp_uiid = models.UUIDField(default=uuid.uuid4, null=True, editable=True)
    anviz_id = models.CharField(max_length=20,null=True, blank=True)
    applicant = models.OneToOneField(Applicant, on_delete=models.SET_NULL, null=True, blank=True, related_name='applicant')

    objects = models.Manager() 
    activeemployees = ActiveEmployeesManager() 
    employees = EmployeesManager() 

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

    def get_absolute_url(self):
        return reverse("hrms:employee")
        

    @property
    def full_name(self):
        if self.first_name and self.last_name and self.other_name:
            return f'{self.first_name} {self.other_name} {self.last_name}'
        else:
            return f'{self.first_name} {self.last_name}'


    @property
    def my_group(self):
        pass
        # group = self.departart_heads.values_list('name', flat=True)
        # group = [group for group in group]
        # return ''.join(group)

    @property
    def profile_exists(self):
        if self.profile:
            return self.profile.url
        return'/static/js/default_profile.jpg'

    @property
    def applicant_cv_exists(self):
        if self.applicant:
            return self.applicant.cv_exists
        else:
            return False

    @property
    def with_beneficiary(self):
        if self.beneficiarys.count() > 0:
            return True
        else:
            return False

    @property
    def age(self):
        today = datetime.today()
        return today.year - int(self.dob.strftime('%Y'))# datetime.strptime(str(date), '%Y-%m-%d').year

   

    class Meta:
        unique_together = ('employee_id', 'mobile')
        ordering = ('-updated_at',)


# CREATE DEFAULT USER IF FOR EMPLOYEE
def save_profile(sender, instance, **kwargs):
    if not instance.employee_id:
        first_name = instance.first_name
        last_name = instance.last_name
        year = instance.date_employed.strftime('%Y')
        initials = f'{first_name[0]}{last_name}-{year}'.upper()
        instance.employee_id = initials.replace(' ','')
        # instance.age = age_calendar(instance.dob)

        # print('age_calendar',age_calendar(instance.dob))

        # instance.save()
    if instance.employee_id:
        first_name = instance.first_name
        last_name = instance.last_name
        year = instance.date_employed.strftime('%Y')
        initials = f'{first_name[0]}{last_name}-{year}'.upper()
        instance.employee_id = initials.replace(' ','')
        # print('employee_id not set')
        
        # instance.age = age_calendar(instance.dob)

        # instance.save()


pre_save.connect(save_profile, sender=Employee)


class Dependant(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='beneficiarys')
    gender = models.CharField(max_length=6, choices=GENDER, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    other_name = models.CharField(
        'Other Name(s)', max_length=200, null=True, blank=True)
    dob = models.DateField(null=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    # image = models.ImageField(null=True, blank=True)

    @property
    def full_name(self):
        if self.first_name and self.last_name and self.other_name:
            return f'{self.first_name} {self.last_name} {self.other_name}'
        else:
            return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name #f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("hrms:employee_view", kwargs={'pk': self.employee.pk})

    class Meta:
        pass
        # unique_together = ('first_name', 'last_name', 'address')


class Education(BaseModel, models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='educations')
    school_name = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    certificate = models.CharField(max_length=200)
    date_completed = models.DateField()

    def __str__(self):
        return f'{self.employee} {self.school_name}'

    class Meta:
        pass
        # pass
        # unique_together = ('school_name', 'course','employee')


class ProfessionalMembership(BaseModel, models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='memberships')
    name = models.CharField(max_length=200)
    # date_completed = models.DateField(null=True,blank=True)

    def __str__(self):
        return f'{self.employee} {self.name}'

    class Meta:
        pass
        # unique_together = ('name', 'employee')


class PreviousEployment(BaseModel, models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='employments')
    company = models.CharField(max_length=200, null=True)
    job_title = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.company} {self.job_title}'

    class Meta:
        pass
        # unique_together = ('job_title', 'employee')


class LeavePolicy(BaseModel, models.Model):
    name = models.CharField(max_length=70)
    days = models.PositiveSmallIntegerField(default=0)
    has_days= models.BooleanField(default=True)
    

    def __str__(self):
        return f'{self.name} : {self.days} days'


class Leave(BaseModel, models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='leave_employees')
    leave_number = models.IntegerField(default=partials.generated_ticket_number)
    start = models.DateField()
    end = models.DateField()
    status = models.CharField(
        choices=STATUS,  default='pending', max_length=15)
    phone = models.CharField(max_length=15, null=True,
                             blank=True, help_text="phone while on leave")
    policy = models.ForeignKey(
        LeavePolicy, on_delete=models.CASCADE, help_text="Leave Policy")
    resuming_date = models.DateField(null=True, blank=False)
    file = models.FileField(null=True, blank=True, upload_to='leave/%Y-%m-%d')

    supervisor = models.BooleanField('supervisor',default=False)
    line_manager = models.BooleanField('hod',default=False)
    hr_manager = models.BooleanField(default=False)
    on_leave = models.BooleanField(default=False)
    from_leave = models.BooleanField(default=False)
    leavedays = models.IntegerField(default=0,editable=True) #using this because sqlite doesn't support calculations with datefieds
    supervisor_approval = models.JSONField(default=dict,null=True,blank=True) #{'name':'date'}
    line_manager_approval = models.JSONField(default=dict,null=True,blank=True)
    hr_manager_approval = models.JSONField(default=dict,null=True,blank=True)




    def __str__(self):
        return self.employee.full_name


    def get_absolute_url(self):
        return reverse("hrms:leave_application_detail", kwargs={"employee": self.employee.employee_id,"leave_id": self.pk})
    # @property
    # def leave_days(self):

    #     return self.leavedays




    @property
    def file_exists(self):
        if self.file:
            return self.file.url
        return ''

    class Meta:
        ordering = ['-updated_at']
        unique_together = ('employee', 'start')
    




def update_leave_status(sender, instance, **kwargs):

    instance.leavedays =partials.days_difference_weekdays(instance.start,instance.end)  #save the leave days

    if instance.line_manager == True and instance.hr_manager == True:
        instance.status = 'approved'

        # instance.on_leave = True
        # instance.save()

    # elif instance.line_manager==True and instance.collegue_approve== True or instance.line_manager==True:
    #     instance.status = 'pending'

    elif instance.hr_manager == True:
        instance.status = 'approved'
        # instance.on_leave = True
    elif instance.hr_manager == False:
        instance.status = 'pending'
        instance.from_leave =False

    # APPROVALS LOGGING
    # partials.approvlas(instance.supervisor, instance.line_manager, instance.hr_manager, instance.employee.full_name)

pre_save.connect(update_leave_status, sender=Leave)






class File(BaseModel):
    name = models.CharField(max_length=200,unique=True)
    
    def __str__(self):
        return self.name


class Documente(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True,related_name='employee_documents')
    description =models.CharField(max_length=200,blank=True)
    filename = models.ForeignKey(File, on_delete=models.CASCADE,related_name='filenames')
    date = models.DateField(null=True, blank=True,default=timezone.now)
    file = models.FileField(upload_to='documents/%Y-%m-%d',null=True)



    # def __str__(self):
    #     return f'{self.filename.name} {self.description}'

    

