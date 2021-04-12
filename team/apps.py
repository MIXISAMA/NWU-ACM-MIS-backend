from django.apps import AppConfig


class TeamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'team'
    verbose_name = '队伍'

    admin_display_priority = 3
