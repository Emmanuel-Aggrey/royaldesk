import hrms
from django.conf import settings
from django.conf.urls.static import \
    static 
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .custome_decorators import default_passeord

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_required(default_passeord((TemplateView.as_view(template_name="home.html")))) ,name="home"),

    path('', include('hrms.urls', namespace = 'hrms')),
    path('', include('helpdesk.urls', namespace = 'helpdesk')),
    path('', include('applicant.urls', namespace = 'applicant')),

    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/password_change/',login_required(TemplateView.as_view(template_name="registration/password_change.html")),name="password_change"),

    # path('accounts/password_change', include('allauth.urls')),
    path('debug/', include('debug_toolbar.urls')),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


