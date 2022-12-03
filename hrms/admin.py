# Register your models here.
import csv

from django.contrib import admin
from django.http import HttpResponse
from helpdesk.models import Issue
from .models import (Department, Dependant,
                     Designation, Education, Employee, Leave, LeavePolicy,
                     PreviousEployment, ProfessionalMembership,Contribution,Documente,File)

admin.site.site_header = "ROCK CITY HOTEL"  # Add this
admin.site.site_title = "ROCK CITY HOTEL"


admin.site.register([File])

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ['pk','snnit_amount','snnit_amount_company','provedent_amont','provedent_amont_company']
    list_editable = ['snnit_amount','snnit_amount_company','provedent_amont','provedent_amont_company']
    # list_display_links =['pk']

    def has_add_permission(self, request):
            # check if generally has add permission
        retVal = super().has_add_permission(request)
        # set add permission to False, if object already exists
        if retVal and Contribution.objects.exists():
            retVal = False
        return retVal


class IssueInline(admin.TabularInline):
    model = Issue


class DesignationInline(admin.TabularInline):
    model = Designation


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name','shortname','email','designations']
    search_fields = ['name']
    inlines = [
        DesignationInline,IssueInline
    ]


admin.site.register(Department, DepartmentAdmin)


class DependantInline(admin.TabularInline):
    model = Dependant


class EducationInline(admin.TabularInline):
    model = Education


class ProfessionalMembershipInline(admin.TabularInline):
    model = ProfessionalMembership


class PreviousEploymentInline(admin.TabularInline):
    model = PreviousEployment


class DocumentInline(admin.TabularInline):
    model = Documente




# export model to csv
def export_employees(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    rows = ['EMPLOYEE ID', 'STATUS', 'FRST NAME', 'LAST NAME', 'DOB', 'MARRIED', 'DEPARTMENT', 'DESIGNATION',
            'MOBILE', 'EMAIL', 'DATE EMPLOYED', 'ADDRESS', 'EMERGENCY NAME', 'EMERGENCY PHONE', ]
    writer.writerow(rows)
    employees = queryset.values_list('employee_id', 'status', 'first_name', 'last_name', 'dob', 'is_merried', 'department__name',
                                'designation__name', 'mobile', 'email', 'date_employed', 'address', 'emergency_name', 'emergency_phone',)
    for employees in employees:
        writer.writerow(employees)
    return response


export_employees.short_description = 'Export to csv'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'status', 'full_name', 'dob','is_head', 'is_merried', 'department',
                    'designation', 'mobile', 'email', 'date_employed', 'address', 'emergency_name', 'emergency_phone','anviz_id']
    search_fields = ['first_name', 'last_name',
                     'other_name', 'mobile', 'employee_id',]
    list_filter = ['is_head','department', 'designation', 'status', 'is_merried','date_employed','exit_check','date_exited']
    list_editable = ['status', 'is_merried','is_head', 'anviz_id']
    # exclude = ['age', ]
    actions = [export_employees]

    fieldsets = (
        ('PERSONAL INFOMATION', {
            'fields': ('employee_id', 'title','first_name','last_name','other_name','profile','gender','dob','is_merried', 'mobile', 'email', 'address','nia','snnit_number')
        }),

        ('WORK RELATED INFOMATION', {
            'fields': ('status','department', 'designation','is_head', 'date_employed','anviz_id','salary','exit_check','date_exited','reason_exiting')
        }),

         ('COUNTRY / REGION INFOMATION', {
            'classes': ('collapse',),
            'fields': ('country','languages','place_of_birth','nationality',)
        }),
        ('EMERGENCY / GUARDIAN INFOMATION', {
            'classes': ('collapse',),
            'fields': ('emergency_name','emergency_phone','emergency_address'),
        }),
        ('NEXT OF KEEN INFOMATION', {
            'classes': ('collapse',),
            'fields': ('next_of_kin_name', 'next_of_kin_phone','next_of_kin_address','next_of_kin_relationship',),
        }),
         ('BANK INFOMATION', {
            'classes': ('collapse',),
            'fields': ('bank_name','bank_branch','bank_ac',),
        }),
        #   ('ROYALDESK MANEGEMENT', {
        #     'classes': ('collapse',),
        #     'fields': ('for_management',),
        # }),

    )


    inlines = [
        DependantInline,
        EducationInline,
        ProfessionalMembershipInline,
        PreviousEploymentInline,
        DocumentInline,
    ]


admin.site.register(Employee, EmployeeAdmin)



class LeavePolicyAdmin(admin.ModelAdmin):
    list_display = ['name','days','has_days']
    search_fields = ['name']
    list_editable = ['days','has_days']
   


admin.site.register(LeavePolicy, LeavePolicyAdmin)

class LeaveAdmin(admin.ModelAdmin):
    # fields = ['employee','status','policy','handler_over_to']
    list_display = ['employee', 'leave_number','status', 'policy',
                    'from_leave','supervisor', 'line_manager','hr_manager', 'leavedays', 'start', 'end']
    list_filter = ['status', 'policy', 'from_leave']
    list_editable = ['policy', 'status','supervisor','line_manager',
                     'from_leave', 'hr_manager', 'start', 'end']
    list_filter =['supervisor','line_manager','hr_manager','start','end','status']
    exclude =['on_leave',]
    search_fields = ['employee__employee_id','employee__first_name', 'employee__last_name','leave_number']


admin.site.register(Leave, LeaveAdmin)

