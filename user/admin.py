from django.contrib import admin
from import_export.formats import base_formats

from user.models import User
from import_export.admin import ImportExportModelAdmin


# Register your models here.


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
            base_formats.TSV,
            base_formats.JSON,
            base_formats.HTML,
        )
        return [f for f in formats if f().can_export()]
