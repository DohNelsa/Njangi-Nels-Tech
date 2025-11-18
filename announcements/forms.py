from django import forms
from .models import Announcement, CommunityUpdate
from meetings.models import Meeting


class AnnouncementForm(forms.ModelForm):
    """Form for creating/editing announcements"""
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority', 'is_pinned', 'expires_at', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CommunityUpdateForm(forms.ModelForm):
    """Form for creating/editing community updates"""
    class Meta:
        model = CommunityUpdate
        fields = ['update_type', 'title', 'content', 'meeting', 'is_active']
        widgets = {
            'update_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'meeting': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meeting'].queryset = Meeting.objects.all().order_by('-date')
        self.fields['meeting'].required = False


