from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateOrderForm
from carts.models import Cart

from .models import Order, OrderItem
from users.models import User


def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():

                        first_name = form.cleaned_data['first_name']
                        last_name = form.cleaned_data['last_name']
                        phone_number = form.cleaned_data['phone_number']
                        delivery_address = form.cleaned_data['delivery_address']

                        User.objects.filter(username=user).update(first_name=first_name, last_name=last_name, phone_number=phone_number, delivery_address=delivery_address)

                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {name} на складе. На данный момент их всего {product.quantity}')

                            order_item = OrderItem.objects.create(
                                order=order,
                                user=order.user,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity
                            )

                            order_items = OrderItem.objects.filter(user=user)



                            product.quantity -= quantity
                            product.save()

                            for cart_item_for_order in cart_items:
                                product = cart_item.product
                                name = cart_item.product.name
                                price = cart_item.product.sell_price()
                                quantity = cart_item.quantity
                                send_mail(
                                    f'Заказ №{order_item.pk} | Пользователь: {order_item.user.username} | Товары: {cart_item_for_order.product}',
                                    f'Пользователь по имени {order_item.user.first_name} {order_item.user.last_name} оформил заказ на продукт: {cart_item_for_order.product}в количестве {cart_item_for_order.quantity} шт. в {order_item.date_create}(по МСК)',
                                    settings.EMAIL_HOST_USER,
                                    ['m.gamidov2005@gmail.com'], fail_silently=False)
                                cart_items.delete()





                        messages.success(request, 'Заказ оформлен!')
                        return redirect('users:profile')

            except ValidationError as val:
                messages.success(request, str(val))
                return redirect(request.META['HTTP_REFERER'])



    # elif request.user.first_name and request.user.last_name:
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone_number': request.user.phone_number,
            'delivery_address': request.user.delivery_address,
        }

        form = CreateOrderForm(initial=initial)

    return render(request, 'orders/orders.html', {'title': 'Заказ', 'form': form})
