# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-10 04:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_auto_20180320_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmembership',
            name='role',
            field=models.CharField(choices=[('normal', 'Normal'), ('admin', 'Admin')], default='normal', max_length=96),
        ),
    ]