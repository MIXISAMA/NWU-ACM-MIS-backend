from django.contrib import admin

from contest.models import Contest, PersonalReward, TeamReward, CollegeReward

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'typ', 'level', 'date')
    ordering = ('-date',)
    fields = ('name', 'typ', 'level', 'date', 'members')
    filter_horizontal = ('members',)

class RewardAdmin(admin.ModelAdmin):
    list_display = ('contest', 'reward_type', 'date_display')
    ordering = ('-contest__date',)
    list_filter = ('reward_type',)
    fields = ('contest', 'reward_type', 'certificate')
    def date_display(self, obj):
        return obj.contest.date
    date_display.short_description = '比赛日期'

@admin.register(PersonalReward)
class PersonalRewardAdmin(RewardAdmin):
    list_display = ('member',) + RewardAdmin.list_display
    fields = RewardAdmin.fields + ('member',)

@admin.register(TeamReward)
class TeamRewardAdmin(RewardAdmin):
    list_display = ('team_name', 'members_display') + RewardAdmin.list_display
    fields = RewardAdmin.fields + ('team_name', 'members')
    filter_horizontal = ('members',)
    def members_display(self, obj):
        return list(member.realname for member in obj.members.all())
    members_display.short_description = '队员'

@admin.register(CollegeReward)
class CollegeRewardAdmin(RewardAdmin):
    fields = RewardAdmin.fields + ('members',)
    filter_horizontal = ('members',)
