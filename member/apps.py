from django.apps import AppConfig


class MemberConfig(AppConfig):
    name = 'member'
    verbose_name = '队员'

    admin_display_priority = 2

