from django import forms
from django.contrib.auth.hashers import check_password

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
        fields = ('password', 'expires_at', 'file', 'owner')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
            'expires_at': forms.DateInput(attrs={'id': 'datepicker', 'class': 'input'}),
        }
