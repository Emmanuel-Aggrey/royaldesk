from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import hr_views
from HRMSPROJECT.custome_decorators import group_required

app_name = 'hrms'

urlpatterns = [
    # STATIC PAGES
    path('hr/',  login_required(TemplateView.as_view(template_name="hr/hr_dashborad.html")),name='hr'),
    path('employee/', login_required(TemplateView.as_view(template_name="employees/employees.html")),name='employee'),
    path('register-staff/',  login_required(TemplateView.as_view(template_name="employees/add_employee.html")),name='register_staff'),
    path('apply-leave-start/', TemplateView.as_view(template_name="leave/apply_leave_start.html")),
    path('apply-leave/', TemplateView.as_view(template_name="leave/apply_leave.html")),
    path('employee-leave/<str:employee_id>/',views.employee_leave),
    path('leave_application_detail/',views.leave_application_detail,name="leave_application_detail"),

    # path('leave_application_detail/<str:employee_id>/<int:pk>/',views.leave_application_detail,name="leave_application_detail"),

    # REGISTER EMPLOYEE
    path('employees/', views.employees,name='employees'),
    path('employee/<str:emp_uiid>/',views.employee),
    path('employee-data/<str:emp_uiid>/',views.employee_data,name='employee_data'),
    # path('employee-info/',login_required(TemplateView(template_name="employees/employee_info.html")),name='employee_info'),
    path('employee-info/<str:emp_uiid>/',  TemplateView.as_view(template_name="employees/employee_info.html"),name='employee_info'),
    #check if employee exit conditions are met
    path('exit_employee/<str:employee_id>/', views.exit_employee), 


    # EMPLOYEE DOCUMENT
    path('filename/',views.filename,name='filename'),
    path('add-document/<str:employee_id>/', views.add_document,name='add_document'),
    path('delate-document/<str:employee_id>/<int:pk>/', views.delate_document,name='delate_document'),

    path('add-dependants/<str:employee_id>/', views.add_dependants,name='add_dependants'),
    path('add-education/<str:employee_id>/',views.add_education,name='add_education'),
    path('add-membership/<str:employee_id>/',views.add_membership,name='add_membership'),
    path('add-emploment/<str:employee_id>/',views.add_emploment,name='add_emploment'),


    # APPLY FOR LEAVE
    path('apply-leave/<str:employee_id>/',views.apply_leave,name='apply_leave'),
    path('my-leaves/<str:employee_id>/',views.leaves,name='my_leaves'),
    path('getleave/<int:pk>/',views.getleave,name='getleave'),
    path('update-leave/<int:leave_id>/',views.update_leave,name='update_leave'),


    # GET DEPARTMENT AND DESIGNATION
    path('designation/',views.designation,name='designation'),


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
    path('upload-anviz-user-profile/', TemplateView.as_view(template_name="attendance/update_anviz_user.html")),
    path('update-anviz-user/',hr_views.update_anviz_user),



]


