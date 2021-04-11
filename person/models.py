from django.db import models

from user.models import User
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
