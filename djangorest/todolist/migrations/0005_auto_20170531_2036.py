# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 17:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_auto_20170528_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='highlighted',
        ),
        migrations.RemoveField(
            model_name='task',
            name='priority',
        ),
    ]
