from django.contrib import admin

from .models import Order, OrderItem


class OrderItemTabular(admin.TabularInline):
    model = OrderItem
    fields = 'product', 'name', 'price', 'quantity'
    extra = 0


class OrderTabular(admin.TabularInline):
    model = Order
    fields = "requires_delivery", "status", "payment_on_get", "is_paid"
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabular]


admin.site.register(OrderItem)