from django import forms

from myapp.models import UpdownFile


class DownloadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password', 'slug')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
            'slug': forms.HiddenInput(),
        }


class UploadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password', 'expires_at', 'file', 'owner', 'max_downloads')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
            'expires_at': forms.DateInput(attrs={'id': 'datepicker', 'class': 'input'}),
        }
