from django.contrib.admin.apps import AdminConfig

class MyAdminConfig(AdminConfig):
    default_site = 'NWU_ACM_MIS.admin.MyAdminSite'
