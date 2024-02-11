from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('cart-add/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('cart-remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
    path('cart-change/<slug:product_slug>/', views.cart_change, name='cart_change'),
    path('quantity-minus/<slug:product_slug>', views.quantity_minus, name='quantity_minus'),
    path('quantity-plus/<slug:product_slug>', views.quantity_plus, name='quantity_plus'),
]