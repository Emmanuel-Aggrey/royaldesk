from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from hrms import hr_views_report


urlpatterns = [

   path('country/',hr_views_report.country_stats),
   path('department/',hr_views_report.department_stats),
   path('employment-rate/',hr_views_report.employment_rate),
   path('employement-status/',hr_views_report.employement_status),
   path('turn-over-rate/',hr_views_report.turn_over_rate),
   path('employees-age/',hr_views_report.employees_age),
   path('leave/',hr_views_report.leave),

   ]