from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

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


@admin.register(MediaClick)
class MediaClickAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'preview', 'media', 'kind', 'country', 'city', 'ip')
    list_filter = ('media', 'kind', 'country', 'created_at')
    search_fields = ('media', 'ip', 'country', 'city', 'user_agent')
    date_hierarchy = 'created_at'
    list_per_page = 50
    readonly_fields = (
        'large_preview', 'created_at', 'media', 'kind', 'ip', 'country',
        'country_code', 'city', 'user_agent',
    )

    def _thumb_url(self, obj):
        base = settings.STATIC_URL
        if obj.kind == 'video':
            poster = obj.media.rsplit('.', 1)[0] + '.jpg'
            return f'{base}me/posters/{poster}'
        return f'{base}me/thumbs/{obj.media}'

    def _full_url(self, obj):
        base = settings.STATIC_URL
        if obj.kind == 'video':
            return f'{base}me/video/{obj.media}'
        return f'{base}me/{obj.media}'

    def _render_preview(self, obj, size):
        if not obj.media:
            return '—'
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">'
            '<img src="{}" alt="{}" '
            'style="height:{}px;width:{}px;object-fit:cover;'
            'border-radius:6px;background:#111;" />'
            '</a>',
            self._full_url(obj),
            self._thumb_url(obj),
            obj.media,
            size,
            size,
        )

    @admin.display(description='image')
    def preview(self, obj):
        return self._render_preview(obj, 72)

    @admin.display(description='image')
    def large_preview(self, obj):
        return self._render_preview(obj, 240)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
