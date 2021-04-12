from typing import Dict
from django.contrib import admin
from django.apps import apps

class MyAdminSite(admin.AdminSite):

    def get_app_list(self, request):
        """按admin_display_priority值从小到大列出admin站点"""

        sort_reference: Dict[str, int] = dict()
        for app_label, config_cls in apps.app_configs.items():
            sort_reference[app_label] = getattr(config_cls, 'admin_display_priority', 999)
        

        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: sort_reference[x['app_label']])

        # for app in app_list:
        #     app['models'].sort(key=lambda x: x['name'])

        return app_list
