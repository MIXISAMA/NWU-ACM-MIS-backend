from django.urls import path
from team.views import (TeamDetail, 
                        ContestDetail,  
                        RewardDetail)

app_name = 'team'

urlpatterns =[
    path('team',                TeamDetail.as_view()),
    path('team/<int:pk>',       TeamDetail.as_view()),
    path('contest',             ContestDetail.as_view()),
    path('contest/<int:pk>',    ContestDetail.as_view()),
    path('reward',              RewardDetail.as_view()),
    path('reward/<int:pk>',     RewardDetail.as_view()),
]