from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from carts.admin import CartTabAdmin
from orders.admin import OrderTabular


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'image', 'phone_number']

    inlines = [CartTabAdmin, OrderTabular]


admin.site.register(User, CustomUserAdmin)
