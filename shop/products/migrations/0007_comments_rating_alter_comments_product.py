# Generated by Django 4.2.6 on 2024-01-29 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_comments_email_remove_comments_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='rating',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)], default=1, max_length=30, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments_products', to='products.product', verbose_name='Товар'),
        ),
    ]
