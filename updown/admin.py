from django.contrib import admin

from .models import UpdownFile


@admin.register(UpdownFile)
class UpdownFileAdmin(admin.ModelAdmin):
    list_display = (
        'filename',
        'owner',
        'max_downloads',
        'download_counter',
        'remaining_downloads',
        'expires_at',
        'created_at',
        'slug',
        'is_password_protected',
        'is_expired'
    )
    list_filter = ('owner',)
    readonly_fields = (
        'slug',
        'created_at'
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('password',)
        return super(UpdownFileAdmin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context
        )

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('slug', 'created_at', 'download_counter')
        return super(UpdownFileAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def filename(self, obj):
        return str(obj)
    filename.short_description = 'filename'

    def is_expired(self, obj):
        return obj.is_expired

    is_expired.short_description = 'is expired'
    is_expired.boolean = True

    def is_password_protected(self, obj):
        return obj.is_password_protected

    is_password_protected.short_description = 'is protected'
    is_password_protected.boolean = True
