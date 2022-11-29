from django.urls import include, path
from django.views.generic import TemplateView
from .import views


app_name = 'applicant'
urlpatterns = [
    path('applicants/',views.applicantView,name='applicants'),
    # path('applicants/',TemplateView.as_view(template_name="applicant/applicants.html"),name="applicants"),
    path('applicant/',TemplateView.as_view(template_name="applicant/applicant.html"),name="applicant"),
    # path('offerl_letter/',TemplateView.as_view(template_name="applicant/offerl_letter.html"),name="offerl_letter"),



    path('applicants-api/',views.applicant,name="applicants_api"),
    path('update_applicant/<str:applicant_id>/',views.update_applicant),

    path('offer-letter/<str:applicant_id>/',views.acceptance_view,name="acceptance_view"),
    path('offer-letter-api/<str:applicant_id>/',views.acceptance_api_view),

]
