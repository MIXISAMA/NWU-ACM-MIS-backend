from django.db import models

from markdownx.models import MarkdownxField

from member.models import Member

class Plan(models.Model):
    """提前布置的任务计划，比如训练赛、正式赛、教学等等，用于更新日程表"""

    class Type(models.TextChoices):
        TRAINING = 'X', '训练赛'
        CONTEST  = 'C', '正式赛'
        TEACHING = 'T', '教学'
        OTHERS   = 'O', '其他'

    name = models.CharField('任务名', max_length=64)
    typ = models.CharField('任务类型', max_length=1, choices=Type.choices)
    detail = models.TextField('详细说明')
    clock_in = models.DateTimeField('开始时间')
    clock_out = models.DateTimeField('结束时间')
    
    has_sent = models.BooleanField('已发送邮件', default=False)
    members = models.ManyToManyField(
        Member, 'plans',
        blank=True, default=True,
        verbose_name='通知队员'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '任务计划'

class Announcement(models.Model):

    title = models.CharField('标题', max_length=64)
    content = MarkdownxField('内容')
    created_date = models.DateField('发布日期', auto_now_add=True)
    changed_date = models.DateField('最后修改日期', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '公告'

