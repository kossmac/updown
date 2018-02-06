from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from myapp.models import UpdownFile


class DownloadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password', 'slug')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
            'slug': forms.HiddenInput(),
        }

    def clean(self):
        if self.instance.is_expired:
            raise ValidationError('error')

        return self.cleaned_data

    def clean_password(self):
        password = self.cleaned_data['password']
        if self.instance.is_password_protected:
            valid = check_password(password, self.instance.password)
        else:
            valid = True

        if not valid:
            raise ValidationError('error')

        return password

    def save(self, commit=True):
        self.instance.download_counter += 1

        if commit:
            self.instance.save(update_fields=['download_counter'])

        return self.instance


class UploadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password', 'expires_at', 'file', 'max_downloads')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
            'expires_at': forms.DateInput(attrs={'id': 'datepicker', 'class': 'input'}),
        }


class AdminUploadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password', 'expires_at', 'file', 'owner', 'max_downloads')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
            'expires_at': forms.DateInput(attrs={'id': 'datepicker', 'class': 'input'}),
        }
