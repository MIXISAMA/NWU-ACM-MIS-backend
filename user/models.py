from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, stu_id, nickname=None, password=None, **extra_fields):
        """
        Create and save a user with the given stu_id and password.
        """
        if not stu_id:
            raise ValueError('The given stu_id must be set')
        if not nickname:
            nickname = '默认昵称' + stu_id[-4:]
        user = self.model(stu_id=stu_id, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, stu_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(stu_id, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """用户"""
    stu_id = models.CharField('学号', max_length=15, primary_key=True)
    nickname = models.CharField('昵称', max_length=24)
    description = models.TextField('自我介绍', default='--', blank=True)
    avatar_key = models.CharField('头像key', max_length=48, default='avatar/default_customer')

    date_joined = models.DateTimeField('账号创建日期', auto_now_add=True)
    is_active = models.BooleanField('激活状态', default=True, help_text='不选相当于删除用户')

    USERNAME_FIELD = 'stu_id'

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return f"[{self.stu_id}] {self.nickname}"

    class Meta:
        verbose_name = verbose_name_plural = '用户'
