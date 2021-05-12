from django.apps import AppConfig

class ContestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contest'
    verbose_name = '竞赛及获奖情况'

    admin_display_priority = 4
