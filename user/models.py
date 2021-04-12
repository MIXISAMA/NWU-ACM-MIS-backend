from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from NWU_ACM_MIS import settings
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,
                    email=None,
                    stu_id=None,
                    password=None,
                    nickname=None,
                    **extra_fields):
        """创建用户, email与stu_id至少提供一个"""
        if email is None:
            if stu_id is None:
                raise ValueError('email与stu_id至少提供一个')
            email = f'{stu_id}@{settings.STUDENT_EMAIL_DOMAIN}'
        if nickname is None:
            nickname = email[:10]
        user = self.model(stu_id=stu_id, email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """用户"""
    stu_id = models.CharField('学号', max_length=12, null=True, blank=True, default=None, unique=True)
    email = models.EmailField('邮箱', max_length=64, unique=True)
    is_verified = models.BooleanField('是否通过邮箱验证', default=False)
    cf_id = models.CharField('CF账号', max_length=24, null=True, blank=True, default=None)
    nickname = models.CharField('昵称', max_length=24)
    realname = models.CharField('真实姓名', max_length=32, null=True, blank=True, default=None)
    need_peer = models.BooleanField('是否需要队友', default=False)
    avatar = models.ImageField('头像', upload_to='avatar', null=True, blank=True, default=None)

    USERNAME_FIELD = 'email'#'stu_id'

    objects = UserManager()
    
    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        if self.stu_id is None:
            return f'{self.email} - {self.nickname}'
        return f"{self.stu_id} - {self.nickname}"

    class Meta:
        verbose_name = verbose_name_plural = '用户'
    

