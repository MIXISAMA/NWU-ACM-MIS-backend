from django.urls import path, include

from rest_framework.routers import SimpleRouter

from user.views import (
    email_register, email_verification, EmailAuthToken,
    UserAPIView
)

router = SimpleRouter()
router.register('user', UserAPIView, 'user')

urlpatterns =[
    path('email-verification/<str:email>/', email_verification),
    path('email-register/',                 email_register),
    path('email-login/',                    EmailAuthToken.as_view()),
    path('', include(router.urls)),
]
