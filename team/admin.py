from django.contrib import admin
from team.models import Team, Contest, TeamContest, Reward


# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    pass

@admin.register(TeamContest)
class TeamContestAdmin(admin.ModelAdmin):
    pass

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    pass
