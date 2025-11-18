from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'role', 'date_joined', 'is_active', 'approved_status']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['date_joined']
    actions = ['approve_members']

    @admin.display(description='Approved')
    def approved_status(self, obj):
        if obj.user:
            return obj.user.is_active and obj.is_active
        return obj.is_active
    approved_status.boolean = True

    @admin.action(description='Approve selected members')
    def approve_members(self, request, queryset):
        updated = 0
        for member in queryset:
            if member.approve():
                updated += 1
        self.message_user(request, f'{updated} member(s) approved.')

    def save_model(self, request, obj, form, change):
        if change:
            previous = Member.objects.get(pk=obj.pk)
        else:
            previous = None
        super().save_model(request, obj, form, change)

        if obj.is_active and ((previous and not previous.is_active) or not previous):
            obj.approve()


