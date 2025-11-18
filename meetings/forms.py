from django import forms
from .models import Meeting, Attendance
from members.models import Member


class MeetingForm(forms.ModelForm):
    """Form for creating/editing meetings"""
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'location', 'agenda', 'minutes', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'agenda': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'minutes': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AttendanceForm(forms.ModelForm):
    """Form for recording attendance"""
    class Meta:
        model = Attendance
        fields = ['member', 'present', 'arrival_time', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'arrival_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        meeting = kwargs.pop('meeting', None)
        super().__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(is_active=True)


class BulkAttendanceForm(forms.Form):
    """Form for bulk attendance recording"""
    present_members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Present Members'
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        label='Notes'
    )


