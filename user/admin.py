from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from user.models import User, Verification
from user.form import UserCreationForm, UserChangeForm

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('avatar_image', 'email', 'nickname', 'role')
    list_filter = ('role',)
    # list_per_page = 10

    fieldsets = (
        ('账号信息', {'fields': (
            'email',
            'nickname',
            'avatar',
            'date_joined',
            'password',
        )}),
        ('其他信息', {'fields': (
            'biography',
            'school',
            'organization',
            'city',
            'homepage',
        )}),
        ('用户类型', {'fields': ('role',)}),
        ('高级设置', {
            'classes': ('collapse',),
            'fields': ('is_banned', 'is_superuser')
        }),
    )
    readonly_fields = ('date_joined', )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'nickname',
                'password1',
                'password2',
            ),
        }),
    )
    search_fields = ('email', 'nickname')
    ordering = ('-date_joined',)
    # filter_horizontal = ()

    def avatar_image(self, obj: User):
        if not obj.avatar.name:
            return "未设置头像"
        return format_html(
            '<div style="'
            'border-radius: 30px;'
            'width:50px;'
            'height:50px;'
            'background: url({}) no-repeat center;'
            'background-size:auto 50px;"></div>',
            obj.avatar.url,
        )
    avatar_image.short_description = '头像'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = UserAdmin.add_form
        return super().get_form(request, obj, **kwargs)
    
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ('phone_number', 'is_appraiser', 'is_supervisor', 'date_joined')
    #     return ()


@admin.register(Verification)
class _(admin.ModelAdmin):
    list_display = ('email', 'code')

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
