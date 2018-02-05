from django.contrib import admin

from myapp.models import UpdownFile


@admin.register(UpdownFile)
class UpdownFileAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created_at')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('password',)
        return super(UpdownFileAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('slug', 'created_at')
        return super(UpdownFileAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)
