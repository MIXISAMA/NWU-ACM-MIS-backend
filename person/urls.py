from django.urls import path
from person.views import UserList

app_name = 'person'

urlpatterns = [
    path('user', UserList.as_view(),),
    path('user/<int:pk>', UserList.as_view()),
]