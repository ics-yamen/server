# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-24 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabular', '0001_squashed_0005_auto_20181024_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('initial', 'Initial (Book Just Added)'), ('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='initial', max_length=30),
        ),
        migrations.AlterField(
            model_name='book',
            name='pending',
            field=models.BooleanField(default=False),
        ),
    ]