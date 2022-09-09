# Register your models here.
import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import (Department, Dependant,
                     Designation, Education, Employee, Leave, LeavePolicy,
                     PreviousEployment, ProfessionalMembership,Contribution)

admin.site.site_header = "ROCK CITY HOTEL"  # Add this
admin.site.site_title = "ROCK CITY HOTEL"


admin.site.register([LeavePolicy])

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


class DesignationInline(admin.TabularInline):
    model = Designation


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name','email']
    search_fields = ['name']
    inlines = [
        DesignationInline,
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
                    'designation', 'mobile', 'email', 'date_employed', 'address', 'emergency_name', 'emergency_phone',]
    search_fields = ['first_name', 'last_name',
                     'other_name', 'mobile', 'employee_id',]
    list_filter = ['is_head','department', 'designation', 'status', 'is_merried','date_employed']
    list_editable = ['status', 'is_merried','is_head' ]
    exclude = ['age', ]
    actions = [export_employees]

    fieldsets = (
        ('PERSONAL INFOMATION', {
            'fields': ('employee_id', 'title','first_name','last_name','other_name','profile','gender','dob','is_merried', 'mobile', 'email', 'address','nia','snnit_number')
        }),

        ('WORK RELATED INFOMATION', {
            'fields': ('status','department', 'designation','is_head', 'date_employed','salary',)
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

    )


    inlines = [
        DependantInline,
        EducationInline,
        ProfessionalMembershipInline,
        PreviousEploymentInline,
    ]


admin.site.register(Employee, EmployeeAdmin)


class LeaveAdmin(admin.ModelAdmin):
    # fields = ['employee','status','policy','handler_over_to']
    list_display = ['employee', 'status', 'policy', 'handle_over_to',
                    'from_leave','collegue_approve', 'line_manager','hr_manager', 'leavedays', 'start', 'end']
    list_filter = ['status', 'policy', 'from_leave']
    list_editable = ['policy', 'status','collegue_approve','line_manager',
                     'from_leave', 'hr_manager', 'start', 'end','handle_over_to']
    list_filter =['collegue_approve','line_manager','hr_manager','start','end','status']
    # exclude =['on_leave',]
    search_fields = ['employee__first_name', 'employee__last_name']


admin.site.register(Leave, LeaveAdmin)

