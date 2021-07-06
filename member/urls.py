from django.urls import path, include

from rest_framework.routers import SimpleRouter

from member.views import (
    MemberAPIView, TeamAPIView,
    join_team, leave_team, tag,
    user_member_info,
)

router = SimpleRouter()
router.register('member', MemberAPIView, 'member')
router.register('team', TeamAPIView, 'team')

urlpatterns = [
    path('join-team/<int:id>/', join_team, name='join-team'),
    path('leave-team/<str:email>/', leave_team, name='leave-team'),
    path('tag/<str:name>/', tag, name='tag'),
    path('user/<str:email>/', user_member_info, name='user-member-detail'),
    path('', include(router.urls)),
]