from django.contrib import admin
from .models import Meeting, Attendance


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    readonly_fields = ['recorded_at', 'recorded_by']


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'date', 'created_at']
    search_fields = ['title', 'agenda', 'minutes']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    date_hierarchy = 'date'
    inlines = [AttendanceInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['member', 'meeting', 'present', 'arrival_time', 'recorded_at']
    list_filter = ['present', 'recorded_at']
    search_fields = ['member__name', 'meeting__title']
    readonly_fields = ['recorded_at', 'recorded_by']


