import uuid
import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models


class UpdownFile(models.Model):
    file = models.FileField(verbose_name='Uploaded file', upload_to=settings.UPLOAD_STORAGE)
    slug = models.CharField(max_length=36, verbose_name='Secret URL Part')
    password = models.CharField(max_length=255, verbose_name='Password', blank=True)
    max_downloads = models.PositiveSmallIntegerField(verbose_name='Maximum downloads', blank=True, null=True)
    download_counter = models.PositiveIntegerField(verbose_name='Download counter', default=0, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    expires_at = models.DateField(verbose_name='Expiration date', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)

    def __str__(self):
        return self.file.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # new file
        if not self.pk:
            self.slug = str(uuid.uuid4())
            if not self.password == '' and (not update_fields or 'password' in update_fields):
                self.password = make_password(self.password)

        super(UpdownFile, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                     update_fields=update_fields)

    @property
    def is_expired(self):
        if self.expires_at and self.expires_at < datetime.date.today():
            return True

        return self.remaining_downloads == 0

    @property
    def has_expiry_date(self):
        return bool(self.expires_at)

    @property
    def is_password_protected(self):
        return bool(self.password)

    @property
    def remaining_downloads(self):
        if self.max_downloads:
            return self.max_downloads - self.download_counter