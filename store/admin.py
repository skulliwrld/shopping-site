from django.contrib import admin

# Register your models here.
from .models import category,Product,Order,OrderItem

admin.site.register(category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
