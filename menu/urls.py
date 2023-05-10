
from django.urls import path

from .import api
app_name = 'menu'
urlpatterns = [
    path('menu/',api.menu,name='menu'),
    path('check/<str:check>/',api.check,name='check'),
    path('verify-payment/',api.verify_payment,name='verify_payment'),
    path('excel-menu/',api.excel_menu,name='excel_menu'),
    path('get-check/<str:check>/',api.verify_check,name='get_check'),

    
]