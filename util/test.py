from member.models import Member
from django.db.models import Model
from rest_framework.authtoken.models import Token
from user.models import User

class TestUtilsMixin:

    def login(self, name):
        """使用self.client登陆对应用户"""
        obj = getattr(self, name)
        if isinstance(obj, User):
            user = obj
        elif isinstance(obj, Member):
            user = obj.user
        else:
            raise Exception('need User or Member!')
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
        """将用户从数据库中删除, 同时删除在对象中对应的属性"""
        getattr(self, name).avatar.delete()
        self.delete_obj(name)
        delattr(self, name + '_psd')

    def create_member_easily(self, name):
        self.create_member(
            name, name+'@xx.xx', 'psd', name,
            stu_id=str(hash(name) % 999999999937), # 质数
            realname=f'朱一龙{name}',
            college='地质学系',
            department='地质工程',
            grade=2017,
            cf_id='xxx',
            vj_id='xxx',
        )
    
    def create_member(self, name, email, password, nickname=None, **kwargs):
        """
        创建一个队员, 并创建self.<name>属性, 用来保管该用户model实例
        同时创建self.<name>_psd属性, 用来保管用户明文密码
        """
        user: User = User.objects.create_user(email, password, nickname)
        member: Member = Member.objects.create(user=user, **kwargs)
        user.save() # 不知道为什么，signal里面已经save了，但是还要再save一次才能更新request里面的user
        setattr(self, name, member)
        setattr(self, name + '_psd', password)
    
    def delete_member(self, name):
        """将队员从数据库中删除, 同时删除在对象中对应的属性"""
        user = getattr(self, name).user
        user.avatar.delete()
        user.delete()
        delattr(self, name)
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
        keys = field_name.split('.')
        data = field_value
        for key in keys[::-1]:
            data = {key: data}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, success_code)
        value = response.json()
        for key in keys:
            value = value[key]
        self.assertEqual(value, field_value)
