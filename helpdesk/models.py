from django.db import models
from hrms.models import Department,Designation,BaseModel
from django.db.models.signals import pre_save,post_save
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from hrms.models import Department,Designation
import random
from django.utils import timezone

PRIORITY = (('critical','CRITICAL'),('normal','NORMAL'))
STATUS = (('resolved','RESOLVED'),('assiend','ASSIGEND'),('pending','PENDING'))


# Create your models here.


class User(AbstractUser):
    
    profile = models.ImageField(blank=True, null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    designation = models.ForeignKey(Designation,on_delete=models.CASCADE, null=True)
    is_head = models.BooleanField(default=False)

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.title()
        else:
            return self.username.title()



    @property
    def profile_exists(self):
        if self.profile:
            return self.profile.url
        return '/static/images/faces-clipart/default_emp_profile.png/'


    def get_absolute_url(self):
        return reverse("hrms:employee")

 


    def __str__(self):
        return self.full_name

    
def hash_password(sender, instance,created,**kwargs):
    if  created:
        # print('password ',instance.password)

        instance.password  =make_password(instance.password)
        # print('password ',instance.password)

        instance.save()

post_save.connect(hash_password, sender=User)

class Issue(models.Model):
    issue_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.issue_name

    class Meta:
        unique_together = ('issue_name','department')
    

def generated_ticket_number():
    return random.randint(10**5, 10**6 - 1)


class Helpdesk(BaseModel,models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='helpdesk_users')
    subject = models.TextField()
    # description = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    priority = models.CharField(max_length=10,choices=PRIORITY,null=True,blank=True)
    handle_over_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,default=4)
    # comment = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=15,choices=STATUS,null=True,blank=True,default='pending')
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    ticket_number = models.PositiveIntegerField(null=True, blank=True,default=generated_ticket_number)
    date = models.DateField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return f'{self.subject} {self.ticket_number}'

    
    class Meta:
        ordering = ('-updated_at',)
        verbose_name= 'Ticket'
        verbose_name_plural= 'Tickets'

    @property
    def image_exists(self):
        if self.image:
            return self.image.url
        return ''




    


    



class Ticket_Comment(BaseModel,models.Model):
    ticket = models.ForeignKey(Helpdesk,on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField('comment')
    user = models.CharField(max_length=255,null=True, blank=True)


    def __str__(self):
        return self.comment

    

    class Meta:
        verbose_name = ('Comment')
        verbose_name_plural = ('Comments')
        ordering = ('created_at',)