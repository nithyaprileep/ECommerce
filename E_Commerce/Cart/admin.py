from django.contrib import admin
from .models import Product_Table, Cart, CartItem, Order, OrderItem

@admin.register(Product_Table)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock','created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','total_amount','status','created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity','price_at_purchase')
