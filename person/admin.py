from django.contrib import admin

from person.models import Region, Contirbute, Training

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
