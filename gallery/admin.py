from django.contrib import admin
from .models import MediaFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'uploaded_by', 'uploaded_at', 'is_active', 'order']
    list_filter = ['media_type', 'is_active', 'uploaded_at']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at', 'updated_at', 'uploaded_by']
    date_hierarchy = 'uploaded_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'media_type', 'file', 'thumbnail', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only set on creation
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
