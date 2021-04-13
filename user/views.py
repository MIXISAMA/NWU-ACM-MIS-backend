import random, string, smtplib
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes
)
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from util.rest import detail

from NWU_ACM_MIS import settings

from user.models import User, Verification
from user.serializers import VerificationSerializer, EmailRegisterSerializer

@api_view(['POST'])
@permission_classes([])
def email_register(request):
    """邮箱验证"""
    serializer = EmailRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        verification = Verification.objects.get(
            email=serializer.validated_data.get('email'),
            code=serializer.validated_data.get('code')
        )
    except Verification.DoesNotExist:
        return Response(detail('验证失败'), status=status.HTTP_403_FORBIDDEN)

    verification.delete()
    serializer.save()
    return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    

def gen_random_code(length):
    """生成由数字和字符组成的随机字符串"""
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

@api_view(['POST'])
@permission_classes([])
def email_verification(request, email):
    """向用户提供的邮箱发送验证码"""
    try:
        verification = Verification.objects.get(email=email)
    except Verification.DoesNotExist:
        verification = Verification(email=email)
    code = gen_random_code(6)
    serializer = VerificationSerializer(
        verification,
        data={'code': code},
        partial=True
    )
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response(detail('该用户已注册'), status=status.HTTP_403_FORBIDDEN)
    try:
        send_mail(
            '邮箱验证',
            f'{settings.PROJECT_VERBOSE_NAME}感谢您的注册，您的验证码是 {code}',
            settings.EMAIL_FROM,
            recipient_list=[email, ],
            fail_silently=False,
        )
    except smtplib.SMTPException:
        return Response(detail('验证邮件发送失败'), status=status.HTTP_412_PRECONDITION_FAILED)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

class EmailAuthToken(ObtainAuthToken):
    """邮箱&密码登入"""
    def post(self, request, *args, **kwargs):
        """邮箱&密码登入"""
        response = super().post(request, *args, **kwargs)
        response.data['token'] = 'Token '+response.data['token']
        response.set_cookie('token', response.data['token'])
        return response
