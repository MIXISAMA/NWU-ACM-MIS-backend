from django.db import models
from user.models import User

class Team(models.Model):
    name = models.CharField('队伍名', max_length=30 )
    disable = models.BooleanField('是否存在', default=False)
    users = models.ManyToManyField(User, 'teams')
    
    class Meta:
        verbose_name = verbose_name_plural = '队伍'


class Contest(models.Model):
    class RewardLevel(models.TextChoices):
        STATE = 'ST', '国级'
        PROVINCE = 'PR', '省级'
        CAMPUS = 'CP', '校级'
    
    class RewardType(models.TextChoices):
        ICPC = 'IC', 'ICPC'
        CCPC = 'CC', 'CCPC'
        OTHERS = 'OT', 'Other'
    
    team_contests = models.ManyToManyField(Team, through='TeamContest', through_fields=('contest', 'team') )
    name = models.CharField('名称', max_length=30)
    start_time = models.DateTimeField('时间')
    record_type = models.CharField('竞赛类型', max_length=2, choices=RewardType.choices)
    record_level = models.CharField('比赛分级', max_length=2, choices=RewardLevel.choices)
    class Meta:
        verbose_name = verbose_name_plural = '比赛'


class TeamContest(models.Model):
    team = models.ForeignKey(Team, models.PROTECT)
    have_reward = models.BooleanField('是否获奖', default=False )
    contest = models.ForeignKey(Contest, models.PROTECT)
    class Meta:
        verbose_name = verbose_name_plural = '队伍-比赛'

class Reward(models.Model):
    class RewardRanting(models.TextChoices):
        AU = 'G', '金奖'
        AG = 'S', '银奖'
        CU = 'B', '铜奖'

    team_contest = models.OneToOneField(TeamContest, on_delete=models.PROTECT)
    record = models.CharField('奖牌类型', max_length=2, choices=RewardRanting.choices)
    class Meta:
        verbose_name = verbose_name_plural = '奖项'


# Create your models here.
