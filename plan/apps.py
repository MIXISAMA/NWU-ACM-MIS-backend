from django.apps import AppConfig


class PlanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plan'
    verbose_name = '日程安排'

    admin_display_priority = 3
