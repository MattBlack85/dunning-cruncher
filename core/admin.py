from django.contrib import admin
from core.models import Engine, Vendor

class EngineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['remindernumber']}),
        ('Date information', {'fields': ['actiondate'], 'classes': ['collapse']}),
    ]
    list_display = ('remindernumber', 'actiondate', 'is_done')
    search_fields = ['remindernumber']
    date_hierarchy = 'actiondate'

admin.site.register(Engine, EngineAdmin)
admin.site.register(Vendor)
