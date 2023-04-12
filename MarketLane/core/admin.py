from django.contrib import admin
from .models import Product, CustomerAddress, ProductCart, Order
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','selling_price','discounted_price','category','gender','product_image']

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['id','customer','name','address','city','state','zip_code','phone']

@admin.register(ProductCart)
class ProductCartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer_loc', 'product','quantity', 'order_date', 'status']