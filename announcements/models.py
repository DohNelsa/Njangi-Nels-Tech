from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    """Announcements and updates for the community"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    is_pinned = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'is_pinned']),
        ]

    def __str__(self):
        return f"{self.title} ({self.priority})"

    def is_expired(self):
        """Check if announcement has expired"""
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False


class CommunityUpdate(models.Model):
    """Community updates like savings status, meeting summaries"""
    UPDATE_TYPES = [
        ('savings_status', 'Savings Status'),
        ('meeting_summary', 'Meeting Summary'),
        ('general', 'General Update'),
        ('reminder', 'Reminder'),
    ]
    
    update_type = models.CharField(max_length=20, choices=UPDATE_TYPES, default='general')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updates_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Optional references
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.SET_NULL, null=True, blank=True, related_name='updates')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'update_type']),
        ]

    def __str__(self):
        return f"{self.get_update_type_display()}: {self.title}"


