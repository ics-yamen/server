# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-05 08:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_auto_20180605_0822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectstatuscondition',
            old_name='value',
            new_name='days',
        ),
    ]
