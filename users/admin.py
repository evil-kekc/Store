from django.contrib import admin

from users.models import User
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admins Product, Basket views"""
    list_display = ('username', 'last_login', 'is_superuser', 'is_staff', 'date_joined', 'image')
    inlines = (BasketAdmin,)
