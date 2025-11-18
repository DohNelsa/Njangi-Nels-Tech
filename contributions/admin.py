from django.contrib import admin
from .models import Contribution, Withdrawal, TransactionLog


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'date', 'category', 'created_at']
    list_filter = ['category', 'date', 'created_at']
    search_fields = ['member__name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    date_hierarchy = 'date'


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'date', 'status', 'approved_by', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['member__name', 'reason']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'approved_by', 'approved_at']
    date_hierarchy = 'date'


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ['transaction_type', 'member', 'amount', 'created_at', 'created_by']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['member__name', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


