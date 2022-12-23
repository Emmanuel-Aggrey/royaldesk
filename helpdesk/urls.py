from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from HRMSPROJECT.custome_decorators import default_passeord,help_desk_user
from .import views
app_name = 'helpdesk'

urlpatterns = [
    # path('change-default-password/', views.change_default_passwords, name='change_default_passwords'),
    path('helpdesk/',login_required(help_desk_user(default_passeord(TemplateView.as_view(template_name="helpdesk/helpdesk.html")))),name='helpdesk'),
    path('helpdesk-cases/<int:pk>/',views.helpdesk,name='helpdesk'),
    path('filter-helpdesk/<int:pk>/',views.filter_helpdesk,name='filter_helpdesk'),
    path('departments-issue/',views.departments_issue,name='departments_issue'),

    # SEND REPORT/ISSUE
    path('send-report/',views.send_report,name='send_report'),

    # GET REPORT
    path('get_issue_data/<int:pk>/',views.get_issue_data,name='get_issue_data'),

    # comment

    path('comment/<int:pk>/',views.comment,name='comment'),
]

