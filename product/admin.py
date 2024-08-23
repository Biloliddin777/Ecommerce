from django.contrib import admin
from product.models import Product, ProductAttribute, AttributeValue, Attribute, Image
from import_export.admin import ImportExportModelAdmin


# Register your models here.

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ImportExportModelAdmin):
    pass


@admin.register(AttributeValue)
class AttributeValueAdmin(ImportExportModelAdmin):
    pass


@admin.register(Attribute)
class AttributeAdmin(ImportExportModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    pass
