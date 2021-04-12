from django.db import models
from user.models import User

class Team(models.Model):
    users = models.ManyToManyField(User, 'teams', verbose_name='队员')
    name = models.CharField('队伍名', max_length=30 )
    disable = models.BooleanField('是否存在', default=False)

    @property
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = verbose_name_plural = '队伍'


class Contest(models.Model):
    class ContestLevel(models.TextChoices):
        STATE = 'ST', '国级'
        PROVINCE = 'PR', '省级'
        CAMPUS = 'CP', '校级'
    
    class ContestType(models.TextChoices):
        ICPC = 'IC', 'ICPC'
        CCPC = 'CC', 'CCPC'
        OTHERS = 'OT', 'Other'
    
    teams = models.ManyToManyField(
        Team, 
        'contests',
        through='TeamContest', 
        through_fields=('contest', 'team'), 
        verbose_name='队伍-比赛'
    )
    name = models.CharField('名称', max_length=30)
    start_time = models.DateTimeField('时间')
    contest_type = models.CharField('竞赛类型', max_length=2, choices=ContestType.choices)
    contest_level = models.CharField('比赛分级', max_length=2, choices=ContestLevel.choices)
    class Meta:
        verbose_name = verbose_name_plural = '比赛'
    
    @property
    def __str__(self):
        return f"{self.name}"


class TeamContest(models.Model):
    contest = models.ForeignKey(
        Contest, 
        models.PROTECT, 
        related_name='team_contests', 
        verbose_name='比赛'
    )
    team = models.ForeignKey(
        Team, 
        models.PROTECT, 
        related_name='team_contests', 
        verbose_name='队伍'
    )
    have_reward = models.BooleanField('是否获奖', default=False )
    class Meta:
        verbose_name = verbose_name_plural = '队伍-比赛'

class Reward(models.Model):
    class RewardRanting(models.TextChoices):
        AU = 'G', '金奖'
        AG = 'S', '银奖'
        CU = 'B', '铜奖'

    team_contest = models.OneToOneField(
        TeamContest, 
        models.PROTECT, 
        related_name='reward', 
        verbose_name='队伍-比赛'
    )
    record = models.CharField('奖牌类型', max_length=2, choices=RewardRanting.choices)
    class Meta:
        verbose_name = verbose_name_plural = '奖项'

# Create your models here.
