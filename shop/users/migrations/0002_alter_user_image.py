# Generated by Django 4.2.6 on 2023-12-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
