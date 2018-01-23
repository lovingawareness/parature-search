from django.contrib import admin
from .models import Record

class RecordAdmin(admin.ModelAdmin):
    readonly_fields = ('path', 'query_string', 'user', 'user_address')
    list_filter = ['created_at', 'user']
    list_display = ('path_full', 'user', 'user_address', 'created_at')

    def view_on_site(self, obj):
        return obj.path_full

admin.site.register(Record, RecordAdmin)
