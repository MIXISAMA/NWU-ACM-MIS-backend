from django.apps import AppConfig

class UserConfig(AppConfig):
    name = 'user'
    verbose_name = '用户'

    admin_display_priority = 1
