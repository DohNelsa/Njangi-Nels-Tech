from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Role choices
ROLE_CHOICES = [
    ('leader', 'Group Leader'),
    ('treasurer', 'Treasurer'),
    ('secretary', 'Secretary'),
    ('member', 'Member'),
]


class Member(models.Model):
    """Member model for NJA PLATFORM"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile', null=True, blank=True)
    name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.name} ({self.role})"

    def get_total_contributions(self):
        """Get total contributions made by this member"""
        from contributions.models import Contribution
        from django.db.models import Sum
        return Contribution.objects.filter(member=self).aggregate(
            total=Sum('amount')
        )['total'] or 0

    def get_current_balance(self):
        """Get current balance (contributions - withdrawals)"""
        from contributions.models import Withdrawal
        from django.db.models import Sum
        contributions = self.get_total_contributions()
        withdrawals = Withdrawal.objects.filter(member=self).aggregate(
            total=Sum('amount')
        )['total'] or 0
        return contributions - withdrawals

    def is_admin(self):
        """Check if member is admin (leader or treasurer)"""
        return self.role in ['leader', 'treasurer']

    def approve(self):
        """Mark member (and linked user) as active/approved. Returns True if any change saved."""
        changed = False

        if not self.is_active:
            self.is_active = True
            changed = True

        if self.user and not self.user.is_active:
            self.user.is_active = True
            self.user.save(update_fields=['is_active'])
            changed = True

        if changed:
            self.save(update_fields=['is_active'])
            # Send automatic approval email
            try:
                from .emails import send_member_approval_email
                send_member_approval_email(self)
            except Exception:
                # Email sending errors are logged inside the helper; we swallow exceptions to avoid breaking admin workflows.
                pass

        return changed

