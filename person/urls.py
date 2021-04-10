from django.urls import path
from person.views import UserList, RegionList

app_name = 'person'

urlpatterns = [
    path('user', UserList.as_view()),
    path('user/<int:pk>', UserList.as_view()),
    path('region', RegionList.as_view()),
    path('region/<int:pk>', RegionList.as_view()),
]