from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .import views
app_name = 'helpdesk'

urlpatterns = [
    path('helpdesk/',login_required(TemplateView.as_view(template_name="helpdesk/helpdesk.html"))),
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

