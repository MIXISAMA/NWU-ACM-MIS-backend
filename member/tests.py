from django.http import response
from django.urls.base import reverse
from rest_framework.test import APIClient, APITransactionTestCase

from util.test import TestUtilsMixin
from member.models import Member

class MemberTestCase(TestUtilsMixin, APITransactionTestCase):

    def setUp(self):
        self.create_user('c1', 'c1@xx.xx', '123', role='C')
        self.create_member_easily('m1')
        self.create_member_easily('m2')
        # self.client = APIClient()
    
    def tearDown(self):
        self.delete_user('c1')
        self.delete_member('m1')
        self.delete_member('m2')

    def test_get_members_list(self):
        """测试 查询所有队员列表"""
        self.login('m2')
        url = reverse('member-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = list()
        for member in Member.objects.all():
            data.append({
                'user': {
                    'email': member.user.email,
                    'nickname': member.user.nickname,
                    'avatar': 'http://testserver' + member.user.avatar.url,
                },
                'role': str(member.role),
                'realname': member.realname,
                'stu_id': member.stu_id,
            })
        self.assertJSONEqual(response.content, data)

    def test_get_one_member(self):
        """测试 查询单个队员"""
        self.login('c1')
        url = reverse('member-detail', args=[self.m1.user.email])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # 内容太多了不测试了
    
    def test_change_member(self):
        """测试 修改队员"""
        self.login('m1')
        url = reverse('member-detail', args=['self'])
        self.patch_test_one(url, 'need_peer', True)
        self.patch_test_one(url, 'vj_id', 'changed_vj')
        self.patch_test_one(url, 'cf_id', 'changed_cf')
        self.patch_test_one(url, 'user.nickname', '修改名')
