from django.contrib import admin

from product.models import Product, ProductAttribute, AttributeValue, Attribute, Image

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(AttributeValue)
admin.site.register(Attribute)
admin.site.register(Image)