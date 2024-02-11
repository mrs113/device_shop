# Generated by Django 4.2.6 on 2024-02-04 14:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_comments_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='rating',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]