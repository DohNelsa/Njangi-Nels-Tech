from django.db import models
from django.core.validators import MinValueValidator
from members.models import Member


class Loan(models.Model):
    """Loan model for members borrowing from pooled savings"""
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('defaulted', 'Defaulted'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Interest rate percentage')
    purpose = models.TextField()
    requested_date = models.DateField()
    approved_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='loans_approved')
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='loans_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-requested_date', '-created_at']
        indexes = [
            models.Index(fields=['-requested_date']),
            models.Index(fields=['member', 'status']),
        ]

    def __str__(self):
        return f"{self.member.name} - {self.amount} ({self.status})"

    def get_total_amount(self):
        """Calculate total amount with interest"""
        interest = (self.amount * self.interest_rate) / 100
        return self.amount + interest

    def get_paid_amount(self):
        """Get total amount paid"""
        from django.db.models import Sum
        return self.repayments.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0

    def get_remaining_balance(self):
        """Get remaining balance"""
        return self.get_total_amount() - self.get_paid_amount()

    def is_overdue(self):
        """Check if loan is overdue"""
        from django.utils import timezone
        if self.status == 'active' and self.due_date < timezone.now().date():
            return True
        return False


class LoanRepayment(models.Model):
    """Loan repayment records"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='repayments_recorded')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']
        indexes = [
            models.Index(fields=['-payment_date']),
            models.Index(fields=['loan', 'status']),
        ]

    def __str__(self):
        return f"Repayment for {self.loan} - {self.amount} ({self.status})"

