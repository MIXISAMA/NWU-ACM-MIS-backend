from django.urls import path, include

app_name = 'user'

urlpatterns =[
    path('authemail/', include('authemail.urls')),
]
