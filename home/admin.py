from django.contrib import admin

from home.models import Order, Product

admin.site.register(Product)
admin.site.register(Order)
