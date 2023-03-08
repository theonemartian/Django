from django.contrib import admin
from .models import Restaurant, Menu,Cart,CartItem,Order,OrderItem

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
# Register your models here.
