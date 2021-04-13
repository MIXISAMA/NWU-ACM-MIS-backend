from django.urls import path

from user.views import email_register, email_verification, EmailAuthToken

app_name = 'user'

urlpatterns =[
    path('email-verification/<str:email>/', email_verification),
    path('email-register/', email_register),
    path('email-login/', EmailAuthToken.as_view()),
]
