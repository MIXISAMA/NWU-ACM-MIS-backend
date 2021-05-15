from django.test import TestCase, Client

from plan.models import Announcement

class AnnouncementTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        Announcement.objects.create(title='test1', content='test content1')
        Announcement.objects.create(title='test2', content='test content2')
        Announcement.objects.create(title='test3', content='test content3')
    
    def tearDown(self):
        Announcement.objects.all().delete()
        
    def test_get_one_announcement(self):
        """测试获取单个公告"""
        for anno in Announcement.objects.all():
            response = self.client.get(f'/plan/announcement/{anno.id}/')
            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(response.content, {
                'id': anno.id,
                'title': anno.title,
                'created_date': str(anno.created_date),
                'changed_date': str(anno.changed_date),
                'content': anno.content,
            })
    
    def test_get_all_announcements(self):
        """测试获取所有公告"""
        response = self.client.get('/plan/announcement/')
        self.assertEqual(response.status_code, 200)
        expected_data = list()
        for anno in Announcement.objects.all():
            expected_data.append({
                'id': anno.id,
                'title': anno.title,
                'created_date': str(anno.created_date),
                'changed_date': str(anno.changed_date),
            })
        self.assertJSONEqual(response.content, expected_data)
