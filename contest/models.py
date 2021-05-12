from django.db import models
from member.models import Member

class Contest(models.Model):
    """竞赛信息"""
    class Level(models.TextChoices):
        STATE    = 'ST', '国级'
        PROVINCE = 'PR', '省级'
        CAMPUS   = 'CP', '校级'
    
    class Type(models.TextChoices):
        ICPC   = 'IC', 'ICPC'
        CCPC   = 'CC', 'CCPC'
        CCCC   = '4C', 'CCCC'
        OTHERS = 'OT', 'Other'

    name = models.CharField('竞赛名', max_length=30)
    date = models.DateField('日期')
    typ = models.CharField('类型', max_length=2, choices=Type.choices)
    level = models.CharField('分级', max_length=2, choices=Level.choices)
    members = models.ManyToManyField(
        Member, 'contests',
        blank=True,
        verbose_name='参加队员'
    )

    class Meta:
        verbose_name = verbose_name_plural = '竞赛'

    def __str__(self):
        return f"{self.name}"

class Reward(models.Model):
    
    contest = models.ForeignKey(Contest, models.PROTECT, verbose_name='竞赛')
    class RewardType(models.TextChoices):
        GOLD   = 'G', '金奖'
        SILVER = 'S', '银奖'
        BRONZE = 'B', '铜奖'
        GRAND  = '0', '特等奖'
        FIRST  = '1', '一等奖'
        SECOND = '2', '二等奖'
        THIRD  = '3', '三等奖'
    reward_type = models.CharField('奖牌类型', max_length=2, choices=RewardType.choices)
    certificate = models.FileField('证书', upload_to='certificates', null=True, blank=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.contest}"

class PersonalReward(Reward):

    member = models.ForeignKey(Member, models.PROTECT, verbose_name='队员')

    class Meta:
        verbose_name = verbose_name_plural = '个人奖项'
    

class TeamReward(Reward):

    team_name = models.CharField('队名', max_length=64)
    members = models.ManyToManyField(Member, verbose_name='队员')

    class Meta:
        verbose_name = verbose_name_plural = '团队奖项'

class CollegeReward(Reward):

    members = models.ManyToManyField(Member, verbose_name='队员')

    class Meta:
        verbose_name = verbose_name_plural = '学校奖项'
