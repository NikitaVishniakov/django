# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 11:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todolist', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='shared',
            field=models.ManyToManyField(default=None, related_name='shared_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]