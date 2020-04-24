# Generated by Django 3.0.5 on 2020-04-18 23:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bugs', '0003_auto_20200418_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bug',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='bug',
            name='assig',
            field=models.ManyToManyField(related_name='assig', to=settings.AUTH_USER_MODEL),
        ),
    ]
