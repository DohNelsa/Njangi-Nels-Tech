from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member


class MemberForm(forms.ModelForm):
    """Form for creating/editing members"""
    class Meta:
        model = Member
        fields = ['name', 'phone', 'email', 'role', 'address', 'notes', 'profile_picture', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserRegistrationForm(UserCreationForm):
    """Extended user registration form with member fields"""
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=200, required=True, label='Full Name')
    phone = forms.CharField(max_length=17, required=False, label='Phone Number')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Address')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_phone(self):
        """Validate phone number format"""
        phone = self.cleaned_data.get('phone')
        if phone:
            import re
            phone_regex = re.compile(r'^\+?1?\d{9,15}$')
            if not phone_regex.match(phone):
                raise forms.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return phone


class GroupEmailForm(forms.Form):
    """Form for administrators to send a group email notification."""
    recipients = forms.ModelMultipleChoiceField(
        queryset=Member.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 10}),
        help_text="Select one or more members to email. Leave blank to send to all active members.",
    )
    include_pending = forms.BooleanField(
        required=False,
        initial=False,
        label="Include pending (inactive) members",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipients'].queryset = Member.objects.filter(is_active=True).order_by('name')



