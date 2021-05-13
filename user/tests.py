from django.core import mail
from django.test import TestCase, Client

from user.models import Verification
from rest_framework.authtoken.models import Token

class AccountTestCase(TestCase):

    def setUp(self):
        self.test_data = {
            'email': 'test@test.com',
            'nickname': 'test_nickname',
            'password': 'test_password',
        }
        self.client = Client()

    def test_mail_register(self):
        """
        测试用户邮箱注册, 然后用该邮箱登陆
        用户邮箱发送的邮件内容中, 最后六个字符被测试用例认为是验证码
        """
        email = self.test_data['email']
        # 向邮箱发送验证码
        response = self.client.post(
            f'/user/email-verification/{email}/'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(mail.outbox), 1)
        code = mail.outbox[0].body[-6:]
        veri = Verification.objects.get(email=email)
        self.assertEqual(code, veri.code)
        # 注册
        response = self.client.post(
            '/user/email-register/',
            {
                'email': email,
                'code': code,
                'nickname': self.test_data['nickname'],
                'password': self.test_data['password'],
            }
        )
        self.assertEqual(response.status_code, 201)
        token = Token.objects.get(user__email=email)
        self.assertEqual(response.json()['token'], 'Token ' + token.key)
        # 登陆
        response = self.client.post(
            '/user/email-login/',
            {
                'username': email,
                'password': self.test_data['password'],
            }
        )
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(user__email=email)
        self.assertEqual(response.json()['token'], 'Token ' + token.key)
