from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MediaFile(models.Model):
    """Model to store images and videos"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='gallery/%Y/%m/%d/')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True, help_text='Optional thumbnail for videos')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='media_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')

    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Files'
        indexes = [
            models.Index(fields=['-uploaded_at', 'media_type']),
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"

    def get_file_extension(self):
        """Get file extension"""
        if self.file:
            return self.file.name.split('.')[-1].lower()
        return None

    def is_image(self):
        """Check if file is an image"""
        image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
        return self.get_file_extension() in image_extensions

    def is_video(self):
        """Check if file is a video"""
        video_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv']
        return self.get_file_extension() in video_extensions
