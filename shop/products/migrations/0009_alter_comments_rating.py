# Generated by Django 4.2.6 on 2024-02-04 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_comments_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='rating',
            field=models.PositiveSmallIntegerField(default=5, verbose_name='Оценка'),
        ),
    ]