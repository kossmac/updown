from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from .models import UpdownFile

UPLOAD_FORM_WIDGETS = {
    'password': forms.PasswordInput(attrs={'class': 'input is-rounded', 'placeholder': 'Password (optional)'}),
    'file': forms.FileInput(attrs={'class': 'file-input'}),
    'max_downloads': forms.NumberInput(
        attrs={
            'class': 'is-rounded',
            'placeholder': 'Max Dloads: ∞ (optional)',
            'style': 'height: 2.25em;border-radius: 20px;border: 1px solid transparent;border-color:  #dbdbdb;font-size:  1rem;padding-top:  calc(0.375em - 1px);padding-bottom:  calc(0.375em - 1px);padding-left: 1.25em;box-shadow: inset 0 1px 2px rgba(10, 10, 10, 0.1)',
        }
    ),
    'expires_at': forms.DateInput(
        attrs={'id': 'datepicker', 'class': 'input is-rounded', 'placeholder': 'Expire date (optional)'}
    ),
}


class DownloadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password',)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input'}),
        }

    def __init__(self, **kwargs):
        # This form is used in GET requests. Set data to an empty dict
        # so this form is always bound and can be validated.
        kwargs['data'] = kwargs.get('data') or {}

        super(DownloadForm, self).__init__(**kwargs)

    def clean(self):
        # produces non_field_error, since is_expired is a property not an attribute of model
        if self.instance.is_expired:
            raise ValidationError(
                message='File %(name)s is expired.',
                params=dict(name=self.instance.file.name),
                code='expired',
            )

        return self.cleaned_data

    def clean_password(self):
        # check if given password is correct
        password = self.cleaned_data['password']

        if self.instance.is_password_protected:
            if not check_password(password, self.instance.password):
                raise ValidationError(
                    message='Wrong Password!',
                    code='wrong-password',
                )

        return password

    def save(self, commit=True):
        # increase download counter
        self.instance.download_counter += 1

        # but only if we commit the instance, see form_valid() of UpdownFileListView
        if commit:
            self.instance.save(update_fields=['download_counter'])

        return self.instance


class UploadForm(forms.ModelForm):
    class Meta:
        model = UpdownFile
        fields = ('password', 'expires_at', 'file', 'max_downloads')
        widgets = UPLOAD_FORM_WIDGETS


class AdminUploadForm(forms.ModelForm):
    # superuser may upload files for different users
    class Meta:
        model = UploadForm.Meta.model
        fields = UploadForm.Meta.fields + ('owner',)
        widgets = UPLOAD_FORM_WIDGETS
