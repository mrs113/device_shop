# Generated by Django 4.2.6 on 2024-01-26 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_alter_comments_active_alter_comments_body_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='name',
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Имя'),
        ),
    ]
