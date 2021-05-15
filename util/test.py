from django.db.models import Model
from rest_framework.authtoken.models import Token
from user.models import User

class TestUtilsMixin:

    def login(self, name):
        """使用self.client登陆对应用户"""
        user: User = getattr(self, name)
        password = getattr(self, name + '_psd')
        self.client.login(username=user.email, password=password)
        token = Token.objects.get(user__email=user.email)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def create_user(self, name, email, password, nickname=None, **kwargs):
        """
        创建一个用户, 并创建self.<name>属性, 用来保管该用户model实例
        同时创建self.<name>_psd属性, 用来保管用户明文密码
        """
        user: User = User.objects.create_user(
            email, password, nickname, **kwargs,
        )
        setattr(self, name, user)
        setattr(self, name + '_psd', password)
    
    def delete_user(self, name):
        """将user从数据库中删除, 同时删除在对象中对应的属性"""
        getattr(self, name).avatar.delete()
        self.delete_obj(name)
        delattr(self, name + '_psd')

    def create_obj(self, name, model: Model, *args, **kwargs):
        """创建一个model实例, 并创建self.<name>属性保管该model实例"""
        obj = model.objects.create(*args, **kwargs)
        setattr(self, name, obj)

    def update_obj(self, name):
        """从数据库重新获取obj, 并用对应属性保管"""
        obj: Model = getattr(self, name)
        setattr(self, name, obj.__class__.objects.get(pk=obj.pk))

    def delete_obj(self, name):
        """将obj从数据库中删除, 同时删除在对象中对应的属性"""
        getattr(self, name).delete()
        delattr(self, name)

    def patch_test_one(self, url, field_name, field_value, success_code=200):
        """patch方法修改一个字段并assertEqual测试"""
        response = self.client.patch(url, {field_name: field_value})
        self.assertEqual(response.status_code, success_code)
        self.assertEqual(response.json()[field_name], field_value)