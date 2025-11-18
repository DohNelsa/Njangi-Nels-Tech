from django import forms
from .models import MediaFile


class MediaFileForm(forms.ModelForm):
    """Form for uploading media files"""
    class Meta:
        model = MediaFile
        fields = ['title', 'description', 'media_type', 'file', 'thumbnail', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,video/*'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_file(self):
        """Validate file type"""
        file = self.cleaned_data.get('file')
        if file:
            # Check file extension
            ext = file.name.split('.')[-1].lower()
            image_exts = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']
            video_exts = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv']
            
            if ext not in image_exts + video_exts:
                raise forms.ValidationError(
                    'Unsupported file type. Please upload an image or video file.'
                )
            
            # Check file size (e.g., 50MB limit)
            if file.size > 50 * 1024 * 1024:  # 50MB
                raise forms.ValidationError('File size cannot exceed 50MB.')
        
        return file

