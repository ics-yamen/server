# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-27 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0052_auto_20181127_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectrole',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
