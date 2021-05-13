from django.test import TestCase, Client

from plan.models import Announcement

class AnnouncementTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.add_some_test_announcements()
    
    def add_some_test_announcements(self):
        Announcement.objects.create(title='test1', content='test content1')
        Announcement.objects.create(title='test2', content='test content2')
        Announcement.objects.create(title='test3', content='test content3')

    def assert_anno(self, body: dict, anno: Announcement, has_content = True):
        self.assertEqual(body['id'], anno.id)
        self.assertEqual(body['title'], anno.title)
        if has_content:
            self.assertEqual(body['content'], anno.content)
        self.assertEqual(body['created_date'], str(anno.created_date))
        self.assertEqual(body['changed_date'], str(anno.changed_date))

    def test_get_one_announcement(self):
        """测试获取单个公告"""
        for anno in Announcement.objects.all():
            response = self.client.get(f'/plan/announcement/{anno.id}/')
            self.assertEqual(response.status_code, 200)
            body = response.json()
            self.assert_anno(body, anno)
    
    def test_get_all_announcements(self):
        """测试获取所有公告"""
        response = self.client.get('/plan/announcement/')
        self.assertEqual(response.status_code, 200)
        body_list = response.json()
        for anno in Announcement.objects.all():
            for body in body_list:
                if body['id'] == anno.id:
                    break
            else:
                raise AssertionError(f'response内未找到id为{anno.id}的对象')
            self.assert_anno(body, anno, False)
