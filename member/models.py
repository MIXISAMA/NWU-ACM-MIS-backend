from datetime import datetime, timedelta

from django.db import models

from user.models import User

class Team(models.Model):
    """该队伍model只用于信息展示，可能与实际队伍有出入"""
    name_ch = models.CharField('队伍名-中文', max_length=64)
    name_en = models.CharField('队伍名-英文', max_length=64)

    def __str__(self):
        return f"{self.name_ch}"
    
    class Meta:
        verbose_name = verbose_name_plural = '队伍'


def now_year():
    return datetime.now().year

class Member(models.Model):
    """协会队员扩展信息"""
    class Role(models.TextChoices):
        NOVICE   = 'N', '萌新'
        AD       = 'A', '现役'
        RETIRED  = 'R', '退役'

    user = models.OneToOneField(User, models.CASCADE, verbose_name='用户', primary_key=True)
    role = models.CharField('用户类型', max_length=1, choices=Role.choices, default=Role.NOVICE)
    stu_id = models.CharField('学号', max_length=12, unique=True)
    realname = models.CharField('真实姓名', max_length=32)
    college = models.CharField('院系', max_length=32)
    department = models.CharField('专业', max_length=32)
    grade = models.IntegerField('年级', default=now_year)

    cf_id = models.CharField('CodeForces账号', max_length=24)
    cf_rank = models.IntegerField('CodeForces分数', null=True, default=None)
    cf_ac = models.IntegerField('CodeForces过题数', null=True, default=None)
    vj_id = models.CharField('vjudge账号', max_length=24)
    vj_ac = models.IntegerField('vjudge过题数', null=True, default=None)

    need_peer = models.BooleanField('是否需要队友', default=False)
    team = models.ForeignKey(
        Team, models.SET_NULL,
        related_name='members',
        null=True, blank=True, default=None,
        verbose_name='队伍'
    )

    class Meta:
        verbose_name = verbose_name_plural = '队员'

    def __str__(self):
        return f'【{self.get_role_display()}】{self.realname}[{self.stu_id}]'
    

class Contribution(models.Model):
    """贡献情况，统计学分时作为工作量的参考"""
    class Type(models.TextChoices):
        VOLUNTEER   = 'VO', '志愿者'
        CLEANING    = 'CL', '打扫卫生'
        TEACHING    = 'TE', '教学'
        QUESTION    = 'QS', '出题'
        OTHERS      = 'OT', '其他'

    title = models.CharField('主题', max_length=15)
    typ = models.CharField('分类', max_length=2, choices=Type.choices)
    date = models.DateField('日期', auto_now_add=True)
    description = models.TextField('描述', default='--')
    members = models.ManyToManyField(
        Member, 'contributions',
        blank=True, default=None,
        verbose_name='参与队员'
    )
    
    class Meta:
        verbose_name = verbose_name_plural = '贡献'

class Tag(models.Model):
    """队员可为自己打标签，比如自己擅长的领域"""
    name = models.CharField('标签名', max_length=32, primary_key=True)
    members = models.ManyToManyField(
        Member, 'tags',
        blank=True, default=None,
        verbose_name='拥有该标签队员'
    )

    class Meta:
        verbose_name = verbose_name_plural = '标签'
    
    def __str__(self):
        return self.name

class Achievement(models.Model):
    """为一些优秀的或有特殊贡献的队员颁发成就"""
    class Level(models.IntegerChoices):
        UNUSUAL   = 1, '不寻常的'
        EXCELLENT = 2, '卓越的'
        MILESTONE = 3, '里程碑的'

    name = models.CharField('成就名', max_length=32)
    level = models.IntegerField('等级', choices=Level.choices)
    detail = models.TextField('描述')
    members = models.ManyToManyField(
        Member, 'achievements',
        blank=True, default=None,
        verbose_name='拥有该成就的队员'
    )

    class Meta:
        verbose_name = verbose_name_plural = '成就'
    
    def __str__(self):
        return self.name

class Training(models.Model):
    """训练情况，配套打卡机"""
    member = models.ForeignKey(Member, models.CASCADE, verbose_name='队员')
    clock_in = models.DateTimeField('开始时间', auto_now_add=True)
    clock_out = models.DateTimeField('结束时间', null=True, blank=True, default=None)
    duration = models.DurationField('训练时长', default=timedelta())

    class Meta:
        verbose_name = verbose_name_plural = '训练'
