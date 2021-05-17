from django.urls import path, include

from rest_framework.routers import SimpleRouter

from member.views import MemberAPIView, MemberSelfAPIView

router = SimpleRouter()
router.register('member', MemberAPIView, 'member')
router.register('self', MemberSelfAPIView, 'member_self')

urlpatterns = [
    path('', include(router.urls)),
]