from django.urls import path
from person.views import UserList

app_name = 'person'

urlpatterns = [
    path('user', UserList.as_view(), name='user'),
]