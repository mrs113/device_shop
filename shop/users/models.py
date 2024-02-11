from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
# user = get_user_model()


class User(AbstractUser):
    image = models.ImageField(upload_to=f'user/%Y/%m/%d/', verbose_name='Фото', null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True, verbose_name='Номер телефона')
    delivery_address = models.CharField(max_length=300, null=True, blank=True, verbose_name='Адрес доставки')
