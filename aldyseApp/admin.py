from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Boutique)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(SizeType)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin ]
 
    class Meta:
       model = Product
 
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
