from django.contrib import admin

from member.models import (
    Team, Member, Contribution, Training, Tag, Achievement
)

class MemberTagInline(admin.TabularInline):
    model = Member.tags.through
    extra = 0
    verbose_name = verbose_name_plural = '队员标签'
    autocomplete_fields = ('tag',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('realname', 'nickname', 'stu_id', 'department', 'grade', 'role')
    list_filter = ('role', 'grade')
    search_fields = ('realname', 'user__nickname', 'stu_id', 'role')
    ordering = ('-user__date_joined',)
    fields = (
        'user',
        'stu_id',
        'realname',
        'college',
        'department',
        'grade',
        'cf_id',
        'vj_id',
        'role',
        'need_peer',
        'team',
    )
    autocomplete_fields = ('user', 'team')
    inlines = (MemberTagInline,)
    def nickname(self, obj):
        return obj.user.nickname
    nickname.short_description = '昵称'

@admin.register(Contribution)
class ContributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'typ', 'date', 'members_display')
    ordering = ('-date',)
    fields = ('title', 'typ', 'date', 'description', 'members')
    autocomplete_fields = ('members',)
    readonly_fields = ('date',)
    def members_display(self, obj):
        return list(member.realname for member in obj.members.all())
    members_display.short_description = '贡献队员'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name_ch', 'name_en', 'members')
    search_fields = ('name_ch', 'name_en')
    fields = ('name_ch', 'name_en')
    def members(self, obj):
        return list(member.realname for member in obj.members.all())
    members.short_description = '队员'

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('member', 'clock_in', 'clock_out', 'duration')
    fields = ('member', 'clock_in', 'clock_out', 'duration')
    readonly_fields = ('member', 'clock_in', 'clock_out', 'duration')

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name',)
    fields = ('name', 'level', 'detail', 'members')
