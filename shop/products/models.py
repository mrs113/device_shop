from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import IntegerField
from django.urls import reverse


class ProductQuerySet(models.QuerySet):

    def total_quantity(self):
        if self:
            return sum(quan for quan in self)
        return 0


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(db_index=True, verbose_name='URL', unique=True)
    image = models.ImageField(upload_to='products/first_image/%Y/%m/%d/', verbose_name='Фото')
    image2 = models.ImageField(upload_to='products/second_image/%Y/%m/%d/', verbose_name='Второе фото', blank=True)
    phone_memory_list = (
        ('64гб', '64гб'),
        ('128гб', '128гб'),
        ('256гб', '256гб'),
        ('512гб', '512гб'),
        ('1тб', '1тб'),
    )
    phone_memory = models.CharField(max_length=30, choices=phone_memory_list, verbose_name='Память смартфона', blank=True)
    phone_color = models.CharField(max_length=40, blank=True, verbose_name='Цвет')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.IntegerField(verbose_name='Цена', help_text='Указывать в рублях')
    is_have = models.BooleanField(default=True, verbose_name='Наличие')
    quantity = models.PositiveSmallIntegerField(null=True, default=50, verbose_name='Количество')
    discount = models.IntegerField(verbose_name='Скидка', help_text='Указывать в процентах', blank=True, default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name='Бренд')

    def __str__(self):
        return f'{self.brand} {self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-id',)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'product_slug': self.slug})

    def display_id(self):
        return f'{self.id:05}'

    def sell_price(self):
        if self.discount:
            return round(self.price - (self.price / 100 * self.discount))
        else:
            return self.price

    objects = ProductQuerySet.as_manager()


class Category(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название')
    slug = models.SlugField(db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)


class Brand(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название')
    slug = models.SlugField(db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='brand/%Y/%m/%d/', verbose_name='Фото')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ('-id',)




class CommentsQuerySet(models.QuerySet):

    def sum_rating(self):
        if self:
            sum_rating2 = sum(comment.rating for comment in self)
            quantity_comment = sum(comment.quantity for comment in self)
            return round(sum_rating2 / quantity_comment, 1)


class Comments(models.Model):
    product = models.ForeignKey(to=Product, related_name='comm'
                                                         'ents_products', on_delete=models.PROTECT, verbose_name='Товар')
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_DEFAULT, default=None, verbose_name='Имя')
    body = models.TextField(verbose_name='Текст комментария')

    # rating_list = (
    #     (int(1), int(1)),
    #     (int(2), int(2)),
    #     (int(3), int(3)),
    #     (int(4), int(4)),
    #     (int(5), int(5)),
    # )

    # rating_list = (
    #     ('1', 1),
    #     ('2', 2),
    #     ('3', 3),
    #     ('4', 4),
    #     ('5', 5),
    # )

    # rating = models.CharField(max_length=30, choices=rating_list, verbose_name='Оценка', default=1)
    # rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    rating = IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ], verbose_name='Оценка'
     )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    active = models.BooleanField(default=True, verbose_name='Опубликовано')
    quantity = models.PositiveSmallIntegerField(editable=False, default=1, verbose_name='Количество')

    objects = CommentsQuerySet.as_manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product}'

    # def clean_rating(self):
    #     if self.rating > 5:
    #         raise forms.ValidationError('Оценка не должна превышать 5')


class Filter_Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    id_input = models.CharField(max_length=100, verbose_name='Id для Input', default='flexRadioDefault2', unique=True)
    value_list = (
        ('name', 'name'),
        ('-name', '-name'),
        ('price', 'price'),
        ('-price', '-price'),
        ('brand_id', 'brand_id'),
        ('-brand_id', '-brand_id'),
    )
    value = models.CharField(max_length=70, choices=value_list, verbose_name='Параметр фильтрации')
    is_have = models.BooleanField(default=True, verbose_name="Опубликовано")

    def __str__(self):
        return f'Фильтрация по {self.value}'

    class Meta:
        verbose_name = 'Фильтрация товаров'
        verbose_name_plural = 'Фильтраци товаров'
        ordering = ('id',)
