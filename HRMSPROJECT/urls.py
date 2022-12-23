import hrms
from django.conf import settings
from django.conf.urls.static import \
    static 
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .custome_decorators import default_passeord,applicant_user

urlpatterns = [
    path('back-office/', admin.site.urls,name='back_office'),
    path('',login_required(default_passeord(applicant_user((TemplateView.as_view(template_name="home.html"))))) ,name="home"),

    path('', include('hrms.urls', namespace = 'hrms')),
    path('', include('helpdesk.urls', namespace = 'helpdesk')),
    path('', include('applicant.urls', namespace = 'applicant')),

    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/password_change/',login_required(TemplateView.as_view(template_name="registration/password_change.html")),name="password_change"),

    # path('accounts/password_change', include('allauth.urls')),
    path('debug/', include('debug_toolbar.urls')),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, 'FORCE_SERVE_STATIC', False):
    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   # urlpatterns += static(
       # settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   # settings.DEBUG = False
    
#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


