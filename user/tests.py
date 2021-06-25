from io import BytesIO

from django.urls import reverse
from django.core.files import File
from django.core import mail
from django.test import TestCase, Client

from rest_framework.test import APITransactionTestCase, APIClient
from rest_framework.authtoken.models import Token

from util.test import TestUtilsMixin
from util.time import to_time_zone
from util.identicon import render_identicon
from user.models import User, Verification

class AccountTestCase(TestCase):

    def test_mail_register(self):
        """
        测试用户邮箱注册, 然后用该邮箱登陆
        用户邮箱发送的邮件内容中, 最后六个字符被测试用例认为是验证码
        """
        test_data = {
            'email': 'test@test.com',
            'nickname': 'test_nickname',
            'password': 'test_password',
        }
        client = Client()

        email = test_data['email']
        # 向邮箱发送验证码
        response = client.post(f'/user/email-verification/{email}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(mail.outbox), 1)
        code = mail.outbox[0].body[-6:]
        veri = Verification.objects.get(email=email)
        self.assertEqual(code, veri.code)
        # 注册
        response = client.post(
            '/user/email-register/',
            {
                'email': email,
                'code': code,
                'nickname': test_data['nickname'],
                'password': test_data['password'],
            }
        )
        self.assertEqual(response.status_code, 201)
        token = Token.objects.get(user__email=email)
        self.assertEqual(response.json()['token'], 'Token%20' + token.key)
        # 登陆
        response = client.post(
            '/user/email-login/',
            {
                'username': email,
                'password': test_data['password'],
            }
        )
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user__email=email)
        self.assertEqual(response.json()['token'], 'Token%20' + token.key)

        user: User = User.objects.get(email=email)
        user.avatar.delete()
        user.delete()

class UserTestCase(TestUtilsMixin, APITransactionTestCase):

    def setUp(self):
        self.create_user('u1', 'test1@xx.xx', 'psd123')
        self.create_user('u2', 'test2@xx.xx', 'psd123')
        self.client = APIClient()

    def tearDown(self):
        self.delete_user('u1')
        self.delete_user('u2')

    def test_get_user_profile(self):
        """测试 获取用户资料"""
        url = reverse('user-detail', args=[self.u1.email])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'email': self.u1.email,
            'nickname': self.u1.nickname,
            'role': str(self.u1.role),
            'avatar': 'http://testserver' + self.u1.avatar.url,
            'date_joined': to_time_zone(self.u1.date_joined),
            'college': self.u1.college,
        })

    def test_change_avatar(self):
        """测试 修改用户头像"""
        self.login('u1')
        with BytesIO() as buffer:
            buffer.name = 'avatar_change.jpg'
            render_identicon(123456789, 64).save(buffer)
            buffer.seek(0)
            url = reverse('user-upload_avatar', args=[self.u1.email])
            response = self.client.put(url, {'avatar': File(buffer)})
        self.update_obj('u1')
        self.assertEqual(response.status_code, 200)

    def test_change_user_profile(self):
        """测试 修改用户信息"""
        self.login('u1')
        url = reverse('user-detail', args=[self.u1.email])
        self.patch_test_one(url, 'nickname', 'changed nickname')
        self.patch_test_one(url, 'college', 'changed college')

    def test_change_user_profile_without_auth(self):
        """测试 未登陆用户不可以修改信息"""
        url = reverse('user-detail', args=[self.u1.email])
        response = self.client.patch(url, {'nickname': 'changed nickname'})
        self.assertEqual(response.status_code, 401)

    def test_change_user_profile_by_others(self):
        """测试 使用其他用户不可以修改该用户信息"""
        self.login('u2') # 尝试使用u2账号修改u1信息
        url = reverse('user-detail', args=[self.u1.email])
        response = self.client.patch(url, {'nickname': 'changed nickname'})
        self.assertEqual(response.status_code, 403)

    def test_get_self_user_user_info(self):
        """测试 权鉴通过后获取自己的用户信息"""
        self.login('u1')
        response = self.client.get('/user/self/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'email': self.u1.email,
            'nickname': self.u1.nickname,
            'role': str(self.u1.role),
            'avatar': self.u1.avatar.url,
            'date_joined': to_time_zone(self.u1.date_joined),
            'college': self.u1.college,
        })
