from django.contrib import admin

from products.models import Product, ProductCategory


admin.site.register(ProductCategory)
admin.site.register(Product)
