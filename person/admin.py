from django.contrib import admin
from django.contrib.auth.models import Group
from person.models import User, Region, Contirbute, Training

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass

@admin.register(Contirbute)
class ContributeAdmin(admin.ModelAdmin):
    pass

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    fields = ['users', 'date']
    readonly_fields = ['date', ]
    
admin.site.unregister(Group)
