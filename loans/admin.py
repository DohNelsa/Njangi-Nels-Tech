from django.contrib import admin
from .models import Loan, LoanRepayment


class LoanRepaymentInline(admin.TabularInline):
    model = LoanRepayment
    extra = 0
    readonly_fields = ['created_at', 'updated_at', 'recorded_by']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['member', 'amount', 'interest_rate', 'requested_date', 'due_date', 'status', 'approved_by']
    list_filter = ['status', 'requested_date', 'approved_date']
    search_fields = ['member__name', 'purpose', 'notes']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'approved_by', 'approved_date']
    date_hierarchy = 'requested_date'
    inlines = [LoanRepaymentInline]


@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'payment_date', 'status', 'recorded_by', 'created_at']
    list_filter = ['status', 'payment_date', 'created_at']
    search_fields = ['loan__member__name', 'notes']
    readonly_fields = ['created_at', 'updated_at', 'recorded_by']
    date_hierarchy = 'payment_date'


