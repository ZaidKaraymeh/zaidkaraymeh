from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Blog)


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'country', 'city', 'ip', 'path', 'browser')
    list_filter = ('country', 'path', 'created_at')
    search_fields = ('ip', 'path', 'country', 'city', 'user_agent', 'referrer')
    date_hierarchy = 'created_at'
    list_per_page = 50
    readonly_fields = (
        'created_at', 'ip', 'country', 'country_code', 'city',
        'path', 'referrer', 'user_agent',
    )

    @admin.display(description='browser')
    def browser(self, obj):
        agent = obj.user_agent or ''
        return agent[:60] + ('...' if len(agent) > 60 else '')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
