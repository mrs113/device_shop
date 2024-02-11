from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from products.models import Product

from .models import Cart
from .utils import get_user_carts


def cart_page(request):
    return render(request, 'carts/cart.html', {'title': 'Корзина'})


def cart_add(request, product_slug):

    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()

            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
        messages.success(request, 'Товар добавлен в корзину')

    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()

            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)
        messages.success(request, 'Товар добавлен в корзину')





    # user_cart = get_user_carts(request)
    # cart_items_html = render_to_string(
    #     "carts/carts.html", {"carts": user_cart}, request=request)
    #
    # response_data = {
    #     "message": "Товар добавлен в корзину",
    #     "cart_items_html": cart_items_html,
    # }
    #
    # return JsonResponse(response_data)

    return redirect(request.META['HTTP_REFERER'])


def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()

    return redirect(request.META['HTTP_REFERER'])


def cart_change(request, product_slug):
    pass


def quantity_minus(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()

            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()

            else:
                messages.success(request, 'Вы не можете уменьшить больше!')
    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()

            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()

            else:
                messages.success(request, 'Вы не можете уменьшить больше!')
    return redirect(request.META['HTTP_REFERER'])


def quantity_plus(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    product_quantity = product.quantity

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()

            if cart.quantity < product_quantity:
                cart.quantity += 1
                cart.save()
            else:
                messages.success(request, 'Вы не можете добавить больше!')
    else:
        carts = Cart.objects.filter(session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()

            if cart.quantity < product_quantity:
                cart.quantity += 1
                cart.save()
            else:
                messages.success(request, 'Вы не можете добавить больше!')

    return redirect(request.META['HTTP_REFERER'])
