from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from .models import UpdownFile


class DownloadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password',)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
        }

    def __init__(self, **kwargs):
        # This form is used in GET requests. Set data to an empty dict
        # so this form is always bound and could be validated.
        kwargs['data'] = kwargs.get('data') or {}

        super(DownloadForm, self).__init__(**kwargs)

    def clean(self):
        if self.instance.is_expired:
            raise ValidationError(
                message='File %(name)s is expired.',
                params=dict(name=self.instance.file.name),
                code='expired',
            )

        return self.cleaned_data

    def clean_password(self):
        password = self.cleaned_data['password']

        if self.instance.is_password_protected:
            if not check_password(password, self.instance.password):
                raise ValidationError(
                    message='Wrong Password!',
                    code='wrong-password',
                )

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
            'password': forms.PasswordInput(attrs={'class': 'input is-rounded', 'placeholder': 'Password (optional)'}),
            'file': forms.FileInput(attrs={'class': 'file-input'}),
            'expires_at': forms.DateInput(
                attrs={'id': 'datepicker', 'class': 'input', 'placeholder': 'Expire date (optional)'}
            ),
        }


class AdminUploadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password', 'expires_at', 'file', 'owner', 'max_downloads')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input is-rounded', 'placeholder': 'Password (optional)'}),
            'file': forms.FileInput(attrs={'class': 'file-input'}),
            'max_downloads': forms.NumberInput(attrs={'class': 'is-rounded', 'placeholder': '∞'}),
            'expires_at': forms.DateInput(
                attrs={'id': 'datepicker', 'class': 'input is-rounded', 'placeholder': 'Expire date (optional)'}
            ),
        }
