from django.urls import path,include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import hr_views
from HRMSPROJECT.custome_decorators import group_required
from HRMSPROJECT.custome_decorators import default_passeord,applicant_user

app_name = 'hrms'

urlpatterns = [

   
   

    # path('dependant/',views.CreateDependantView.as_view()),
    # path('dependant/<str:pk>/',views.CreateDependantView.as_view()),

    # path('emp-api/<str:employee_id>/',views.updateEmployee),

    # STAFF URLS
    # path('hr/',  login_required(TemplateView.as_view(template_name="hr/hr_dashborad.html")),name='hr'),
    path('hr-dashborad',hr_views.hr_dashborad,name='hr_dashborad'),
    path('employee/', login_required(TemplateView.as_view(template_name="employees/employees.html")),name='employee'),

    path('register-employee/',  login_required(TemplateView.as_view(template_name="employees/register_employee.html")),name='register_employee'),
    path('update-employee/<str:employee_id>/',  login_required(TemplateView.as_view(template_name="employees/update_employee.html")),name='update_employee'),

    # REQUEST FOR CHANGE 
    path('request-changes/<str:employee_id>/',views.request_changes),
    # HR VIEW , GRANT REQUEST
    path('grant-request/',views.grant_request),
    path('grant-request/<int:request_id>/',views.grant_request),
    

    # GET EMPLOYEEs
    path('employees/', views.employees,name='employees'),
    # delete employee session when form is submitted
    path('allemployees/',views.allemployees),

    path('employee-api/<str:employee_id>/',views.updateEmployee),

    path('verify-data/<str:employee_id>/', views.verify_data),


    # path('employee-api/<str:employee_id>/',views.employee_api),
    path('employee-data/<str:emp_uiid>/',views.employee_data,name='employee_data'),
    path('employee-info/<str:emp_uiid>/',  TemplateView.as_view(template_name="employees/employee_info.html"),name='employee_info'),
    #check if employee exit conditions are met

    path('employee-exit-form/<str:employee_id>/',login_required(TemplateView.as_view(template_name="employees/employee_exit_form.html")),name='employee_exit_form'),

    path('exit-employee/<str:employee_id>/', views.exit_employee), 


    # EMPLOYEE DOCUMENT
    path('filename/',views.filename,name='filename'),
    path('add-document/<str:employee_id>/', views.add_document,name='add_document'),
    path('delete-dependent/<str:employee_id>/<int:pk>/', views.deletedependent),
    path('delate-document/<str:employee_id>/<int:pk>/', views.delate_document),


    path('add-dependants/<str:employee_id>/', views.add_dependants,name='add_dependants'),

    path('add-education/<str:employee_id>/',views.add_education,name='add_education'),
    path('delete-education/<str:employee_id>/<int:pk>/', views.deleteEducation),

    path('add-membership/<str:employee_id>/',views.add_membership,name='add_membership'),
    path('delete-membership/<str:employee_id>/<int:pk>/', views.deleteMembership),

    path('add-emploment/<str:employee_id>/',views.add_emploment,name='add_emploment'),
    path('delete-emploment/<str:employee_id>/<int:pk>/', views.deleteEmployment),



    # APPLY FOR LEAVE
    path('apply-leave-start/', TemplateView.as_view(template_name="leave/apply_leave_start.html")),
    path('apply-leave/', TemplateView.as_view(template_name="leave/apply_leave.html")),
    path('employee-leave/<str:employee_id>/',views.employee_leave),
    path('leave-detail/<str:employee>/<int:leave_id>/',views.leave_application_detail,name="leave_application_detail"),
    path('apply-leave/<str:employee_id>/',views.apply_leave,name='apply_leave'),
    path('my-leaves/<str:employee_id>/',views.leaves,name='my_leaves'),
    path('getleave/<int:pk>/',views.getleave,name='getleave'),
    path('update-leave/<int:leave_id>/',views.update_leave,name='update_leave'),



    # GET DEPARTMENT AND DESIGNATION
    path('designation/',views.designation,name='designation'),
    # GET ANVIZ DEPARTMENT FROM JSON FILE
    path('anviz-department/',views.anviz_department),


    # HR REPORTS
    path('hr-reports/',hr_views.hr_reports,name='hr_reports'),

    path('hr-reports/<str:data_value>/',hr_views.hr_reports,name='hr_reports'),

    path('emp-on-leave/<int:pk>/',hr_views.emp_on_leave,name='emp_on_leave'),

    path('hr-approve-leave/<int:pk>/',hr_views.hr_approve_leave,name='hr_approve_leave'),


    path('employment-rate/<str:quarter>/',hr_views.employment_rate,name='employment_rate'),


    # ATTENDANCE
    # path('attendance/', login_required(TemplateView.as_view(template_name="attendance/attendance.html")),name='attendance'),
    path('attendance/', hr_views.attendance,name='attendance'),

    path('time-attendance/',hr_views.time_attendance,name='time_attendance'),
    path('get-department/<str:department>/',hr_views.get_department,name='get_department'),
    path('clockins/',hr_views.clockins,name='clockins'),
    path('upload-anviz-user-profile/', applicant_user(TemplateView.as_view(template_name="attendance/update_anviz_user.html"))),
    path('update-anviz-user/',hr_views.update_anviz_user),
    path('daemons_service/<str:service_name>/',hr_views.daemons_service),


    # HR REPORT TABLES VIEW
    path('hr-table/',include('hrms.hr_views_report_urls'))
]


