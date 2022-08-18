from django.contrib import admin
from . models import Applicant
# Register your models here.

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['applicant_id','full_name','email','phone','department','designation','status','resuming_date']
    search_fields = ('applicant_id','first_name','last_name','other_name','email','phone','department__name','designation__name')
    list_filter = ['department','designation','status','resuming_date']

    