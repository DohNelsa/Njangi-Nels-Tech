from django.db import models
from django.core.validators import MinValueValidator
from members.models import Member


class Meeting(models.Model):
    """Meeting model for scheduling and managing meetings"""
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    agenda = models.TextField()
    minutes = models.TextField(blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='meetings_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
        ]

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"

    def get_attendance_count(self):
        """Get number of attendees"""
        return self.attendance.filter(present=True).count()

    def get_total_members(self):
        """Get total number of active members"""
        return Member.objects.filter(is_active=True).count()


class Attendance(models.Model):
    """Meeting attendance tracking"""
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendance')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    present = models.BooleanField(default=False)
    arrival_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['meeting', 'member']
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['meeting', 'member']),
        ]

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.member.name} - {self.meeting.title} ({status})"


