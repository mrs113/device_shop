from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product


class CartQuerySet(models.QuerySet):

    def total_price(self):
        return sum(price.products_price() for price in self)

    def total_quantity(self):
        if self:
            return sum(quan.quantity for quan in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    objects = CartQuerySet().as_manager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.user:
            return f'Пользователь - {self.user} | Товар - {self.product.name} | Количество - {self.quantity}'
        return f'Анонимный пользователь | Товар - {self.product.name} | Количество - {self.quantity}'

    def products_price(self):
        return self.product.sell_price() * self.quantity
