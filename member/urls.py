from django.urls import path
from member.views import UserList

urlpatterns = [
    path('user', UserList.as_view()),
    path('user/<int:pk>', UserList.as_view()),
    # path('region', RegionList.as_view()),
    # path('region/<int:pk>', RegionList.as_view()),
]