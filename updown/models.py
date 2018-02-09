import datetime
import os
import uuid

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class RealPositiveSmallIntegerField(models.PositiveSmallIntegerField):
    def formfield(self, **kwargs):
        return super(RealPositiveSmallIntegerField, self).formfield(min_value=1, **kwargs)


class UpdownFile(models.Model):
    file = models.FileField(verbose_name='File', upload_to=settings.UPLOAD_STORAGE, null=False)
    slug = models.CharField(max_length=36, verbose_name='Secret URL Part', unique=True, null=False)
    password = models.CharField(max_length=255, verbose_name='Password', blank=True)
    max_downloads = RealPositiveSmallIntegerField(
        verbose_name='Maximum downloads',
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )
    download_counter = models.PositiveIntegerField(verbose_name='Download counter', default=0, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    expires_at = models.DateField(verbose_name='Expiration date', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Creation date', auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.file.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # is object has no pk, its new -> generate an id, and hash optional password
        if not self.pk:
            self.slug = str(uuid.uuid4())
            if not self.password == '' and (not update_fields or 'password' in update_fields):
                self.password = make_password(self.password)

        super(UpdownFile, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                     update_fields=update_fields)

    @property
    def is_expired(self):
        """
        expired if:
          (expiry date ist set and this date is in the past)
          OR
          (max_download is set and remaining downloads <= 0)
        """
        if self.expires_at and self.expires_at < datetime.date.today():
            return True

        if self.max_downloads is not None:
            return bool(self.remaining_downloads <= 0)

        return False

    @property
    def can_expire(self):
        # shall we show the clock?
        return self.max_downloads or bool(self.expires_at)

    @property
    def is_password_protected(self):
        return bool(self.password)

    @property
    def remaining_downloads(self):
        if self.max_downloads is not None:
            return self.max_downloads - self.download_counter
