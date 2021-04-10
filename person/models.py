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
    stu_id = models.CharField('学号', max_length=12, primary_key=True)
    cf_id = models.CharField('CF账号', max_length=24, null=True, blank=True, default=None)
    nickname = models.CharField('昵称', max_length=24)
    need_peer = models.BooleanField('是否需要队友', default=False)
    avatar_key = models.CharField('头像key', max_length=48, default='avatar/default_customer')

    USERNAME_FIELD = 'stu_id'

    objects = UserManager()
    
    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return f"[{self.stu_id}] {self.nickname}"

    class Meta:
        verbose_name = verbose_name_plural = '队员'

class Contirbute(models.Model):

    class ContributeType(models.TextChoices):
        VOLUNTEER = 'VO', '志愿'
        CLEANING = 'CL', '清理'
        TEACHING = 'TE', '教学'
        QUESTION = 'QS', '出题'
        OTHERS = 'OT', '其他'


    title = models.CharField('主题', max_length=15)
    contri_type = models.CharField('分类', max_length=2, choices=ContributeType.choices)  
    description = models.CharField('描述', max_length=30)
    user = models.ForeignKey(User, models.PROTECT, verbose_name='队员')
    
    class Meta:
        verbose_name = verbose_name_plural = '贡献'

class Region(models.Model):
    name = models.CharField('板块名', max_length=12)
    users = models.ManyToManyField(User, verbose_name='队员', related_name='regions')

    class Meta:
        verbose_name = verbose_name_plural = '板块'

class Training(models.Model):
    users = models.ManyToManyField(User, verbose_name='队员')
    date = models.DateField('训练日期', auto_now_add=True)
    
    class Meta:
        verbose_name = verbose_name_plural = '训练日期'
