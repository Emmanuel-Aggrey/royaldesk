from . import views
from django.urls import  path

app_name = 'reservations'
urlpatterns = [
    path('', views.reservations,name='reservations'),    
]