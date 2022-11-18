from django.urls import path

from .views import *

app_name = 'base'

urlpatterns = [

    path('', landing, name='landing'),

    path('plans/', plans, name='plans'),
    path('contact-us/', contact, name='contact'),

    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('juridical-info/', juridical_info, name='juridical-info'),
    path('online-payment-protection/', online_payment_protection, name='online-payment-protection'),
    path('information-security/', information_security, name='information-security'),
    

]