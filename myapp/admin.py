from django.contrib import admin

from myapp.models import UpdownFile


@admin.register(UpdownFile)
class UpdownFileAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created_at', 'password')
