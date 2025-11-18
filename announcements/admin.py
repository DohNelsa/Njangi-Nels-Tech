from django.contrib import admin
from .models import Announcement, CommunityUpdate


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_pinned', 'is_active', 'created_at', 'created_by']
    list_filter = ['priority', 'is_pinned', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    date_hierarchy = 'created_at'


@admin.register(CommunityUpdate)
class CommunityUpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'update_type', 'is_active', 'created_at', 'created_by']
    list_filter = ['update_type', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    date_hierarchy = 'created_at'


