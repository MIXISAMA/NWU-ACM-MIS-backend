from django.db import reset_queries
from django.http import response
from django.urls.base import reverse
from rest_framework.test import APITransactionTestCase

from util.test import TestUtilsMixin
from member.models import Member, Team

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
                    'role': str(member.user.role),
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
    
    def test_get_one_user_member(self):
        """测试 查询用户附带队员信息"""
        url = reverse('user-member-detail', args=[self.m2.user.email])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('member' in response.json())
        self.login('m1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('member' in response.json())

class TagTestCase(TestUtilsMixin, APITransactionTestCase):
    def setUp(self):
        self.create_member_easily('m1')
        self.login('m1')
    
    def tearDown(self):
        self.delete_member('m1')
    
    def test_add_and_remove_tag(self):
        url = reverse('tag', args=['测试标签'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

class TeamTestCase(TestUtilsMixin, APITransactionTestCase):
    def setUp(self):
        self.create_member_easily('m1')
        self.login('m1')
    
    def tearDown(self):
        self.delete_member('m1')
    
    def create_a_team_and_join(self,
                               member: Member,
                               name_ch='队名',
                               name_en='team name'):
        team = Team.objects.create(name_ch=name_ch, name_en=name_en)
        member.team = team
        member.save(update_fields=['team'])
        return team

    def test_create_team(self):
        """测试创建队伍"""
        url = reverse('team-list')
        response = self.client.post(url, {
            'name_ch': '测试队名',
            'name_en': 'test team name',
        })
        self.assertEqual(response.status_code, 201)
        team: Team = Team.objects.first()
        data: dict = response.json()
        del data['members'] # 太多了不测了
        self.assertEqual(data, {
            'id': team.id,
            'name_ch': team.name_ch,
            'name_en': team.name_en,
        })
        self.update_obj('m1')
        self.assertEqual(self.m1.team, team) # 测试自动加入新创建的队伍
        team.delete()

    def test_update_team(self):
        """测试修改队伍信息"""
        team = self.create_a_team_and_join(self.m1)
        url = reverse('team-detail', args=[-1])
        self.patch_test_one(url, 'name_ch', '修改队名')
        self.patch_test_one(url, 'name_en', 'changed name')
        team.delete()

    def test_destroy_team(self):
        """测试解散队伍"""
        team = self.create_a_team_and_join(self.m1)
        url = reverse('team-detail', args=[team.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
    
    def test_get_all_teams(self):
        """测试查询所有队伍"""
        Team.objects.bulk_create([
            Team(name_ch='队名1', name_en='name1'),
            Team(name_ch='队名2', name_en='name2'),
            Team(name_ch='队名3', name_en='name3'),
        ])
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        teams = Team.objects.all()
        data = list({
            'id': team.id,
            'name_ch': team.name_ch,
            'name_en': team.name_en,
        } for team in teams)
        res_data = response.json()
        for d in res_data:
            del d['members'] # 太多了不测了
        self.assertEqual(res_data, data)
        teams.delete()

    def test_get_one_team(self):
        """测试查询一个队伍"""
        team = self.create_a_team_and_join(self.m1)
        url = reverse('team-detail', args=[team.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data: dict = response.json()
        del data['members'] # 太多了不测了
        self.assertEqual(data, {
            'id': team.id,
            'name_ch': team.name_ch,
            'name_en': team.name_en,
        })
        team.delete()

    def test_join_team(self):
        """测试加入一个队伍"""
        team = Team.objects.create(name_ch='队名', name_en='name')
        url = reverse('join-team', args=[team.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 204)
        team.delete()
    
    def test_leave_team(self):
        """测试离开一个队伍"""
        team = self.create_a_team_and_join(self.m1)
        url = reverse('leave-team', args=[self.m1.user.email])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        team.delete()
