from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from ecommerce.models import Customer
# from users.models import User
# Register your models here.




admin.site.register(User)
# admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Customer)
class CustomerModelAdmin(ImportExportModelAdmin, admin.ModelAdmin,):
    list_display: tuple = ('full_name', 'email', 'phone', 'address')  # preview_image
    search_fields: list = ['full_name', 'email', 'address']
    list_filter: list = ['address']
    prepopulated_fields: dict = {'slug': ('full_name',)}

