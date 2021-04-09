from django.db import models
from user.models import User

class Team(models.Model):
    name = models.CharField('队伍名', max_length=30 )
    disable = models.BooleanField('是否存在', default=False)
    users = models.ManyToManyField(User, 'teams')
    class Meta:
        verbose_name = verbose_name_plural = '队伍'


class Contest(models.Model):
    team_contests = models.ManyToManyField(Team, through='TeamContest', through_fields=('contest', 'team') )
    name = models.CharField('比赛名称', max_length=30)
    start_time = models.DateTimeField('比赛时间')
    class Meta:
        verbose_name = verbose_name_plural = '比赛'


class TeamContest(models.Model):
    team = models.ForeignKey(Team, models.PROTECT)
    have_reward = models.BooleanField('是否获奖', default=False )
    contest = models.ForeignKey(Contest, models.PROTECT)
    class Meta:
        verbose_name = verbose_name_plural = '队伍-比赛'

class Reward(models.Model):
    team_contest = models.OneToOneField(TeamContest, on_delete=models.PROTECT)
    class Meta:
        verbose_name = verbose_name_plural = '奖项'


# Create your models here.
