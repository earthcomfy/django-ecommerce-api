from django.contrib import admin

from orders.models import Order, OrderItem


admin.site.register(Order)
admin.site.register(OrderItem)
