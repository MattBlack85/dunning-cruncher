from django.contrib import admin
from core.models import Engine, Vendor

class EngineAdmin(admin.ModelAdmin):
    list_display = ('remindernumber', 'actiondate', 'is_done')
    search_fields = ['remindernumber']
    date_hierarchy = 'actiondate'

class VendorAdmin(admin.ModelAdmin):
    list_display = ('vnumber', 'vname', 'vmail')
    search_fields = ['vnumber']

admin.site.register(Engine, EngineAdmin)
admin.site.register(Vendor, VendorAdmin)
