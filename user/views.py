import random, string, smtplib

from django.conf import settings
from django.core.mail import send_mail

from rest_framework import mixins, status, permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import (
    action, api_view, permission_classes
)
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from util.rest import detail
from user.models import User, Verification
from user.serializers import (
    UserAvatarSerializer, UserSerializer,
    VerificationSerializer, EmailRegisterSerializer,
)

@api_view(['POST'])
@permission_classes([])
def email_register(request):
    """邮箱验证"""
    serializer = EmailRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    try:
        user_email = serializer.validated_data.get('email')
        verification = Verification.objects.get(
            email=user_email,
            code=serializer.validated_data.get('code')
        )
    except Verification.DoesNotExist:
        return Response(detail('验证码无效'), status.HTTP_403_FORBIDDEN)

    verification.delete()
    serializer.save()
    response = Response(serializer.validated_data, status.HTTP_201_CREATED)
    response.data['token'] = 'Token%20'+ Token.objects.get(user__email=user_email).key
    response.set_cookie('token', response.data['token'])
    return response

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
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response(detail('该用户已注册'), status.HTTP_403_FORBIDDEN)
    try:
        # 测试用例认为邮件内容的最后6个字符是验证码
        send_mail(
            '邮箱验证',
            f'{settings.PROJECT_VERBOSE_NAME}感谢您的注册，您的验证码是 {code}',
            settings.EMAIL_FROM,
            recipient_list=[email, ],
            fail_silently=False,
        )
    except smtplib.SMTPException:
        return Response(detail('验证邮件发送失败'), status.HTTP_412_PRECONDITION_FAILED)
    
    serializer.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

class EmailAuthToken(ObtainAuthToken):
    """邮箱&密码登入"""
    def post(self, request, *args, **kwargs):
        """邮箱&密码登入"""
        response = super().post(request, *args, **kwargs)
        response.data['token'] = 'Token%20' + response.data['token']
        # response.set_cookie('token', response.data['token'], secure=True, samesite='None') # https
        response.set_cookie('token', response.data['token']) # http
        return response

class UploadAvatarView(GenericViewSet, mixins.UpdateModelMixin):
    lookup_field = 'email'
    lookup_value_regex = '[^/]+' # 不会写邮箱匹配, 当做普通字符串吧
    queryset = User.objects.filter(is_banned=False).all()
    serializer_class = UserAvatarSerializer

class IsSelfOrReadOnly(permissions.BasePermission):
    """允许所有人使用GET|HEAD|OPTION方法, 其他方法只能自己针对自己的信息操作"""
    def has_object_permission(self, request, view, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

class UserAPIView(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    """用户视图集"""
    permission_classes = (IsSelfOrReadOnly,)
    lookup_field = 'email'
    lookup_value_regex = '[^/]+' # 不会写邮箱匹配, 先当做普通字符串匹配吧
    queryset = User.objects.filter(is_banned=False).all()
    serializer_class = UserSerializer

    @action(('put', 'post'), True, 'avatar', 'upload_avatar',
            serializer_class=UserAvatarSerializer)
    def upload_avatar(self, request, email):
        return self.update(request)

@api_view(['GET'])
def self_user_info(request):
    """获取自己的用户信息"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
