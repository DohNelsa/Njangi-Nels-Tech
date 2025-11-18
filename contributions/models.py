from django.db import models
from django.core.validators import MinValueValidator
from members.models import Member


class Contribution(models.Model):
    """Member contributions/savings"""
    CATEGORY_REGULAR = 'regular'
    CATEGORY_SOCIAL = 'social'
    CATEGORY_LATENESS = 'lateness_fee'

    CATEGORY_CHOICES = [
        (CATEGORY_REGULAR, 'Regular Contribution'),
        (CATEGORY_SOCIAL, 'Social Contribution'),
        (CATEGORY_LATENESS, 'Lateness Fee'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField()
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_REGULAR)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='contributions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['member']),
        ]

    def __str__(self):
        return f"{self.member.name} - {self.amount} on {self.date}"


class Withdrawal(models.Model):
    """Member withdrawals from savings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='withdrawals_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='withdrawals_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['member', 'status']),
        ]

    def __str__(self):
        return f"{self.member.name} - {self.amount} ({self.status}) on {self.date}"


class TransactionLog(models.Model):
    """Transaction log for audit trail"""
    TRANSACTION_TYPES = [
        ('contribution', 'Contribution'),
        ('withdrawal', 'Withdrawal'),
        ('loan_granted', 'Loan Granted'),
        ('loan_repayment', 'Loan Repayment'),
    ]
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='transaction_logs')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Reference to original transaction
    contribution = models.ForeignKey(Contribution, on_delete=models.SET_NULL, null=True, blank=True)
    withdrawal = models.ForeignKey(Withdrawal, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['member', 'transaction_type']),
        ]

    def __str__(self):
        return f"{self.transaction_type} - {self.member.name if self.member else 'N/A'} - {self.amount}"


