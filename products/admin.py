from django.contrib import admin

from products.models import Product, ProductCategory, Basket

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admins Product views"""
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', 'price', 'quantity', 'image', 'category')
    readonly_fields = ('description',)
    search_fields = ('name', 'category__name')
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    """Basket view in UserAdmin"""
    model = Basket
    fields = ('product', 'quantity')
    extra = 1
