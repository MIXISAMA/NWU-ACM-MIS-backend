from django.urls import path, include

from rest_framework.routers import SimpleRouter

from user.views import (
    email_register, email_verification, EmailAuthToken,
    UserAPIView, self_user_info
)

router = SimpleRouter()
router.register('user', UserAPIView, 'user')

urlpatterns =[
    path('email-verification/<str:email>/', email_verification),
    path('email-register/',                 email_register),
    path('email-login/',                    EmailAuthToken.as_view()),
    path('self/',                           self_user_info),
    path('', include(router.urls)),
]
