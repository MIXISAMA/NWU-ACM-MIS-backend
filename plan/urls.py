from django.urls import path
from plan.views import AnnouncementView

urlpatterns = [
    path('announcement/', AnnouncementView.as_view()),
    path('announcement/<int:id>/', AnnouncementView.as_view()),
]