from django.contrib.auth import get_user_model
from django.db import models
from products.models import Product


class OrderQuerySet(models.QuerySet):

    def total_price(self):
        return sum(order.products_price() for order in self)

    def total_quantity(self):
        if self:
            return sum(order.quantity for order in self)
        return 0

    def all_products(self):
        return str(order.product for order in self)


class Order(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, verbose_name='Пользователь')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, default='В обработке', verbose_name='Статус заказа')

    class Meta:
        ordering = ('-id', '-date_create')
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'Заказ № {self.pk} | Пользователь - {self.user.first_name} {self.user.last_name}'
        else:
            return f'Заказ № {self.pk} | Пользователь - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_DEFAULT, default=None, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, default=None, verbose_name='Продукт')
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")

    class Meta:
        ordering = ('-id', '-date_create')
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"

    objects = OrderQuerySet.as_manager()

    def products_price(self):
        return self.product.sell_price() * self.quantity
