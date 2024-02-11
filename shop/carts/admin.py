from django.contrib import admin
from .models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = 'product', 'quantity', 'date_create'
    search_fields = 'product', 'quantity', 'date_create'
    readonly_fields = ('date_create',)
    extra = 1


admin.site.register(Cart)
